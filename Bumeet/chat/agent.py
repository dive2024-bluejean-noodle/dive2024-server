from typing import List
from typing_extensions import TypedDict
from langchain.schema import Document
from .config import BuMeetConfig


class BuMeetAgent:
    def __init__(self, config: BuMeetConfig) -> None:
        self.config = config
    
    def retrieve(self, state):
        """
        Retrieve documents from vectorstore

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---RETRIEVE---")
        question = state["question"]

        # Retrieval
        documents = self.config.retriever.invoke(question)
        return {"documents": documents, "question": question}

    def generate(self, state):
        """
        Generate answer using RAG on retrieved documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        
        # RAG generation
        generation = self.config.rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}

    def grade_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question
        If any document is not relevant, we will set a flag to run web search

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Filtered out irrelevant documents and updated web_search state
        """

        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]
        
        # Score each doc
        filtered_docs = []
        web_search = "No"
        for d in documents:
            score = self.config.retrieval_grader.invoke({"question": question, "document": d.page_content})
            grade = score.binary_score
            
            # Document relevant
            if grade.lower() == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            # Document not relevant
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                # We do not include the document in filtered_docs
                # We set a flag to indicate that we want to run web search
                web_search = "Yes"
                continue
        return {"documents": filtered_docs, "question": question, "web_search": web_search} #


    def transform_query(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """

        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]

        # Re-write question
        better_question = self.config.question_rewriter.invoke({"question": question})
        return {"documents": documents, "question": better_question}


    def web_search(self, state):
        """
        Web search based based on the question

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Appended web results to documents
        """

        print("---WEB SEARCH---")
        question = state["question"]
        documents = state.get("documents", [])
        # Web search
        docs = self.config.web_search_tool.invoke({"query": question})
            
        # docs가 문자열인지 확인
        if isinstance(docs, str):
            # docs가 문자열이면 바로 사용
            web_results = docs
        elif isinstance(docs, list):
            # docs가 리스트일 때, 각 문서의 content를 추출
            web_results = "\n".join([d["content"] for d in docs])

        # Document 객체로 변환
        web_results = Document(page_content=web_results)

        # 문서가 이미 있을 경우 append
        if documents is not None:
            documents.append(web_results)
        else:
            documents = [web_results]

        return {"documents": documents, "question": question}
        # return {"documents": web_results, "question": question}
        
        
    def route_question(self, state):
        """
        Route question to web search or RAG.

        Args:
            state (dict): The current graph state

        Returns:
            str: Next node to call
        """

        print("---ROUTE QUESTION---")
        question = state["question"]
        print(question)
        source = self.config.router.invoke({"question": question})  
        print(source)
        print(source.datasource)
        if source.datasource == 'web_search':
            print("---ROUTE QUESTION TO WEB SEARCH---")
            return "websearch"
        elif source.datasource == 'vectorstore':
            print("---ROUTE QUESTION TO RAG---")
            return "vectorstore"
        

    # 문서가 적합하지 않다면, 추가적으로 웹 검색 시도
    def decide_to_generate(self, state):
        """
        Determines whether to generate an answer, or add web search

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        print("---ASSESS GRADED DOCUMENTS---")
        question = state["question"]
        web_search = state["web_search"]
        filtered_documents = state["documents"]

        if web_search == "Yes":
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---")
            return "websearch"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"

    def grade_generation_v_documents_and_question(self, state):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        print("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        # 디버깅을 위한 문서 및 생성된 답변 출력
        print("Documents:")
        for doc in documents:
            print(doc.page_content[:200])  # 문서의 처음 200자만 출력 (필요시 전체 출력)
        print("Generated Answer:", generation)

        # check hallucination
        score = self.config.hallucination_grader.invoke({"documents": documents, "generation": generation})
        grade = score.binary_score

        # Check hallucination
        if grade.lower() == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            # Check question-answering
            print("---GRADE GENERATION vs QUESTION---")
            score = self.config.answer_grader.invoke({"question": question,"generation": generation})
            grade = score.binary_score
            if grade == "yes":
                print("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            else:
                print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                return "not useful"
        else:
            print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
            return "not supported"
