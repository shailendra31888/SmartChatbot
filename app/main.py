from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.graph.smart_agent import app as langgraph_app  # Import the LangGraph app (compiled app)
import os

# Initialize the FastAPI app
app = FastAPI()

# Define the request model for the user input
class QueryRequest(BaseModel):
    input: str

# POST endpoint to interact with the chatbot
@app.post("/chat")
async def chat(request: QueryRequest):
    input_text = request.input

    # Log input (optional, useful for debugging)
    print(f"User Input: {input_text}")

    # Prepare the state for LangGraph agent and call the invoke function
    state = {
        "input": input_text,
        "all_actions": [],
        "response": "",
        "category": "",
    }

    # Run the LangGraph agent with the input state
    result = langgraph_app.invoke(state)

    # Return the response from LangGraph agent
    return {"response": result.get("response", "⚠️ No response generated.")}

# Example route for health check (optional)
@app.get("/health")
async def health_check():
    return {"status": "ok"}

