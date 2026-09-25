import json
import re
from pathlib import Path
from datetime import datetime
DATA_DIR = Path(__file__).parent / "data"
MESSAGES_FILE = DATA_DIR / "messages.json"
MEMORY_FILE = DATA_DIR / "memories.json"

#message 保存

def load_messages():
    if not MESSAGES_FILE.exists():
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_message(role, content):
    messages=load_messages()
    if messages:
        message_id = messages[-1]["id"] + 1
    else:
        message_id = 1
    message={
        "id": message_id,
        "role": role,
        "content": content
    }
    messages.append(message)
    DATA_DIR.mkdir(exist_ok=True)

    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            messages,
            f,
            ensure_ascii=False,
            indent=2
        )

def get_recent_messages(limit=20):
    messages = load_messages()
    recent=messages[-limit:]
    result=[]
    for msg in recent:
        result.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return result


#memory 保存

def load_memories():
    if not MEMORY_FILE.exists():
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    memories=load_memories()

    if memories:
        memory_id = memories[-1]["id"] + 1
    else:
        memory_id = 1

    memory["id"] = memory_id
    memory["created_at"] = datetime.now().isoformat()

    memories.append(memory)

    DATA_DIR.mkdir(exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memories,
            f,
            ensure_ascii=False,
            indent=2
        )


def _search_terms(text):
    """Extract lightweight search terms that work for Chinese and English."""
    normalized = str(text).lower()
    terms = set(re.findall(r"[a-z0-9_]+", normalized))

    # Chinese has no spaces, so character bigrams provide a useful dependency-free
    # approximation until the project adopts embeddings or a tokenizer.
    for chunk in re.findall(r"[\u4e00-\u9fff]+", normalized):
        if len(chunk) == 1:
            terms.add(chunk)
        else:
            terms.update(chunk[index:index + 2] for index in range(len(chunk) - 1))

    return terms


def _memory_relevance(memory, query_terms):
    memory_terms = _search_terms(memory.get("content", ""))
    if not memory_terms:
        return 0

    overlap = query_terms & memory_terms
    if not overlap:
        return 0

    # Recall matters more than memory length: a memory is useful when it covers a
    # meaningful portion of what the user is currently talking about.
    lexical_score = len(overlap) / len(query_terms)
    importance = memory.get("importance", 0.5)
    if not isinstance(importance, (int, float)):
        importance = 0.5

    return lexical_score * (0.75 + 0.25 * max(0, min(importance, 1)))


def get_relevant_memories(query, limit=10):
    memories = load_memories()
    query_terms = _search_terms(query)
    if not query_terms:
        return []

    ranked = []
    for memory in memories:
        score = _memory_relevance(memory, query_terms)
        if score > 0:
            ranked.append((score, memory.get("id", 0), memory))

    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [memory for _, _, memory in ranked[:limit]]


def update_memory(memory_id, new_memory):

    memories = load_memories()

    for memory in memories:

        if memory["id"] == memory_id:

            memory.update(new_memory)

            memory["updated_at"] = datetime.now().isoformat()

            break


    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memories,
            f,
            ensure_ascii=False,
            indent=2
        )
