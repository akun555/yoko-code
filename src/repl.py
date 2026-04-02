"""
YOKO Code - 交互式 REPL (美颜版)
"""

import os
import sys
import readline
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint
from rich.syntax import Syntax

from src.tools import get_tools, execute_tool
from src.commands import get_commands, execute_command
from src.ai_chat import ask_ai, get_ai_chat


class YokoREPL:
    """YOKO Code 交互式环境"""
    
    def __init__(self):
        self.console = Console()
        self.tools = self._load_tools()
        self.commands = self._load_commands()
        self.history = []
        self._setup_completer()
    
    def _load_tools(self):
        try:
            tools = get_tools()
            if isinstance(tools, tuple):
                return {t.name: {'description': t.responsibility} for t in tools if hasattr(t, 'name')}
            return tools
        except:
            return {}
    
    def _load_commands(self):
        try:
            commands = get_commands()
            if isinstance(commands, tuple):
                return {c.name: {'description': c.responsibility} for c in commands if hasattr(c, 'name')}
            return commands
        except:
            return {}
    
    def _setup_completer(self):
        readline.set_completer(self._completer)
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims(' \t\n')
    
    def _completer(self, text, state):
        options = []
        if text.startswith('/'):
            options = ['/' + c for c in self.commands if c.startswith(text[1:])]
        elif text.startswith('!'):
            options = ['!' + t for t in self.tools if t.startswith(text[1:])]
        else:
            options = ['/help', '/tools', '/commands', '/status', '/clear', '/exit', '/pet']
        return options[state] if state < len(options) else None
    
    def show_banner(self):
        self.console.print()
        self.console.print(Panel.fit(
            "[bold yellow]🚀 YOKO Code[/bold yellow] [dim]v1.0[/dim]\n"
            "[bold cyan]坤哥专属 AI 编程助手[/bold cyan]",
            border_style="cyan",
            padding=(1, 4)
        ))
        self.console.print()
        self.console.print("[dim]输入 [bold]/help[/bold] 查看帮助  •  按 [bold]Tab[/bold] 自动补全  •  直接输入对话[/dim]", justify="center")
        self.console.print()
    
    def show_help(self):
        table = Table(title="📖 YOKO Code 帮助", show_header=False, border_style="cyan")
        table.add_column("类型", style="yellow", width=12)
        table.add_column("命令", style="green", width=25)
        table.add_column("说明", style="white")
        
        table.add_row("命令", "/help", "显示帮助")
        table.add_row("", "/tools", "查看工具")
        table.add_row("", "/commands", "查看命令")
        table.add_row("", "/status", "状态信息")
        table.add_row("", "/clear", "清屏")
        table.add_row("", "/exit", "退出")
        table.add_row("", "/pet", "宠物系统")
        table.add_row()
        table.add_row("工具", "!read --path <文件>", "读取文件")
        table.add_row("", "!write --path <文件> --content <内容>", "写入文件")
        table.add_row("", "!exec --command <命令>", "执行命令")
        table.add_row("", "!list --path <目录>", "列出文件")
        table.add_row("", "!search --pattern <模式>", "搜索内容")
        table.add_row()
        table.add_row("AI", "直接输入文字", "AI 智能对话")
        
        self.console.print(table)
        self.console.print()
    
    def show_tools(self):
        table = Table(title=f"📦 可用工具 ({len(self.tools)} 个)", border_style="cyan")
        table.add_column("命令", style="green", width=25)
        table.add_column("描述", style="white")
        
        for name, tool in list(self.tools.items())[:15]:
            desc = tool.get('description', '') if isinstance(tool, dict) else ''
            table.add_row(f"!{name}", desc[:50] if desc else '')
        
        if len(self.tools) > 15:
            table.add_row("[dim]...[/dim]", f"[dim]还有 {len(self.tools)-15} 个工具[/dim]")
        
        self.console.print(table)
        self.console.print()
    
    def show_commands(self):
        table = Table(title=f"⚡ 可用命令 ({len(self.commands)} 个)", border_style="cyan")
        table.add_column("命令", style="green", width=20)
        table.add_column("描述", style="white")
        
        for name, cmd in self.commands.items():
            desc = cmd.get('description', '') if isinstance(cmd, dict) else ''
            table.add_row(f"/{name}", desc[:50] if desc else '')
        
        self.console.print(table)
        self.console.print()
    
    def show_status(self):
        ai_status = "[green]✅ 已配置[/green]" if get_ai_chat().is_available() else "[red]❌ 未配置[/red]"
        
        panel = Panel(
            f"工具数量: [cyan]{len(self.tools)}[/cyan]\n"
            f"命令数量: [cyan]{len(self.commands)}[/cyan]\n"
            f"历史记录: [cyan]{len(self.history)}[/cyan] 条\n"
            f"AI 对话:  {ai_status}",
            title="📊 状态",
            border_style="cyan"
        )
        self.console.print(panel)
        self.console.print()
    
    def handle_pet(self, args):
        try:
            from src.pet_commands import cmd_pet
            result = cmd_pet(args)
            self.console.print(result)
        except ImportError:
            self.console.print("[red]❌ 宠物系统未加载[/red]")
    
    def handle_command(self, user_input):
        parts = user_input.split()
        cmd = parts[0][1:]
        args = parts[1:] if len(parts) > 1 else []
        
        handlers = {
            'help': lambda: self.show_help(),
            'tools': lambda: self.show_tools(),
            'commands': lambda: self.show_commands(),
            'status': lambda: self.show_status(),
            'clear': lambda: os.system('clear' if os.name == 'posix' else 'cls'),
            'exit': lambda: (self.console.print("\n[bold cyan]👋 再见坤哥！[/bold cyan]"), sys.exit(0)),
            'quit': lambda: (self.console.print("\n[bold cyan]👋 再见坤哥！[/bold cyan]"), sys.exit(0)),
            'pet': lambda: self.handle_pet(args),
        }
        
        if cmd in handlers:
            handlers[cmd]()
        elif cmd in self.commands:
            result = self.commands[cmd].get('execute', lambda x: '')(args)
            self.console.print(result)
        else:
            self.console.print(f"[red]❌ 未知命令: /{cmd}[/red]")
            self.console.print("[dim]输入 /help 查看帮助[/dim]")
    
    def handle_tool(self, user_input):
        parts = user_input.split()
        tool_name = parts[0][1:]
        
        params = {}
        i = 1
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                    params[key] = parts[i + 1]
                    i += 2
                else:
                    params[key] = True
                    i += 1
            else:
                i += 1
        
        if tool_name in self.tools:
            result = execute_tool(tool_name, params)
            self.console.print(result)
        else:
            self.console.print(f"[red]❌ 未知工具: !{tool_name}[/red]")
    
    def handle_chat(self, user_input):
        ai = get_ai_chat()
        
        if ai.is_available():
            with self.console.status("[bold cyan]🤔 思考中...[/bold cyan]"):
                response = ask_ai(user_input)
            
            # 检查是否包含代码
            if '```' in response:
                self.console.print()
                self.console.print(Markdown(response))
            else:
                self.console.print()
                self.console.print(Panel(response, border_style="green", padding=(0, 2)))
            self.console.print()
        else:
            self.console.print(f"\n[bold yellow]🤔 我收到了:[/bold yellow] {user_input}")
            self.console.print("[dim]未配置 API Key，输入 /help 查看帮助[/dim]\n")
    
    def handle_input(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return
        
        self.history.append(user_input)
        
        if user_input.startswith('/'):
            self.handle_command(user_input)
        elif user_input.startswith('!'):
            self.handle_tool(user_input)
        else:
            self.handle_chat(user_input)
    
    def run(self):
        self.show_banner()
        
        while True:
            try:
                user_input = Prompt.ask("[bold green]坤哥[/bold green]")
                self.handle_input(user_input)
            except KeyboardInterrupt:
                self.console.print("\n\n[bold cyan]👋 再见坤哥！[/bold cyan]")
                break
            except EOFError:
                self.console.print("\n\n[bold cyan]👋 再见坤哥！[/bold cyan]")
                break
            except Exception as e:
                self.console.print(f"\n[red]❌ 错误: {e}[/red]\n")


def main():
    repl = YokoREPL()
    repl.run()


if __name__ == '__main__':
    main()
