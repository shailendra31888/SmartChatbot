from fastapi import APIRouter
from app.models.chatbot_schema import ChatRequest, ChatResponse
from app.pipeline.graph import app as langgraph_app  # LangGraph app to process input

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle the chatbot request."""
    
    # Input is taken from the request body, validated by Pydantic
    user_input = request.input

    # Process the input using the LangGraph pipeline
    state = langgraph_app.process({"input": user_input})
    
    # Extract the response and category
    chatbot_response = state["response"]
    category = state.get("category", None)
    
    # Return the response following the ChatResponse schema
    return ChatResponse(response=chatbot_response, category=category)
