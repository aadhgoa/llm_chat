# The line `from fastapi import FastAPI, HTTPException` is importing the `FastAPI` class and the
# `HTTPException` class from the `fastapi` module.
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain.llms import AI21
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

AI21_API_KEY = os.getenv("AI21_API_KEY")

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class QuestionRequest(BaseModel):
    question: str


memory = ConversationBufferMemory(memory_key="chat_history")

@app.post("/chat")
async def chat_endpoint(question_request: QuestionRequest):
    template = """You have access to a vast knowledge base. Your task is to answer a wide range of questions with accurate and concise information.
    {chat_history}
    Human: {question}
    AI:
    """
    prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)

    llm = AI21(ai21_api_key=AI21_API_KEY)

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True,
        memory=memory,
    )

    result = llm_chain.predict(question=question_request.question)
    return {"response": result}

# This is a basic example structure to create a FastAPI backend endpoint '/chat'
# It sets up a POST endpoint to receive questions and returns AI-generated responses




@app.get("/clear-memory")
async def clear_memory():
    global memory  # Use the memory defined outside the function

    # Clear the memory
    memory.clear()
    
    return {"message": "Memory cleared successfully."}

def main():
    # This function is called when running this script directly
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    import uvicorn
    main()