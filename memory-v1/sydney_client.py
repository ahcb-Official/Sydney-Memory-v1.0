from openai import OpenAI
import httpx

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",

    timeout=30.0,
    max_retries=0,

    http_client=httpx.Client(
        trust_env=False
    )
)


def chat(messages):

    response = client.chat.completions.create(
        model="uncategorized",
        messages=messages,
        temperature=0.8,
        stop=[
            "### Instruction:",
            "### Response:",
            "### Reply:",
            "Instruction###"
        ]
    )

    return response.choices[0].message.content
