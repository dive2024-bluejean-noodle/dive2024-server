from django.shortcuts import render
from typing import List
from typing_extensions import TypedDict
from django.http import JsonResponse
from .agent import BuMeetAgent
from .config import BuMeetConfig
from langgraph.graph import END, StateGraph, START
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import os


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """
    question: str
    generation: str
    web_search: str
    documents: List[str]


class ProcessQueryView(APIView):
    #permission_classes = [IsAuthenticated]  # 인증이 필요하다면 주석을 해제하세요.
    """
    Class-based view to process the query using BuMeetAgent and LangGraph workflow.
    """

    def post(self, request, *args, **kwargs):
        """
        POST 요청으로 사용자로부터 질문을 받아서 처리
        """
        # 요청에서 question 추출
        question = request.data.get('question')
        
        # BuMeet 설정 초기화
        config = BuMeetConfig(model_name="gpt-3.5-turbo-0125")

        # 이미 저장된 벡터 디비가 있을 경우 로드 (예시: ./chroma_store)
        config.load_existing_vectorstore(persist_directory='./chroma_store')

        # BuMeet 에이전트 초기화
        agent = BuMeetAgent(config=config)

        # LangGraph 워크플로우 생성
        workflow = StateGraph(state_schema=GraphState)

        # Define the nodes
        workflow.add_node("websearch", agent.web_search)
        workflow.add_node("retrieve", agent.retrieve)
        workflow.add_node("grade_documents", agent.grade_documents)
        workflow.add_node("generate", agent.generate)

        # Build Graph
        workflow.set_conditional_entry_point(
            agent.route_question,
            {
                "websearch": "websearch",
                "vectorstore": "retrieve",
            },
        )

        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            agent.decide_to_generate,
            {
                "websearch": "websearch",
                "generate": "generate",
            },
        )
        workflow.add_edge("websearch", "generate")
        workflow.add_conditional_edges(
            "generate",
            agent.grade_generation_v_documents_and_question,
            {
                "not supported": "websearch",
                "useful": END,
                "not useful": "websearch",
            },
        )

        # Compile workflow
        app = workflow.compile()

        # 입력 데이터를 처리
        inputs = {"question": question}

        # 결과 처리
        results = []
        for output in app.stream(inputs):
            results.append(output)

        # 최종 결과 반환
        # final_generation = results[-1]["generation"] if results else None
        return Response({"results": results[-1]})
        # "final_generation": final_generation,

