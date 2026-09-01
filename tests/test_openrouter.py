import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Give me a simple chicken pasta recipe for two people."
        }
    ],
    temperature=0.3,
    max_tokens=700,
)

print("=" * 60)
print("MODEL USED")
print("=" * 60)

print(response.model)

print("\n" + "=" * 60)
print("RESPONSE")
print("=" * 60)

print(response.choices[0].message.content)