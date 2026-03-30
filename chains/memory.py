# chains/memory.py
# Session memory management — each session_id gets its own history
# Concept: Multiple users can chat simultaneously without mixing histories

from langchain.memory import ConversationBufferMemory
from typing import Dict

# Global dict — stores memory per session_id
# Key: session_id (str), Value: ConversationBufferMemory
_session_memories: Dict[str, ConversationBufferMemory] = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    """
    Returns memory for a session. Creates new one if doesn't exist.
    - return_messages=True makes it compatible with ChatModels
    """
    if session_id not in _session_memories:
        # Create fresh memory for new sessions
        _session_memories[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        print(f"✅ New session created: {session_id}")

    return _session_memories[session_id]

def clear_memory(session_id: str) -> bool:
    """
    Clears memory for a specific session.
    - Returns True if session existed and was cleared
    - Returns False if session was not found
    """
    if session_id in _session_memories:
        del _session_memories[session_id]  # Remove from dict entirely
        print(f"🗑️ Session cleared: {session_id}")
        return True

    return False  # Session didn't exist

def get_active_sessions() -> list:
    """Returns list of all active session IDs."""
    return list(_session_memories.keys())