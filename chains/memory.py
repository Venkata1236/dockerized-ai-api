# chains/memory.py
# Session memory management — each session_id gets its own history
# Concept: Multiple users can chat simultaneously without mixing histories

from langchain.memory import ConversationBufferMemory
from typing import Dict

# Global dict — stores memory per session_id
_session_memories: Dict[str, ConversationBufferMemory] = {}


def get_memory(session_id: str) -> ConversationBufferMemory:
    """
    Returns memory for a session. Creates new one if doesn't exist.

    Args:
        session_id: unique identifier for the session

    Returns:
        ConversationBufferMemory for that session
    """
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        print(f"✅ New session created: {session_id}")
    return _session_memories[session_id]


def clear_memory(session_id: str) -> bool:
    """
    Clears memory for a specific session.

    Args:
        session_id: session to clear

    Returns:
        True if cleared, False if session not found
    """
    if session_id in _session_memories:
        del _session_memories[session_id]
        print(f"🗑️ Session cleared: {session_id}")
        return True
    return False


def get_active_sessions() -> list:
    """Returns list of all active session IDs."""
    return list(_session_memories.keys())