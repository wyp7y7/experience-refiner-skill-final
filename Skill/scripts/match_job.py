"""
岗位匹配器 - 扫描所有经历，匹配目标岗位要求
用法：python match_job.py "数据分析师"
"""

import sys
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
            {"role": "system", "content": "你是一个专业的简历顾问和职业规划师。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    
    if response.status_code != 200:
        return f"API调用失败：{response.status_code}"
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

def match_job(job_title, experiences):
    """匹配目标岗位"""
    exp_text = ""
    for i, exp in enumerate(experiences, 1):
        exp_text += f"\n经历{i}：{exp}"
    
    prompt = f"""
用户有这些经历：
{exp_text}

用户想投的岗位是：{job_title}

请分析每条经历与这个岗位的匹配度，按以下格式输出：

## 匹配报告

### 岗位：{job_title}

### 经历匹配度分析
1. 经历1：[匹配度百分比]%
   分析：[为什么匹配/不匹配]
2. 经历2：[匹配度百分比]%
   分析：[为什么匹配/不匹配]
3. 经历3：[匹配度百分比]%
   分析：[为什么匹配/不匹配]

### 总体匹配度：[XX]%

### 建议
[给用户的具体建议]
"""
    return call_doubao(prompt)

if __name__ == "__main__":
    # 三条真实经历
    experiences = [
        "用WorkBuddy搭建个人知识库系统，设计目录结构，配置AI工作流，实现输入输出闭环",
        "课程中做了多个微信小程序项目，包括生日邀请函、音乐播放器、模拟时钟等，用微信开发者工具完成",
        "小组作业中负责整合大家的报告内容，制作答辩PPT，统一格式和风格"
    ]
    
    if len(sys.argv) > 1:
        job = " ".join(sys.argv[1:])
    else:
        job = input("请输入目标岗位（如：数据分析师）：")
    
    print("\n" + "="*50)
    print(f"🎯 正在匹配岗位：{job}")
    print("="*50 + "\n")
    
    result = match_job(job, experiences)
    print(result)