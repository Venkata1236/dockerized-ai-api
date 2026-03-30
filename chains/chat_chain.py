# chains/chat_chain.py
# LangChain conversation chain
# Concept: Wrap LangChain logic inside a function called by FastAPI

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory


def create_chat_chain(api_key: str, memory: ConversationBufferMemory, temperature: float = 0.7) -> ConversationChain:
    """
    Creates a conversation chain with memory.

    Args:
        api_key    : OpenAI API key
        memory     : session memory
        temperature: response creativity

    Returns:
        ConversationChain ready to use
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        openai_api_key=api_key
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

    return chain


def get_response(chain: ConversationChain, message: str) -> str:
    """
    Gets a response from the chain.

    Args:
        chain  : ConversationChain
        message: user message

    Returns:
        Bot response string
    """
    result = chain.invoke({"input": message})
    return result["response"]