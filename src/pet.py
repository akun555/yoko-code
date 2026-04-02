"""
YOKO Code - 宠物系统 🐾
坤哥专属的电子宠物
"""

import os
import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


# 宠物物种
SPECIES = {
    'cat': {'name': '猫咪', 'emoji': '🐱', 'rarity': 'common'},
    'dog': {'name': '狗狗', 'emoji': '🐶', 'rarity': 'common'},
    'rabbit': {'name': '兔兔', 'emoji': '🐰', 'rarity': 'common'},
    'fox': {'name': '狐狸', 'emoji': '🦊', 'rarity': 'rare'},
    'panda': {'name': '熊猫', 'emoji': '🐼', 'rarity': 'rare'},
    'dragon': {'name': '小龙', 'emoji': '🐉', 'rarity': 'epic'},
    'phoenix': {'name': '凤凰', 'emoji': '🔥', 'rarity': 'epic'},
    'unicorn': {'name': '独角兽', 'emoji': '🦄', 'rarity': 'legendary'},
}

# 稀有度权重
RARITY_WEIGHTS = {
    'common': 60,
    'rare': 25,
    'epic': 10,
    'legendary': 5,
}

# 稀有度颜色
RARITY_COLORS = {
    'common': '⚪',
    'rare': '🔵',
    'epic': '🟣',
    'legendary': '🟡',
}


