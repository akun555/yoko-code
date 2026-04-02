"""
YOKO Code - 宠物命令
"""

from typing import List
from .pet import get_pet_manager, SPECIES


def cmd_pet(args: List[str]) -> str:
    """宠物命令"""
    manager = get_pet_manager()
    
    if not args:
        return """
🐾 YOKO Pet - 坤哥的电子宠物

用法:
  /pet adopt [物种] [名字]  - 领养宠物
  /pet list                 - 查看所有宠物
  /pet status               - 查看当前宠物状态
  /pet feed                 - 喂食
  /pet play                 - 玩耍
  /pet train                - 训练
  /pet rest                 - 休息
  /pet switch <宠物ID>      - 切换宠物
  /pet release <宠物ID>     - 放生宠物
  /pet species              - 查看可选物种
  /pet help <任务类型>      - 让宠物帮忙

任务类型:
  code_review - 代码审查
  bug_hunt    - 查找 bug
  file_search - 搜索文件
  suggest     - 提供建议
  guard       - 守护代码

物种列表:
  🐱 cat    - 猫咪 (普通)
  🐶 dog    - 狗狗 (普通)
  🐰 rabbit - 兔兔 (普通)
  🦊 fox    - 狐狸 (稀有)
  🐼 panda  - 熊猫 (稀有)
  🐉 dragon - 小龙 (史诗)
  🔥 phoenix - 凤凰 (史诗)
  🦄 unicorn - 独角兽 (传说)
"""
    
    action = args[0]
    
    if action == 'adopt':
        species = args[1] if len(args) > 1 else None
        name = args[2] if len(args) > 2 else None
        
        # 检查物种是否有效
        if species and species not in SPECIES:
            return f"❌ 无效的物种: {species}\n\n可选物种: {', '.join(SPECIES.keys())}"
        
        pet = manager.adopt_pet(species, name)
        
        shiny_text = " ✨ 闪光！" if pet.shiny else ""
        rarity_icon = {'common': '⚪', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟡'}[pet.rarity]
        
        return f"""
🎉 恭喜坤哥领养了新宠物！

{pet.emoji} {pet.name} {rarity_icon}{shiny_text}
物种: {pet.species}
稀有度: {pet.rarity}

快去照顾它吧！
喂食: /pet feed
玩耍: /pet play
状态: /pet status
"""
    
    elif action == 'list':
        pets = manager.list_pets()
        
        if not pets:
            return "🐾 还没有宠物，快去领养一只吧！\n领养: /pet adopt"
        
        output = [f"🐾 坤哥的宠物 ({len(pets)} 只):\n"]
        
        for pet in pets:
            shiny = '✨' if pet['shiny'] else ''
            rarity_icon = {'common': '⚪', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟡'}[pet['rarity']]
            active = '👈 当前' if pet['id'] == manager.active_pet_id else ''
            
            output.append(f"  {pet['emoji']} {pet['name']} {rarity_icon} {shiny} Lv.{pet['level']} {active}")
        
        return '\n'.join(output)
    
    elif action == 'status':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！\n领养: /pet adopt"
        
        return pet.get_status()
    
    elif action == 'feed':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        result = pet.feed()
        manager.save_pet(manager.active_pet_id)
        return result
    
    elif action == 'play':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        result = pet.play()
        manager.save_pet(manager.active_pet_id)
        return result
    
    elif action == 'train':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        result = pet.train()
        manager.save_pet(manager.active_pet_id)
        return result
    
    elif action == 'rest':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        result = pet.rest()
        manager.save_pet(manager.active_pet_id)
        return result
    
    elif action == 'switch':
        if len(args) < 2:
            return "❌ 请指定宠物ID\n用法: /pet switch <宠物ID>"
        
        pet_id = args[1]
        
        if pet_id not in manager.pets:
            return f"❌ 宠物不存在: {pet_id}\n\n查看所有宠物: /pet list"
        
        manager.set_active_pet(pet_id)
        pet = manager.get_active_pet()
        
        return f"✅ 已切换到 {pet.emoji} {pet.name}"
    
    elif action == 'species':
        output = ["🐾 可选物种:\n"]
        
        for species_id, info in SPECIES.items():
            rarity_icon = {'common': '⚪', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟡'}[info['rarity']]
            output.append(f"  {info['emoji']} {species_id:10} - {info['name']} {rarity_icon}")
        
        output.append("\n领养: /pet adopt <物种> [名字]")
        
        return '\n'.join(output)
    
    elif action == 'help':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        if len(args) < 2:
            return """
🐾 让宠物帮忙

用法: /pet help <任务类型>

任务类型:
  code_review - 代码审查
  bug_hunt    - 查找 bug
  file_search - 搜索文件
  suggest     - 提供建议
  guard       - 守护代码
"""
        
        task_type = args[1]
        valid_tasks = ['code_review', 'bug_hunt', 'file_search', 'suggest', 'guard']
        
        if task_type not in valid_tasks:
            return f"❌ 无效的任务类型: {task_type}\n\n有效类型: {', '.join(valid_tasks)}"
        
        # 检查是否能帮忙
        if not pet.can_help(task_type):
            return f"{pet.emoji} {pet.name} 不擅长这个任务..."
        
        # 尝试帮忙
        result = pet.help_task(task_type)
        manager.save_pet(manager.active_pet_id)
        
        return result['message']
    
    elif action == 'skills':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        output = [f"🎯 {pet.emoji} {pet.name} 的技能:\n"]
        
        skill_descriptions = {
            'hunt': '狩猎 - 帮助查找 bug',
            'stealth': '潜行 - 帮助搜索文件',
            'charm': '魅力 - 提供建议',
            'speed': '速度 - 快速搜索',
            'trick': '诡计 - 提供创意建议',
            'wisdom': '智慧 - 代码审查',
            'fire': '火焰 - 强力审查',
            'rebirth': '重生 - 恢复代码',
            'magic': '魔法 - 神奇建议',
            'guard': '守护 - 保护代码',
        }
        
        for skill, level in pet.skills.items():
            bar = '█' * level + '░' * (5 - level)
            desc = skill_descriptions.get(skill, skill)
            output.append(f"  {skill:10} {bar} Lv.{level} - {desc}")
        
        return '\n'.join(output)
    
    elif action == 'release':
        if len(args) < 2:
            return "❌ 请指定宠物ID\n用法: /pet release <宠物ID>"
        
        pet_id = args[1]
        
        if pet_id not in manager.pets:
            return f"❌ 宠物不存在: {pet_id}\n\n查看所有宠物: /pet list"
        
        pet = manager.pets[pet_id]
        pet_name = f"{pet.emoji} {pet.name}"
        
        # 删除宠物
        del manager.pets[pet_id]
        
        # 删除存储文件
        import os
        file_path = os.path.join(manager.storage_dir, f'{pet_id}.json')
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 如果是当前宠物，切换到其他宠物
        if manager.active_pet_id == pet_id:
            if manager.pets:
                manager.active_pet_id = list(manager.pets.keys())[0]
            else:
                manager.active_pet_id = None
        
        return f"""
👋 {pet_name} 已经回归大自然了...

感谢它的陪伴！
想养新宠物？/pet adopt
"""
    
    elif action == 'skills':
        pet = manager.get_active_pet()
        
        if not pet:
            return "🐾 还没有宠物，快去领养一只吧！"
        
        output = [f"🎯 {pet.emoji} {pet.name} 的技能:\n"]
        
        skill_descriptions = {
            'hunt': '狩猎 - 帮助查找 bug',
            'stealth': '潜行 - 帮助搜索文件',
            'charm': '魅力 - 提供建议',
            'speed': '速度 - 快速搜索',
            'trick': '诡计 - 提供创意建议',
            'wisdom': '智慧 - 代码审查',
            'fire': '火焰 - 强力审查',
            'rebirth': '重生 - 恢复代码',
            'magic': '魔法 - 神奇建议',
            'guard': '守护 - 保护代码',
        }
        
        for skill, level in pet.skills.items():
            bar = '█' * level + '░' * (5 - level)
            desc = skill_descriptions.get(skill, skill)
            output.append(f"  {skill:10} {bar} Lv.{level} - {desc}")
        
        return '\n'.join(output)
    
    else:
        return f"❌ 未知命令: {action}\n\n用法: /pet [adopt|list|status|feed|play|train|rest|switch|species|help|skills]"
