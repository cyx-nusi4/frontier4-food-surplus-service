# import openai
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

def ask_gpt(prompt):
    return "请稍等，我正在处理你的请求..."
    # try:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     return response.choices[0].message.content.strip()
    # except Exception as e:
    #     return f"❌ GPT 请求失败：{e}"
