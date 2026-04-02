# YOKO Code

<p align="center">
  <strong>🚀 坤哥专属的 AI 编程助手 🚀</strong>
</p>

<p align="center">
  基于 Claude Code 架构的干净重写版本
</p>

---

## 📖 简介

YOKO Code 是一个 AI 驱动的编程助手，参考了 Claude Code 的架构设计，采用 Python 实现。拥有美颜终端界面、AI 智能对话、电子宠物系统等特色功能。

## ✨ 功能特性

- 🧠 **AI 智能对话** - OpenRouter 驱动，支持多种模型
- 💻 **美颜终端界面** - 参考 Claude Code / Gemini CLI 风格
- 🐾 **电子宠物系统** - 8种物种、稀有度、技能、任务帮忙
- 🔧 **工具系统** - 读写文件、执行命令、搜索等
- 📊 **状态面板** - 美观的树状结构显示

## 🚀 快速部署

### 方法 1：克隆安装

```bash
# 克隆仓库
git clone https://github.com/akun555/yoko-code.git
cd yoko-code

# 安装依赖
pip install rich requests

# 配置 API Key
cat > .env << 'EOF'
OPENROUTER_API_KEY=你的key
OPENROUTER_MODEL=qwen/qwen3.6-plus-preview:free
EOF

# 添加到 PATH（可选）
echo 'export PATH="$PATH:$(pwd)"' >> ~/.bashrc
source ~/.bashrc

# 启动
yoko chat
```

### 方法 2：手动配置

```bash
# 1. 下载项目
git clone https://github.com/akun555/yoko-code.git

# 2. 进入目录
cd yoko-code

# 3. 安装依赖
pip install rich requests

# 4. 创建 .env 文件
echo 'OPENROUTER_API_KEY=你的key' > .env

# 5. 给启动脚本加执行权限
chmod +x yoko

# 6. 启动
./yoko chat
```

## 🔑 获取 API Key

1. 访问 [OpenRouter](https://openrouter.ai)
2. 注册/登录账号
3. 进入 [API Keys](https://openrouter.ai/keys) 页面
4. 点击 "Create Key"
5. 复制 Key 并配置到 `.env` 文件

## 🎮 使用方式

```bash
# 启动对话模式
yoko chat

# 在 YOKO Code 中
坤哥 ❯ 你好，帮我写个排序算法    # AI 对话
坤哥 ❯ /help                      # 查看帮助
坤哥 ❯ /status                    # 查看状态
坤哥 ❯ /pet adopt dragon 小火龙   # 领养宠物
坤哥 ❯ !read --path README.md     # 读取文件
坤哥 ❯ /exit                      # 退出
```

## 📋 命令列表

| 命令 | 缩写 | 说明 |
|------|------|------|
| `/help` | `/h` | 显示帮助 |
| `/tools` | `/t` | 查看工具列表 |
| `/commands` | `/cmds` | 查看命令列表 |
| `/status` | `/s` | 查看状态 |
| `/version` | `/v` | 版本信息 |
| `/clear` | `/cls` | 清屏 |
| `/exit` | `/q` | 退出 |

### 🐾 宠物系统

| 命令 | 说明 |
|------|------|
| `/pet` | 查看宠物状态 |
| `/pet adopt [物种] [名字]` | 领养宠物 |
| `/pet feed` | 喂食 |
| `/pet play` | 玩耍 |
| `/pet train` | 训练 |
| `/pet rest` | 休息 |
| `/pet skills` | 查看技能 |
| `/pet help [任务]` | 让宠物帮忙 |

## 🐾 宠物物种

| 物种 | 名称 | 稀有度 | 技能 |
|------|------|--------|------|
| 🐱 | 猫咪 | 普通 | debug |
| 🐶 | 狗狗 | 普通 | code_review |
| 🐰 | 兔子 | 普通 | refactoring |
| 🐺 | 狼 | 稀有 | architecture |
| 🦊 | 狐狸 | 稀有 | security_audit |
| 🦄 | 独角兽 | 史诗 | ai_suggest |
| 🐉 | 龙 | 史诗 | auto_fix |
| 🐼 | 熊猫 | 传说 | translation |

## 📁 项目结构

```
yoko-code/
├── yoko                  # 启动脚本
├── .env                  # API Key（不提交到 Git）
├── .gitignore            # Git 忽略文件
├── src/
│   ├── ui.py            # 美颜终端界面
│   ├── ai_chat.py       # AI 对话模块
│   ├── api_config.py    # API 配置
│   ├── pet.py           # 宠物系统
│   ├── pet_commands.py  # 宠物命令
│   ├── tools.py         # 工具系统
│   ├── commands.py      # 命令系统
│   └── ...
├── rust/                 # Rust 版本（开发中）
└── tests/               # 测试
```

## ⚙️ 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENROUTER_API_KEY` | OpenRouter API Key | 必填 |
| `OPENROUTER_MODEL` | 使用的模型 | `qwen/qwen3.6-plus-preview:free` |

## 🔒 安全提示

- ⚠️ **永远不要**把 API Key 提交到 GitHub
- ✅ 使用 `.env` 文件存储 Key
- ✅ 确保 `.gitignore` 包含 `.env`
- ✅ 公开仓库务必检查敏感信息

## 🛠️ 依赖

- Python 3.8+
- rich
- requests

## 📚 参考

- Claude Code 官方架构
- Claw Code 干净重写版
- OpenRouter API

## 📄 许可证

MIT License

---

**YOKO Code** - 坤哥专属的 AI 编程助手 💪
