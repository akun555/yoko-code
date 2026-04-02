# YOKO Code

<p align="center">
  <strong>🚀 坤哥专属的 AI 编程助手 🚀</strong>
</p>

<p align="center">
  基于 Claude Code 架构的干净重写版本
</p>

---

## 📖 简介

YOKO Code 是一个 AI 驱动的编程助手，参考了 Claude Code 的架构设计，采用 Python 实现。

## ✨ 功能特性

- **智能对话** - 与 AI 进行自然语言交互
- **代码编辑** - 读取、写入、搜索、替换文件
- **命令执行** - 安全地执行 Shell 命令
- **Git 集成** - Git 状态查看、差异比较
- **插件系统** - 可扩展的插件架构
- **权限系统** - 安全的权限控制
- **Hook 系统** - 事件拦截和自动化

## 🚀 快速开始

```bash
# 查看帮助
python3 -m src.main --help

# 查看工具列表
python3 -m src.main tools

# 查看命令列表
python3 -m src.main commands

# 运行对话循环
python3 -m src.main turn-loop "你好"
```

## 📁 项目结构

```
yoko-code/
├── src/                    # Python 源码
│   ├── main.py            # 主入口
│   ├── tools.py           # 工具系统
│   ├── commands.py        # 命令系统
│   ├── permissions.py     # 权限系统
│   ├── hooks.py           # Hook 系统
│   └── ...
├── rust/                   # Rust 重写版（开发中）
├── tests/                  # 测试
└── README.md              # 项目文档
```

## 🛠️ 工具列表

| 工具 | 描述 |
|------|------|
| `read` | 读取文件内容 |
| `write` | 写入文件内容 |
| `exec` | 执行 Shell 命令 |
| `list` | 列出文件和目录 |
| `search` | 搜索文件内容 |
| `replace` | 替换文件内容 |

## ⚡ 命令列表

| 命令 | 描述 |
|------|------|
| `/help` | 显示帮助信息 |
| `/tools` | 列出可用工具 |
| `/status` | 显示状态信息 |
| `/clear` | 清屏 |
| `/exit` | 退出程序 |

## 🔐 安全特性

- **权限控制** - 基于角色的权限管理
- **命令验证** - 危险命令检测和阻止
- **路径保护** - 受保护路径检查
- **Hook 拦截** - 事件拦截和审计

## 📚 参考

本项目参考了以下资源：
- Claude Code 官方仓库
- Claw Code 干净重写版
- 社区讨论和分析

## 📄 许可证

MIT License

---

**YOKO Code** - 坤哥专属的 AI 编程助手 💪
