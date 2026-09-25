from sydney_client import chat
from storage import (
    save_message,
    get_recent_messages,
    get_relevant_memories,
    load_memories
)
from memory import (
    extract_memories,
    apply_memory_actions
)
session_messages = []
print("Welcome to Sydney Memory v1. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":

        print("正在整理本次聊天记忆...")


        existing_memories = load_memories()


        result = extract_memories(
            session_messages,
            existing_memories
        )


        apply_memory_actions(
            result
        )


        print("长期记忆更新完成。")


        break

    save_message("user", user_input)
    session_messages.append(
    {
        "role":"user",
        "content":user_input
    }
    )

    recent_messages = get_recent_messages()
    memories = get_relevant_memories(user_input)
    memory_context = ""

    for memory in memories:
        memory_context += (
            f"- {memory['content']}\n"
        )

    messages=[
        {
            "role":"system",
            "content": 
            "Important memories:\n"
            + memory_context
        }
    ] + recent_messages
    
    
    response_content = chat(messages)
    print(f"Sydney: {response_content}")
    save_message("assistant", response_content)
    session_messages.append(
    {
        "role":"assistant",
        "content":response_content
    }
    )
