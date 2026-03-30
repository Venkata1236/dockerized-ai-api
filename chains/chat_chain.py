# chains/chat_chain.py
# LangChain conversation chain
# Concept: Wrap LangChain logic inside a function called by FastAPI

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

def create_chat_chain(
    api_key: str,
    memory: ConversationBufferMemory,
    temperature: float = 0.7
) -> ConversationChain:
    """
    Creates a conversation chain with memory.
    - model: gpt-3.5-turbo (fast + cheap for demos)
    - verbose=False: suppresses LangChain internal logs
    """
    # Initialize the OpenAI LLM with given settings
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",      # Change to gpt-4 for better responses
        temperature=temperature,     # Higher = more creative, Lower = more factual
        openai_api_key=api_key
    )

    # Attach memory so the chain remembers past messages
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False   # Set True to debug LangChain internals
    )

    return chain

def get_response(chain: ConversationChain, message: str) -> str:
    """
    Gets a response from the chain.
    - chain.invoke() sends message + history to LLM
    - Returns only the "response" string from result dict
    """
    result = chain.invoke({"input": message})
    return result["response"]  # Extract just the text response