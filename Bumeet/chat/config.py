from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from .schemas import (
    RouteQuery, 
    GradeDocuments, 
    GradeHallucinations, 
    GradeAnswer,
)
from .prompt import (
    router_prompt, 
    document_grade_prompt, 
    hallucination_grade_prompt, 
    answer_grade_prompt,
    rewrite_prompt,
)
import hashlib
from django.conf import settings

    
# 벡터 DB 설정해야함.
# gpt-4-turbo, gpt-4o-realtime-preview, gpt-4o-mini, gpt-4o
class BuMeetConfig:
    def __init__(self, model_name='gpt-3.5-turbo-0125'):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.embed_model = OpenAIEmbeddings()
        # self.vectorstores = {}
        # self.retrievers = {}    
        self.vectorstore = None
        self.retriever = None
        self.router = self._init_router()
        self.document_grader = self._init_document_grader()
        self.hallucination_grader = self._init_hallucination_grader()
        self.answer_grader = self._init_answer_grader()
        self.rag_chain = self._init_chain()
        self.question_rewriter = rewrite_prompt | self.llm | StrOutputParser()
        self.web_search_tool = TavilySearchResults(api_key=settings.TAVILY_API_KEY, k=3)
        self.document_hashes = set()  # 이미 추가된 문서의 해시값을 저장
        
    def load_existing_vectorstore(self, persist_directory):
        ''' 이미 저장된 Chroma 벡터스토어에서 데이터를 로드하여 리트리버 초기화 '''
        self.vectorstore = Chroma(
            embedding_function=self.embed_model,
            persist_directory=persist_directory,  # 기존 데이터가 저장된 경로
            collection_name="dive2024"  # 기존에 사용한 컬렉션 이름과 동일해야 합니다.
        )
        
        # 벡터스토어에서 검색을 위한 retriever 설정
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})

    def _calculate_document_hash(self, document_content):
        """ 문서 내용의 해시값을 계산 """
        return hashlib.md5(document_content.encode('utf-8')).hexdigest()

    def add_documents(self, directory_path, category, loader_type=CSVLoader):
        ''' 디렉토리 경로로부터 문서 로드, 벡터스토어에 추가 '''
        loader = DirectoryLoader(
            directory_path, 
            show_progress=True, 
            use_multithreading=True,
            loader_cls=loader_type,
        )  
        new_documents = loader.load()

        # 새로운 문서만 필터링 (기존 벡터스토어에 있는 문서는 제외)
        filtered_documents = []
        for doc in new_documents:
            doc_hash = self._calculate_document_hash(doc.page_content)
            if doc_hash not in self.document_hashes:
                filtered_documents.append(doc)
                self.document_hashes.add(doc_hash)  # 새 문서의 해시 추가

        if not filtered_documents:
            print("모든 문서가 이미 벡터스토어에 존재합니다.")
            return

        # 새로운 문서만 벡터스토어에 추가
        if self.vectorstore:
            self.vectorstore.add_documents(filtered_documents)
        else:
            self.vectorstore = Chroma.from_documents(
                documents=filtered_documents,
                embedding=self.embed_model,
                collection_name=category,
                persist_directory="./chroma_store"
            )

        # 벡터스토어에서 검색을 위한 retriever 업데이트
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
    def _init_router(self):
        ''' 질문을 웹 검색 또는 벡터스토어로 라우팅하는 라우터 초기화 '''
        # 라우팅용 구조화된 출력 설정
        router = self.llm.with_structured_output(RouteQuery)
        question_router = router_prompt | router
        return question_router

    def _init_document_grader(self):
        ''' 검색된 문서에 대한 평가를 위한 grader 초기화 '''
        doc_grader_schema = self.llm.with_structured_output(GradeDocuments)
        retrieval_doc_grader = doc_grader_schema | document_grade_prompt
        return retrieval_doc_grader
    
    def _init_chain(self):
        ''' chain 초기화 '''
        prompt = hub.pull('rlm/rag-prompt')
        rag_chain = prompt | self.llm | StrOutputParser()
        return rag_chain
    
    def _init_hallucination_grader(self):
        ''' 생성한 응답에서 할루시네이션이 발생했는지(응답-문서 비교) 평가하기 위한 grader 초기화 '''
        hallu_grader_schema = self.llm.with_structured_output(GradeHallucinations)
        response_hallucination_grader = hallucination_grade_prompt | hallu_grader_schema
        return response_hallucination_grader
    
    def _init_answer_grader(self):
        ''' 생성한 응답-질문 비교 및 평가하는 grader 초기화 '''
        answer_grader_schema = self.llm.with_structured_output(GradeAnswer)
        answer_question_grader = answer_grade_prompt | answer_grader_schema
        return answer_question_grader