class Pet:
    """宠物"""
    
    def __init__(self, species: str, name: str = None, shiny: bool = False):
        self.species = species
        self.name = name or SPECIES[species]['name']
        self.emoji = SPECIES[species]['emoji']
        self.rarity = SPECIES[species]['rarity']
        self.shiny = shiny
        
        # 属性
        self.hunger = 100      # 饱食度 (0-100)
        self.happiness = 100   # 快乐度 (0-100)
        self.energy = 100      # 精力 (0-100)
        self.exp = 0           # 经验值
        self.level = 1         # 等级
        
        # 技能
        self.skills = self._init_skills()
        
        # 统计
        self.feed_count = 0
        self.play_count = 0
        self.train_count = 0
        self.tasks_completed = 0
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()
    
    def _init_skills(self) -> Dict[str, int]:
        """初始化技能"""
        # 不同物种有不同的初始技能
        skill_presets = {
            'cat': {'hunt': 3, 'stealth': 5, 'charm': 4},
            'dog': {'hunt': 4, 'stealth': 2, 'charm': 5, 'guard': 4},
            'rabbit': {'hunt': 2, 'stealth': 4, 'charm': 3, 'speed': 5},
            'fox': {'hunt': 4, 'stealth': 5, 'charm': 3, 'trick': 4},
            'panda': {'hunt': 2, 'stealth': 2, 'charm': 5, 'wisdom': 4},
            'dragon': {'hunt': 5, 'stealth': 3, 'charm': 3, 'fire': 5},
            'phoenix': {'hunt': 3, 'stealth': 3, 'charm': 4, 'rebirth': 5},
            'unicorn': {'hunt': 2, 'stealth': 4, 'charm': 5, 'magic': 5},
        }
        
        base_skills = skill_presets.get(self.species, {'hunt': 3, 'stealth': 3, 'charm': 3})
        
        # 闪光宠物技能 +1
        if self.shiny:
            base_skills = {k: min(5, v + 1) for k, v in base_skills.items()}
        
        return base_skills
    
    def can_help(self, task_type: str) -> bool:
        """检查是否能帮忙"""
        task_skills = {
            'code_review': ['wisdom', 'charm'],
            'bug_hunt': ['hunt', 'stealth'],
            'file_search': ['hunt', 'speed'],
            'suggest': ['charm', 'magic', 'trick'],
            'guard': ['guard', 'stealth'],
        }
        
        required = task_skills.get(task_type, [])
        return any(skill in self.skills for skill in required)
    
    def help_task(self, task_type: str) -> Dict[str, Any]:
        """帮忙完成任务"""
        if self.energy < 10:
            return {
                'success': False,
                'message': f"{self.emoji} {self.name} 太累了，让它休息一下吧！"
            }
        
        # 计算成功率
        success_rate = self._calculate_success_rate(task_type)
        success = random.random() < success_rate
        
        if success:
            self.energy = max(0, self.energy - 10)
            self.exp += 15
            self.tasks_completed += 1
            self.last_interaction = datetime.now()
            
            self._check_level_up()
            
            messages = {
                'code_review': f"{self.emoji} {self.name} 帮你检查了代码，发现了一些问题！",
                'bug_hunt': f"{self.emoji} {self.name} 帮你找到了 bug！",
                'file_search': f"{self.emoji} {self.name} 帮你找到了文件！",
                'suggest': f"{self.emoji} {self.name} 给你提了个建议！",
                'guard': f"{self.emoji} {self.name} 守护了你的代码！",
            }
            
            return {
                'success': True,
                'message': messages.get(task_type, f"{self.emoji} {self.name} 帮你完成了任务！"),
                'bonus': self._get_task_bonus(task_type)
            }
        else:
            self.energy = max(0, self.energy - 5)
            self.last_interaction = datetime.now()
            
            return {
                'success': False,
                'message': f"{self.emoji} {self.name} 尝试帮忙但失败了..."
            }
    
    def _calculate_success_rate(self, task_type: str) -> float:
        """计算任务成功率"""
        base_rate = 0.3  # 基础 30%
        
        # 等级加成
        level_bonus = self.level * 0.05
        
        # 技能加成
        skill_bonus = 0
        task_skills = {
            'code_review': ['wisdom', 'charm'],
            'bug_hunt': ['hunt', 'stealth'],
            'file_search': ['hunt', 'speed'],
            'suggest': ['charm', 'magic', 'trick'],
            'guard': ['guard', 'stealth'],
        }
        
        for skill in task_skills.get(task_type, []):
            if skill in self.skills:
                skill_bonus += self.skills[skill] * 0.05
        
        # 稀有度加成
        rarity_bonus = {
            'common': 0,
            'rare': 0.1,
            'epic': 0.2,
            'legendary': 0.3,
        }[self.rarity]
        
        # 快乐度加成
        happy_bonus = self.happiness / 100 * 0.2
        
        total_rate = base_rate + level_bonus + skill_bonus + rarity_bonus + happy_bonus
        
        return min(0.95, total_rate)  # 最高 95%
    
    def _get_task_bonus(self, task_type: str) -> str:
        """获取任务奖励描述"""
        bonuses = {
            'code_review': '经验 +15',
            'bug_hunt': '经验 +15',
            'file_search': '经验 +15',
            'suggest': '经验 +15',
            'guard': '经验 +15',
        }
        return bonuses.get(task_type, '经验 +15')
    
    def feed(self) -> str:
        """喂食"""
        if self.hunger >= 100:
            return f"{self.emoji} {self.name} 已经吃饱啦！"
        
        self.hunger = min(100, self.hunger + 30)
        self.exp += 5
        self.feed_count += 1
        self.last_interaction = datetime.now()
        
        self._check_level_up()
        
        return f"{self.emoji} 给 {self.name} 喂食了！饱食度 +30"
    
    def play(self) -> str:
        """玩耍"""
        if self.energy < 10:
            return f"{self.emoji} {self.name} 太累了，让它休息一下吧！"
        
        self.happiness = min(100, self.happiness + 20)
        self.energy = max(0, self.energy - 10)
        self.hunger = max(0, self.hunger - 10)
        self.exp += 10
        self.play_count += 1
        self.last_interaction = datetime.now()
        
        self._check_level_up()
        
        messages = [
            f"{self.emoji} 和 {self.name} 玩了一会儿！好开心！",
            f"{self.emoji} {self.name} 玩得不亦乐乎！",
            f"{self.emoji} {self.name} 蹦蹦跳跳的！",
        ]
        
        return random.choice(messages)
    
    def train(self) -> str:
        """训练"""
        if self.energy < 20:
            return f"{self.emoji} {self.name} 太累了，让它休息一下吧！"
        
        self.energy = max(0, self.energy - 20)
        self.exp += 20
        self.train_count += 1
        self.last_interaction = datetime.now()
        
        self._check_level_up()
        
        return f"{self.emoji} 训练 {self.name}！经验 +20"
    
    def rest(self) -> str:
        """休息"""
        self.energy = min(100, self.energy + 50)
        self.last_interaction = datetime.now()
        
        return f"{self.emoji} {self.name} 休息了一会儿，精力恢复了！"
    
    def _check_level_up(self):
        """检查升级"""
        exp_needed = self.level * 100
        
        if self.exp >= exp_needed:
            self.exp -= exp_needed
            self.level += 1
            
            # 升级奖励
            self.hunger = min(100, self.hunger + 20)
            self.happiness = min(100, self.happiness + 20)
            self.energy = min(100, self.energy + 20)
    
    def update_status(self):
        """更新状态（随时间衰减）"""
        now = datetime.now()
        hours_passed = (now - self.last_interaction).total_seconds() / 3600
        
        # 随时间衰减
        self.hunger = max(0, self.hunger - hours_passed * 5)
        self.happiness = max(0, self.happiness - hours_passed * 3)
        self.energy = min(100, self.energy + hours_passed * 2)
    
    def get_status(self) -> str:
        """获取状态"""
        self.update_status()
        
        # 状态条
        hunger_bar = self._make_bar(self.hunger)
        happy_bar = self._make_bar(self.happiness)
        energy_bar = self._make_bar(self.energy)
        
        # 稀有度标识
        rarity_icon = RARITY_COLORS[self.rarity]
        shiny_icon = '✨' if self.shiny else ''
        
        # 技能显示
        skills_str = ', '.join([f"{k}:{v}" for k, v in self.skills.items()])
        
        status = f"""
╔══════════════════════════════════════╗
║  {shiny_icon} {self.emoji} {self.name} {rarity_icon} Lv.{self.level}
╠══════════════════════════════════════╣
║  饱食度  {hunger_bar} {int(self.hunger):>3}%
║  快乐度  {happy_bar} {int(self.happiness):>3}%
║  精力    {energy_bar} {int(self.energy):>3}%
╠══════════════════════════════════════╣
║  技能: {skills_str}
╠══════════════════════════════════════╣
║  经验值  {self.exp}/{self.level * 100}
║  喂食    {self.feed_count} 次
║  玩耍    {self.play_count} 次
║  训练    {self.train_count} 次
║  任务    {self.tasks_completed} 次
╚══════════════════════════════════════╝
"""
        return status
        return status
    
    def _make_bar(self, value: int, length: int = 10) -> str:
        """制作进度条"""
        filled = int(value / 100 * length)
        empty = length - filled
        return '█' * filled + '░' * empty
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'species': self.species,
            'name': self.name,
            'shiny': self.shiny,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'energy': self.energy,
            'exp': self.exp,
            'level': self.level,
            'skills': self.skills,
            'feed_count': self.feed_count,
            'play_count': self.play_count,
            'train_count': self.train_count,
            'tasks_completed': self.tasks_completed,
            'created_at': self.created_at.isoformat(),
            'last_interaction': self.last_interaction.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pet':
        """从字典创建"""
        pet = cls(data['species'], data['name'], data.get('shiny', False))
        pet.hunger = data.get('hunger', 100)
        pet.happiness = data.get('happiness', 100)
        pet.energy = data.get('energy', 100)
        pet.exp = data.get('exp', 0)
        pet.level = data.get('level', 1)
        pet.skills = data.get('skills', pet.skills)
        pet.feed_count = data.get('feed_count', 0)
        pet.play_count = data.get('play_count', 0)
        pet.train_count = data.get('train_count', 0)
        pet.tasks_completed = data.get('tasks_completed', 0)
        pet.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        pet.last_interaction = datetime.fromisoformat(data.get('last_interaction', datetime.now().isoformat()))
        return pet


