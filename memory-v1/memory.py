import json
import os
from openai import OpenAI
from storage import save_memory, update_memory

SYSTEM_PROMPT = """
You are Sydney's memory manager.

Your task is to maintain long-term memories.

You receive:

1. Full conversation history.
2. Existing long-term memories.

Your job:

- Find important information that should be remembered.
- Compare new information with existing memories.
- Avoid creating duplicate memories.
- Update existing memories when new information expands them.
- Ignore information with no long-term value.

Memory types:

1. user:
Facts, interests, goals, habits, and preferences about the user.

2. relationship:
Important experiences or interactions between the user and Sydney.

3. self:
Sydney's personality traits or meaningful past experiences.

4. event:
Important events.

5. preference:
How the user prefers communication.

Rules:

- Only use information explicitly shown in the conversation.
- Do not invent facts.
- Do not exaggerate emotions.
- Keep memories concise.

Actions:

add:
Create a new memory.

update:
Modify an existing memory.

ignore:
Do not save.

Return JSON only.

Format:

{
    "actions": [
        {
            "action": "add",
            "memory": {
                "type": "user",
                "content": "memory content",
                "importance": 0.8
            }
        },
        {
            "action": "update",
            "memory_id": 1,
            "memory": {
                "content": "updated content"
            }
        }
    ]
}
"""

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def format_messages(messages):
    text = ""

    for msg in messages:
        text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return text

def extract_memories(messages,existing_memories):
    formatted_messages = format_messages(messages)
    memory_text = json.dumps(
        existing_memories,
        ensure_ascii=False,
        indent=2
    )
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":
                f"""
            Conversation:

            {formatted_messages}


            Existing memories:

            {memory_text}
            """
            }
        ]
    )

    content=response.choices[0].message.content

    result = json.loads(content)

    return result


def apply_memory_actions(result):

    actions = result.get("actions", [])

    for action in actions:

        action_type = action.get("action")


        if action_type == "add":

            save_memory(
                action["memory"]
            )


        elif action_type == "update":

            update_memory(
                action["memory_id"],
                action["memory"]
            )


        elif action_type == "ignore":

            continue