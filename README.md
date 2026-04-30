# YOKO Code

<p align="center">
  <strong>🚀 坤哥专属的 AI 编程助手 🚀</strong>
</p>

<p align="center">
  Claude Code inspired 的本地编程 Agent 实验项目，当前主实现位于 Rust workspace。
</p>

---

## 项目状态

YOKO Code 目前包含两条实现线：

| 路径 | 角色 | 状态 |
|---|---|---|
| `rust/` | 当前主产品面，包含 CLI、runtime、tools、commands、plugins、LSP 等模块 | 推荐优先使用 |
| `src/` | Python 原型/移植工作区，保存命令与工具 surface 的镜像、审计和辅助 CLI | 可用于验证和参考 |

> 说明：根目录的 `./yoko` 脚本保留为 Python 兼容入口；正式 CLI 建议从 `rust/` 构建运行。

## 功能方向

- AI 编程对话与本地 workspace 辅助
- 文件读写、搜索、Shell 等工具调用能力
- Slash command 命令体系
- 会话、配置、权限与成本统计
- 插件、skills、MCP/LSP 等扩展方向
- Python 端提供 porting/parity 辅助检查

## 快速开始：Rust CLI（推荐）

### 1. 准备环境

需要安装：

- Rust stable toolchain
- Cargo
- 至少一个模型供应商的 API Key

### 2. 配置模型凭据

Anthropic 兼容模型：

```bash
export ANTHROPIC_API_KEY="***"
# 可选：自定义兼容 endpoint
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
```

Grok / xAI：

```bash
export XAI_API_KEY="***"
# 可选
export XAI_BASE_URL="https://api.x.ai"
```

### 3. 构建和运行

```bash
git clone https://github.com/akun555/yoko-code.git
cd yoko-code/rust

# 开发运行
cargo run --bin yoko -- --help
cargo run --bin yoko -- prompt "summarize this workspace"

# 本地安装
cargo install --path crates/claw-cli --locked

yoko --help
```

## Python 兼容入口

Python 入口主要用于原型、移植审计和 legacy UI：

```bash
cd yoko-code
python -m pip install rich requests pytest

# 查看 Python porting workspace 概览
python -m src.main summary

# 运行 Python 测试
python -m pytest -q

# legacy chat UI
cat > .env <<'EOF'
OPENROUTER_API_KEY=***
OPENROUTER_MODEL=qwen/qwen3.6-plus-preview:free
EOF

./yoko chat
```

## 根目录脚本

```bash
./yoko help
./yoko summary
./yoko tools
./yoko commands
./yoko chat
```

`./yoko` 会自动以脚本所在目录作为项目根目录，并加载根目录 `.env`。

## 验证命令

提交前建议运行：

```bash
# Python
python -m compileall -q src tests
python -m pytest -q

# Rust
cd rust
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo build --release
```

## 项目结构

```text
yoko-code/
├── yoko                    # Python 兼容启动脚本
├── src/                    # Python 原型/移植工作区
├── tests/                  # Python 测试
├── rust/                   # Rust 主实现
│   ├── crates/api          # 模型供应商客户端与 streaming
│   ├── crates/runtime      # 会话、配置、权限、runtime loop
│   ├── crates/tools        # 内置工具
│   ├── crates/commands     # Slash command 注册与处理
│   ├── crates/plugins      # 插件发现与生命周期
│   ├── crates/lsp          # LSP 支持
│   └── crates/claw-cli     # `yoko` CLI binary
├── .github/workflows/ci.yml
└── README.md
```

## 环境变量

| 变量 | 用途 |
|---|---|
| `ANTHROPIC_API_KEY` | Rust CLI 的 Anthropic API Key |
| `ANTHROPIC_BASE_URL` | Rust CLI 的 Anthropic 兼容 endpoint，可选 |
| `XAI_API_KEY` | Rust CLI 的 xAI/Grok API Key |
| `XAI_BASE_URL` | Rust CLI 的 xAI/Grok endpoint，可选 |
| `OPENROUTER_API_KEY` | Python legacy chat 入口使用 |
| `OPENROUTER_MODEL` | Python legacy chat 入口使用 |

## 安全提示

- 不要提交 `.env` 或任何 API Key
- 提交前运行测试和格式化检查
- 涉及工具执行、文件写入、Shell 命令时，保持最小权限原则

## License

MIT License，详见 [`LICENSE`](LICENSE)。
