"""
YOKO Code - 高级终端 UI
参考 Claude Code / Gemini CLI 风格
"""

import os
import sys
import readline
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.live import Live
from rich.spinner import Spinner
from rich.layout import Layout
from rich import box

from src.tools import get_tools, execute_tool
from src.commands import get_commands, execute_command
from src.ai_chat import ask_ai, get_ai_chat


# 配色方案
class Theme:
    PRIMARY = "cyan"
    SECONDARY = "blue"
    ACCENT = "magenta"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR = "red"
    MUTED = "dim white"
    USER = "bold green"
    AI = "bold cyan"
    TOOL = "bold yellow"
    COMMAND = "bold magenta"


class YokoUI:
    """YOKO Code 高级终端界面"""
    
    def __init__(self):
        self.console = Console(highlight=True)
        self.tools = self._load_tools()
        self.commands = self._load_commands()
        self.history = []
        self.session_start = datetime.now()
        self.message_count = 0
        
        self._setup_readline()
    
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
    
    def _setup_readline(self):
        readline.set_completer(self._completer)
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims(' \t\n')
    
    def _completer(self, text, state):
        options = []
        if text.startswith('/'):
            options = ['/' + c for c in self.commands if c.startswith(text[1:])]
        elif text.startswith('!'):
            options = ['!' + t for t in self.tools if t.startswith(text[1:])]
        return options[state] if state < len(options) else None
    
    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_welcome(self):
        """显示欢迎界面"""
        self.clear()
        
        # Logo
        logo = """
[bold cyan]
   ██╗   ██╗ ██████╗ ██╗  ██╗ ██████╗ 
   ╚██╗ ██╔╝██╔═══██╗██║ ██╔╝██╔═══██╗
    ╚████╔╝ ██║   ██║█████╔╝ ██║   ██║
     ╚██╔╝  ██║   ██║██╔═██╗ ██║   ██║
      ██║   ╚██████╔╝██║  ██╗╚██████╔╝
      ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
[/bold cyan]
"""
        self.console.print(logo, justify="center")
        
        # 版本信息
        self.console.print(
            Panel(
                "[bold white]Code[/bold white] [dim]v1.0.0[/dim]",
                subtitle="[dim]坤哥专属 AI 编程助手[/dim]",
                border_style=Theme.PRIMARY,
                padding=(0, 2)
            ),
            justify="center"
        )
        
        # 快速提示
        self.console.print()
        tips = [
            ("💬 对话", "直接输入文字"),
            ("🔧 工具", "!工具名 --参数"),
            ("⚡ 命令", "/命令名"),
            ("🐾 宠物", "/pet"),
            ("❓ 帮助", "/help"),
        ]
        
        tip_panels = []
        for icon, desc in tips:
            tip_panels.append(Panel(
                f"{icon}\n[dim]{desc}[/dim]",
                border_style=Theme.MUTED,
                padding=(0, 1),
                width=16
            ))
        
        self.console.print(Columns(tip_panels, expand=True, equal=True))
        self.console.print()
    
    def show_help(self):
        """显示帮助"""
        self.console.print(Rule("帮助", style=Theme.PRIMARY))
        
        # 命令表
        cmd_table = Table(
            show_header=True,
            header_style=f"bold {Theme.PRIMARY}",
            box=box.SIMPLE_HEAVY,
            padding=(0, 2)
        )
        cmd_table.add_column("命令", style=Theme.COMMAND, width=15)
        cmd_table.add_column("说明", style="white")
        
        cmd_table.add_row("/help", "显示帮助")
        cmd_table.add_row("/tools", "查看工具列表")
        cmd_table.add_row("/commands", "查看命令列表")
        cmd_table.add_row("/status", "查看状态")
        cmd_table.add_row("/clear", "清屏")
        cmd_table.add_row("/pet", "宠物系统")
        cmd_table.add_row("/exit", "退出")
        
        self.console.print(cmd_table)
        self.console.print()
    
    def show_tools(self):
        """显示工具"""
        self.console.print(Rule("工具列表", style=Theme.PRIMARY))
        
        table = Table(
            show_header=True,
            header_style=f"bold {Theme.PRIMARY}",
            box=box.SIMPLE_HEAVY,
            padding=(0, 1)
        )
        table.add_column("工具", style=Theme.TOOL, width=20)
        table.add_column("说明", style="white")
        
        for name, tool in list(self.tools.items())[:20]:
            desc = tool.get('description', '') if isinstance(tool, dict) else ''
            table.add_row(f"!{name}", desc[:40] if desc else '')
        
        if len(self.tools) > 20:
            table.add_row("[dim]...[/dim]", f"[dim]还有 {len(self.tools)-20} 个[/dim]")
        
        self.console.print(table)
        self.console.print()
    
    def show_commands(self):
        """显示命令"""
        self.console.print(Rule("命令列表", style=Theme.PRIMARY))
        
        # 只显示真正实现的命令
        table = Table(
            show_header=True,
            header_style=f"bold {Theme.PRIMARY}",
            box=box.SIMPLE_HEAVY,
            padding=(0, 1)
        )
        table.add_column("命令", style=Theme.COMMAND, width=15)
        table.add_column("缩写", style=Theme.MUTED, width=8)
        table.add_column("说明", style="white")
        
        table.add_row("/help", "/h", "显示帮助")
        table.add_row("/tools", "/t", "查看工具列表")
        table.add_row("/commands", "/cmds", "查看命令列表")
        table.add_row("/status", "/s", "查看状态")
        table.add_row("/version", "/v", "版本信息")
        table.add_row("/model", "/m", "切换模型")
        table.add_row("/clear", "/cls", "清屏")
        table.add_row("/exit", "/q", "退出")
        
        table.add_row()
        table.add_row("[bold magenta]宠物系统[/bold magenta]", "", "")
        table.add_row("/pet", "", "查看宠物状态")
        table.add_row("/pet adopt", "", "领养宠物 [物种] [名字]")
        table.add_row("/pet feed", "", "喂食")
        table.add_row("/pet play", "", "玩耍")
        table.add_row("/pet train", "", "训练")
        table.add_row("/pet rest", "", "休息")
        table.add_row("/pet skills", "", "查看技能")
        table.add_row("/pet help", "", "让宠物帮忙 [任务]")
        
        self.console.print(table)
        self.console.print()
    
    def show_status(self):
        """显示状态"""
        ai_status = "[bold green]●[/bold green] 已连接" if get_ai_chat().is_available() else "[bold red]●[/bold red] 未配置"
        
        # 计算运行时间
        elapsed = datetime.now() - self.session_start
        minutes = int(elapsed.total_seconds() / 60)
        
        status_panel = Panel(
            f"""
[bold {Theme.PRIMARY}]YOKO Code[/bold {Theme.PRIMARY}] [dim]v1.0.0[/dim]

  [bold]状态[/bold]
  ├── AI 对话    {ai_status}
  ├── 工具数量   [cyan]{len(self.tools)}[/cyan]
  ├── 命令数量   [cyan]{len(self.commands)}[/cyan]
  ├── 消息数量   [cyan]{self.message_count}[/cyan]
  └── 运行时间   [cyan]{minutes}[/cyan] 分钟

  [bold]快捷键[/bold]
  ├── Tab        自动补全
  ├── Ctrl+C     中断
  └── Ctrl+D     退出
""",
            title="📊 状态",
            border_style=Theme.PRIMARY,
            padding=(1, 2)
        )
        
        self.console.print(status_panel)
        self.console.print()
    
    def show_pet_status(self):
        """显示宠物状态"""
        try:
            from src.pet import get_pet_manager
            manager = get_pet_manager()
            pet = manager.get_active_pet()
            
            if not pet:
                self.console.print(Panel(
                    "[yellow]还没有宠物，快去领养一只吧！[/yellow]\n\n"
                    "[dim]领养: /pet adopt <物种> <名字>[/dim]",
                    title="🐾 宠物",
                    border_style=Theme.ACCENT
                ))
                return
            
            pet.update_status()
            
            # 状态条
            hunger_bar = self._make_bar(pet.hunger)
            happy_bar = self._make_bar(pet.happiness)
            energy_bar = self._make_bar(pet.energy)
            
            # 稀有度颜色
            rarity_colors = {
                'common': 'white',
                'rare': 'blue',
                'epic': 'magenta',
                'legendary': 'yellow'
            }
            rarity_color = rarity_colors.get(pet.rarity, 'white')
            
            shiny = " ✨" if pet.shiny else ""
            
            pet_panel = Panel(
                f"""
{pet.emoji} [bold {rarity_color}]{pet.name}[/bold {rarity_color}] {shiny} [dim]Lv.{pet.level}[/dim]

  饱食度  {hunger_bar} {int(pet.hunger):>3}%
  快乐度  {happy_bar} {int(pet.happiness):>3}%
  精力    {energy_bar} {int(pet.energy):>3}%

  [dim]经验: {pet.exp}/{pet.level * 100}  |  任务: {pet.tasks_completed}[/dim]
""",
                title=f"🐾 {pet.emoji} {pet.name}",
                border_style=rarity_color,
                padding=(1, 2)
            )
            
            self.console.print(pet_panel)
        
        except Exception as e:
            self.console.print(f"[red]❌ {e}[/red]")
        
        self.console.print()
    
    def _make_bar(self, value, length=15):
        filled = int(value / 100 * length)
        empty = length - filled
        if value > 60:
            return f"[green]{'█' * filled}[/green][dim]{'░' * empty}[/dim]"
        elif value > 30:
            return f"[yellow]{'█' * filled}[/yellow][dim]{'░' * empty}[/dim]"
        else:
            return f"[red]{'█' * filled}[/red][dim]{'░' * empty}[/dim]"
    
    def handle_pet(self, args):
        try:
            from src.pet_commands import cmd_pet
            result = cmd_pet(args)
            self.console.print(result)
        except ImportError:
            self.console.print("[red]❌ 宠物系统未加载[/red]")
    
    def show_model(self, args=None):
        """显示/切换模型"""
        from src.api_config import get_model
        import requests
        
        current = get_model()
        
        if args and len(args) > 0:
            # 切换模型
            new_model = args[0]
            
            # 更新 .env 文件
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
            try:
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                with open(env_path, 'w') as f:
                    for line in lines:
                        if line.startswith('OPENROUTER_MODEL='):
                            f.write(f'OPENROUTER_MODEL={new_model}\n')
                        else:
                            f.write(line)
                
                self.console.print(Panel(
                    f"[green]✅ 已切换到:[/green] [cyan]{new_model}[/cyan]\n\n"
                    "[dim]重启 YOKO Code 后生效[/dim]",
                    title="🔄 切换模型",
                    border_style=Theme.PRIMARY
                ))
            except Exception as e:
                self.console.print(f"[red]❌ 切换失败: {e}[/red]")
        else:
            # 显示当前模型和可用模型
            model_panel = Panel(
                f"[bold]当前模型:[/bold] [cyan]{current}[/cyan]\n\n"
                "[bold]切换命令:[/bold]\n"
                "  /model <模型名>    切换模型\n\n"
                "[bold]推荐免费模型:[/bold]\n"
                "  [green]qwen/qwen3.6-plus:free[/green]          最强免费\n"
                "  qwen/qwen3.6-plus-preview:free  Preview\n"
                "  minimax/minimax-m2.5:free       MiniMax\n"
                "  stepfun/step-3.5-flash:free     阶跃星辰\n"
                "  openai/gpt-oss-120b:free        OpenAI开源",
                title="🧠 模型管理",
                border_style=Theme.PRIMARY,
                padding=(1, 2)
            )
            
            self.console.print(model_panel)
    
    def handle_command(self, user_input):
        parts = user_input.split()
        cmd = parts[0][1:]
        args = parts[1:] if len(parts) > 1 else []
        
        # 只处理真正实现的命令
        handlers = {
            'help': self.show_help,
            'h': self.show_help,
            '?': self.show_help,
            'tools': self.show_tools,
            't': self.show_tools,
            'commands': self.show_commands,
            'cmds': self.show_commands,
            'status': self.show_status,
            'stats': self.show_status,
            's': self.show_status,
            'clear': self.clear,
            'cls': self.clear,
            'pet': lambda: self.show_pet_status() if not args else self.handle_pet(args),
            'version': lambda: self.console.print("[cyan]YOKO Code v1.0.0[/cyan]"),
            'v': lambda: self.console.print("[cyan]YOKO Code v1.0.0[/cyan]"),
            'model': lambda: self.show_model(args),
            'm': lambda: self.show_model(args),
            'exit': lambda: (self.console.print("\n[bold cyan]👋 再见坤哥！[/bold cyan]"), sys.exit(0)),
            'quit': lambda: (self.console.print("\n[bold cyan]👋 再见坤哥！[/bold cyan]"), sys.exit(0)),
            'q': lambda: (self.console.print("\n[bold cyan]👋 再见坤哥！[/bold cyan]"), sys.exit(0)),
        }
        
        if cmd in handlers:
            handlers[cmd]()
        else:
            self.console.print(f"[red]❌ 未知命令: /{cmd}[/red]")
            self.console.print("[dim]输入 /help 查看可用命令[/dim]")
    
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
            with self.console.status(f"[bold {Theme.TOOL}]执行中...[/bold {Theme.TOOL}]"):
                result = execute_tool(tool_name, params)
            self.console.print(Panel(result, border_style=Theme.TOOL))
        else:
            self.console.print(f"[red]❌ 未知工具: !{tool_name}[/red]")
    
    def handle_chat(self, user_input):
        ai = get_ai_chat()
        self.message_count += 1
        
        if ai.is_available():
            # 显示用户消息
            self.console.print()
            self.console.print(f"[{Theme.USER}]坤哥[/{Theme.USER}]", end=" ")
            self.console.print(f"[dim]{user_input}[/dim]")
            self.console.print()
            
            # AI 思考动画
            with self.console.status(f"[bold {Theme.AI}]💭 思考中...[/bold {Theme.AI}]"):
                response = ask_ai(user_input)
            
            # 显示 AI 响应
            if '```' in response:
                self.console.print(Markdown(response))
            else:
                self.console.print(Panel(
                    Markdown(response),
                    border_style=Theme.AI,
                    padding=(1, 2),
                    title=f"[{Theme.AI}]YOKO[/{Theme.AI}]",
                    title_align="left"
                ))
            
            self.console.print()
        else:
            self.console.print(Panel(
                "[yellow]未配置 API Key，无法使用 AI 对话[/yellow]\n\n"
                "[dim]请设置: export OPENROUTER_API_KEY='你的key'[/dim]",
                border_style=Theme.WARNING
            ))
    
    def get_input(self):
        """获取用户输入"""
        try:
            # 自定义提示符
            prompt = Text()
            prompt.append("坤哥 ", style=Theme.USER)
            prompt.append("❯", style=Theme.PRIMARY)
            prompt.append(" ", style="white")
            
            return self.console.input(prompt)
        except KeyboardInterrupt:
            raise
        except EOFError:
            raise
    
    def run(self):
        """运行 UI"""
        self.show_welcome()
        
        while True:
            try:
                user_input = self.get_input().strip()
                
                if not user_input:
                    continue
                
                self.history.append(user_input)
                
                if user_input.startswith('/'):
                    self.handle_command(user_input)
                elif user_input.startswith('!'):
                    self.handle_tool(user_input)
                else:
                    self.handle_chat(user_input)
            
            except KeyboardInterrupt:
                self.console.print("\n[dim]输入 /exit 退出[/dim]\n")
            except EOFError:
                self.console.print("\n\n[bold cyan]👋 再见坤哥！[/bold cyan]")
                break
            except Exception as e:
                self.console.print(f"\n[red]❌ {e}[/red]\n")


def main():
    ui = YokoUI()
    ui.run()


if __name__ == '__main__':
    main()
