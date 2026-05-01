# YOKO Code

<p align="center">
  <strong>跟 AI 聊天，让它帮你写代码、修 Bug、做重构</strong>
</p>

<p align="center">
  <a href="https://github.com/akun555/yoko-code/actions"><img src="https://github.com/akun555/yoko-code/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/rust-1.80+-orange.svg" alt="Rust">
  <img src="https://img.shields.io/badge/version-0.1.0-lightgrey.svg" alt="Version">
</p>

---

## 这是什么

YOKO Code 是一个运行在**命令行**里的 AI 编程助手。你像聊天一样告诉它想做什么，它就会读你的代码、写新功能、修复 Bug、帮你重构——

```
$ yoko
> 帮我把 src/config.rs 里的硬编码字符串提取到常量文件
> 给 user.rs 的 login 函数加上参数校验
> 这段代码报错了，帮我看看怎么回事
```

## 它能干什么

| 能力 | 说明 |
|------|------|
| 💬 **自然语言编程** | 用日常语言描述需求，AI 理解并执行 |
| 📂 **文件操作** | 读写、搜索、替换项目中的任何文件 |
| 🐚 **Shell 命令** | 在安全沙箱内执行终端命令 |
| 🔍 **代码搜索** | 正则搜索、glob 模式匹配、语义检索 |
| 🌐 **网络访问** | 搜索网页、抓取文档，获取最新信息 |
| 📋 **任务管理** | 自动追踪待办事项，不遗漏任何步骤 |
| 🔌 **插件扩展** | 支持自定义插件、Skills、MCP 协议 |
| 🔒 **权限控制** | 分级权限模型，敏感操作需确认 |

## 快速开始

### 1. 装好 Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 2. 搞一个 API Key

目前支持 Anthropic 和 xAI 的模型。任选一个：

```bash
# Anthropic（Claude）
export ANTHROPIC_API_KEY="sk-ant-..."

# xAI（Grok）
export XAI_API_KEY="xai-..."
```

### 3. 克隆、编译、运行

```bash
git clone https://github.com/akun555/yoko-code.git
cd yoko-code/rust

# 一句话试试
cargo run --bin yoko -- prompt "介绍一下这个项目"

# 交互模式
cargo run --bin yoko
```

### 4. 安装到系统（可选）

```bash
cargo install --path crates/claw-cli --locked
yoko --help
```

## 项目结构

```
yoko-code/
├── rust/                      # 🦀 Rust 主实现
│   ├── crates/api             #   模型供应商客户端
│   ├── crates/runtime         #   会话、权限、执行引擎
│   ├── crates/tools           #   内置工具集
│   ├── crates/commands        #   斜杠命令系统
│   ├── crates/plugins         #   插件框架
│   ├── crates/lsp             #   LSP 语言服务器
│   └── crates/claw-cli        #   yoko 命令行入口
├── src/                       # 🐍 Python 原型（参考用）
├── .github/workflows/         # CI（fmt → clippy → test → build）
└── README.md
```

## 质量保障

每次提交自动在 Ubuntu + macOS 上运行：

- ✅ `cargo fmt --check` — 代码格式统一
- ✅ `cargo clippy -- -D warnings` — 零警告容忍
- ✅ `cargo test --workspace` — 290+ 测试全过
- ✅ `cargo build --release` — 确保可发布

## 安全提示

- `.env` 和 API Key **绝对不要提交到 Git**
- 工具执行遵循最小权限原则
- 敏感操作（Shell、网络）需要交互确认

## License

MIT · 详见 [LICENSE](LICENSE)
