from langchain_core.prompts import ChatPromptTemplate


# 에이전트 라우터 프롬프트
router_system = """You are an expert who directs user questions to the Vector Store or web search. 

The Vector Store contains articles and data about the following topics related to the Busan Subway:
- ATMs in Busan Subway (Location and Contact Information)
- Bicycle storage (location and number of stations)
- Information on cultural facilities (library, historical artifacts, VR, reading seats) in subway stations
- Elevators in subway stations (locations and door numbers)
- Escalators in Subway Stations (Locations and Exit Numbers)
- Busan Subway basic information and number of amenities
- Information on nursing rooms in Busan Subway Stations (nearby exit number, detailed location, number of cots, number of sofas, number of microwaves, and number of simple washing machines)
- Lockers in subway stations (locations, fees, and number)
- Name, contact information, address, subway station name, and exit number of tourist attractions near Busan Subway
- Information on restaurants near Busan Subway (name of nearby station, restaurant phone number, address, representative menu, etc.)
- Location of cell phone charging stations on Busan Subway, usage fee, station name, etc.
- Location of restrooms in Busan Subway stations, nearby exit numbers, restroom classification information, etc.
- Menu details of restaurants near 7 major beaches in Busan, including specialties, prices, and restaurant names
- Menu details (specialties, prices, etc.) of restaurants near 7 major beaches in Busan
- Rating information for 7 major beaches in Busan
- Service information of restaurants near 7 major beaches in Busan (parking, playground, pets, reservation, delivery, etc.)
- Busan tourism accommodation information
- Busan Tourism Information on water leisure, sports, parks, and related businesses and spaces
- Busan Food Theme Street Restaurant and Menu Details
- Busan Food Theme Street Restaurant and Menu Information
- Busan Food Theme Street Restaurant Rating Information
- Detailed information such as location, phone number, and introduction of Busan food theme street restaurants
- Busan Food Theme Street restaurant options (Wi-Fi, pet friendly, etc.)
- Busan Marine Healing related business information
- Busan marine tourism related information such as accommodation, village, space, etc.
- Busan cultural life related business information
- Busan tourism transportation-related business information (bus stops, etc.)
- Business information related to Busan tourism food and snack business
- Busan tourism marine recreation related business information

For questions related to these topics, use the Vector Store to retrieve the information. 

For any other questions that are unrelated to these topics, use web search."""
router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", router_system),
        ("human", "{question}"),
    ]
)

# 검색된 문서에 대한 평가를 위한 프롬프트
document_system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
document_grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", document_system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

# 생성한 응답에서 할루시네이션이 발생했는지 평가하기 위한 프롬프트
response_system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
hallucination_grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", response_system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

# 생성한 응답과 질문에 적합한 대답을 하였는지 평가하기 위한 프롬프트
answer_system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
answer_grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", answer_system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

# 사용자 질문을 재구성하기 위한 프롬프트
rewrite_system = """You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewrite_system),
        (
            "human",
            "Here is the initial question: \n\n {question} \n Formulate an improved question.",
        ),
    ]
)