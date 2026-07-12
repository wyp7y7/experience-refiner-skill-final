"""
AI经历提炼器 - 接入豆包 API 版本
用法：python refine_experience.py "帮师姐整理了3年Excel数据"
"""

import sys
import json
import requests

# ===== 请填写你的 API 信息 =====
API_KEY = "ark-2e117a64-5f75-49cf-affe-4b8aef1325e1-e4092"
ENDPOINT_ID = "ep-20260712130311-cwrgt"
# ================================

def call_doubao(prompt):
    """调用豆包 API"""
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": ENDPOINT_ID,
        "messages": [
            {"role": "system", "content": "你是一个专业的简历顾问，擅长用STAR法则提炼经历。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    if response.status_code != 200:
        return f"API调用失败：{response.status_code} - {response.text}"
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

def refine_experience(raw_text):
    """输入大白话经历，调用豆包 API 提炼 STAR 格式"""
    prompt = f"""
请将下面这段经历提炼成 STAR 格式，并自动标记能力标签。

经历描述：
{raw_text}

请按以下格式输出：

标题：[一句话总结经历]

**Situation（情境）**：当时面临什么情况？
**Task（任务）**：你的具体任务是什么？
**Action（行动）**：你具体做了什么？
**Result（结果）**：带来了什么成果？（尽量用数据）

**能力标签**：标签1、标签2、标签3
"""
    
    return call_doubao(prompt)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        raw = input("请用大白话描述你的经历：")
    
    print("\n" + "="*50)
    print("✨ AI 正在提炼你的经历...")
    print("="*50 + "\n")
    
    result = refine_experience(raw)
    print(result)