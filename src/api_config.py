"""
YOKO Code - API 配置
"""

import os

# API 配置
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'qwen/qwen3.6-plus-preview:free')

def get_api_key():
    """获取 API Key"""
    return OPENROUTER_API_KEY

def get_model():
    """获取模型名称"""
    return OPENROUTER_MODEL

def is_api_configured():
    """检查 API 是否已配置"""
    return bool(OPENROUTER_API_KEY)
