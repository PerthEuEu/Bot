import os
import requests

# ===== ดึง Token จาก Replit Secrets =====
HUGGINGFACE_API_KEY = os.environ["HF_API_TOKEN"]

def ask_huggingface(prompt):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]['generated_text']
    else:
        return f"เกิดข้อผิดพลาด: {response.status_code}, {response.text}"

print("💬 บอทออนไลน์! พิมพ์ 'ออก' เพื่อหยุด")
while True:
    user_input = input("คุณ: ")
    if user_input.lower() in ["ออก", "exit", "quit"]:
        print("บอท: เจอกันใหม่!")
        break
    bot_reply = ask_huggingface(user_input)
    print("บอท:", bot_reply)