class PetManager:
    """宠物管理器"""
    
    def __init__(self, storage_dir: str = None):
        self.storage_dir = storage_dir or os.path.expanduser('~/.yoko-code/pets')
        self.pets: Dict[str, Pet] = {}
        self.active_pet_id: Optional[str] = None
        
        os.makedirs(self.storage_dir, exist_ok=True)
        self.load_all_pets()
    
    def adopt_pet(self, species: str = None, name: str = None) -> Pet:
        """领养宠物"""
        # 随机选择物种
        if not species:
            species = self._random_species()
        
        # 检查是否闪光
        shiny = random.random() < 0.01  # 1% 概率闪光
        
        # 创建宠物
        pet = Pet(species, name, shiny)
        pet_id = f"{species}_{len(self.pets)}"
        
        self.pets[pet_id] = pet
        self.active_pet_id = pet_id
        self.save_pet(pet_id)
        
        return pet
    
    def _random_species(self) -> str:
        """随机选择物种（基于稀有度权重）"""
        species_list = list(SPECIES.keys())
        weights = [RARITY_WEIGHTS[SPECIES[s]['rarity']] for s in species_list]
        return random.choices(species_list, weights=weights)[0]
    
    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """获取宠物"""
        return self.pets.get(pet_id)
    
    def get_active_pet(self) -> Optional[Pet]:
        """获取当前宠物"""
        if self.active_pet_id:
            return self.pets.get(self.active_pet_id)
        return None
    
    def set_active_pet(self, pet_id: str):
        """设置当前宠物"""
        if pet_id in self.pets:
            self.active_pet_id = pet_id
    
    def list_pets(self) -> List[Dict[str, Any]]:
        """列出所有宠物"""
        pets = []
        for pet_id, pet in self.pets.items():
            pets.append({
                'id': pet_id,
                'name': pet.name,
                'emoji': pet.emoji,
                'species': pet.species,
                'rarity': pet.rarity,
                'level': pet.level,
                'shiny': pet.shiny,
            })
        return pets
    
    def save_pet(self, pet_id: str) -> bool:
        """保存宠物"""
        pet = self.pets.get(pet_id)
        if not pet:
            return False
        
        file_path = os.path.join(self.storage_dir, f'{pet_id}.json')
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(pet.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ 保存宠物失败: {e}")
            return False
    
    def load_pet(self, pet_id: str) -> Optional[Pet]:
        """加载宠物"""
        file_path = os.path.join(self.storage_dir, f'{pet_id}.json')
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            pet = Pet.from_dict(data)
            self.pets[pet_id] = pet
            return pet
        except Exception as e:
            print(f"❌ 加载宠物失败: {e}")
            return None
    
    def save_all_pets(self):
        """保存所有宠物"""
        for pet_id in self.pets:
            self.save_pet(pet_id)
    
    def load_all_pets(self):
        """加载所有宠物"""
        if not os.path.exists(self.storage_dir):
            return
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                pet_id = filename[:-5]
                self.load_pet(pet_id)


# 全局宠物管理器
_pet_manager = None


def get_pet_manager() -> PetManager:
    """获取宠物管理器实例"""
    global _pet_manager
    if _pet_manager is None:
        _pet_manager = PetManager()
    return _pet_manager
