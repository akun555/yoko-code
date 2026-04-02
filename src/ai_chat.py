"""
YOKO Code - AI 对话模块
"""

import os
import json
import requests
from typing import List, Dict, Any

from .api_config import get_api_key, get_model, is_api_configured


class AIChat:
    """AI 对话"""
    
    def __init__(self):
        self.api_key = get_api_key()
        self.model = get_model()
        self.base_url = 'https://openrouter.ai/api/v1'
        self.history = []
    
    def is_available(self) -> bool:
        """检查 AI 是否可用"""
        return is_api_configured()
    
    def chat(self, user_message: str, system_prompt: str = None) -> str:
        """发送对话请求"""
        if not self.is_available():
            return "❌ 未配置 API Key\n\n请设置环境变量:\nexport OPENROUTER_API_KEY='你的key'"
        
        # 构建消息
        messages = []
        
        # 系统提示词
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        else:
            messages.append({
                'role': 'system',
                'content': '''你是 YOKO Code，坤哥专属的 AI 编程助手。

你的能力：
1. 回答编程问题
2. 生成代码
3. 解释代码
4. 调试帮助
5. 架构建议

请用中文回复，简洁明了。'''
            })
        
        # 添加历史
        for msg in self.history[-10:]:
            messages.append(msg)
        
        # 添加当前消息
        messages.append({'role': 'user', 'content': user_message})
        
        # 发送请求
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': messages
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            ai_response = result['choices'][0]['message']['content']
            
            # 记录历史
            self.history.append({'role': 'user', 'content': user_message})
            self.history.append({'role': 'assistant', 'content': ai_response})
            
            return ai_response
        
        except requests.exceptions.RequestException as e:
            return f"❌ API 请求失败: {str(e)}"
        except Exception as e:
            return f"❌ 错误: {str(e)}"


# 全局 AI 对话实例
_ai_chat = None


def get_ai_chat() -> AIChat:
    """获取 AI 对话实例"""
    global _ai_chat
    if _ai_chat is None:
        _ai_chat = AIChat()
    return _ai_chat


def ask_ai(message: str) -> str:
    """向 AI 提问"""
    chat = get_ai_chat()
    return chat.chat(message)
