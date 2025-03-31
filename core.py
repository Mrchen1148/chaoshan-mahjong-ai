import random
import numpy as np
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import time

from .tiles import Tile, TileType, TileSet
from .utils import ProbabilityEngine, OperationDelay
from .vision import ScreenProcessor
from .automation import GameController
from .anti_detection import BehaviorSimulator

class ChaoshanMJPlugin:
    def __init__(self, window_title: str = ""):
        self.history = []
        self.prob_engine = ProbabilityEngine()
        self.delay_module = OperationDelay()
        self.screen_processor = ScreenProcessor()
        self.game_controller = GameController(window_title) if window_title else None
        self.behavior_sim = BehaviorSimulator()
        self.hand_tiles = []
        self.discard_history = []
        self.game_context = GameContext()

    def initialize(self, window_title: str) -> bool:
        """初始化插件"""
        self.game_controller = GameController(window_title)
        return self.game_controller.initialize()

    def intelligent_discard(self, tiles: List[Tile]) -> Tile:
        """智能出牌决策"""
        # 更新状态
        self.hand_tiles = tiles.copy()
        
        # 动态权重评估
        scores = self.prob_engine.calculate_tile_scores(tiles)
        
        # 行为模拟
        options = [(tile, score) for tile, score in scores.items()]
        selected_tile, _ = self.behavior_sim.simulate_decision(options)
        
        # 模拟反应时间
        reaction_time = self.behavior_sim.simulate_reaction('decision')
        self.delay_module.random_delay('discard')
        
        # 如果有游戏控制器，执行实际操作
        if self.game_controller:
            tile_pos = self._find_tile_position(selected_tile)
            if tile_pos:
                self.game_controller.click_tile(tile_pos)
        
        self._record_discard(selected_tile)
        return selected_tile

    def tile_selection(self, available_tiles: List[Tile]) -> List[Tile]:
        """智能选牌"""
        # 行为模拟
        reaction_time = self.behavior_sim.simulate_reaction('select')
        self.delay_module.random_delay('select')
        
        # 概率增强
        enhanced_tiles = self.prob_engine.enhance_quality(available_tiles)
        
        # 模拟人类选择
        selected = []
        for _ in range(13):
            if not enhanced_tiles:
                break
            options = [(tile, self._calculate_selection_score(tile)) 
                      for tile in enhanced_tiles[:5]]
            choice, _ = self.behavior_sim.simulate_decision(options)
            selected.append(choice)
            enhanced_tiles.remove(choice)
        
        # 执行实际操作
        if self.game_controller:
            for tile in selected:
                tile_pos = self._find_tile_position(tile)
                if tile_pos:
                    self.game_controller.click_tile(tile_pos)
                    # 模拟人类操作间隔
                    time.sleep(self.behavior_sim.simulate_reaction('click'))
        
        self._update_history(selected)
        return selected

    def process_game_screen(self, screen_img: np.ndarray) -> Dict:
        """处理游戏画面"""
        return self.screen_processor.process_screen(screen_img)

    def handle_opponent_action(self, action_type: str, tiles: List[Tile]):
        """处理对手动作"""
        for tile in tiles:
            self.prob_engine.update_seen_tiles(tile)
        self.game_context.update_opponent_action(action_type, tiles)

    def _find_tile_position(self, tile: Tile) -> Optional[Tuple[int, int]]:
        """查找牌的位置"""
        # 这里需要实现具体的位置查找逻辑
        # 可以通过图像识别或预定义位置来实现
        pass

    def _calculate_selection_score(self, tile: Tile) -> float:
        """计算选牌分数"""
        base_score = random.uniform(0.8, 1.2)
        
        # 考虑牌型
        if tile.type in [TileType.WIND, TileType.DRAGON]:
            base_score *= 1.1
            
        # 考虑数值
        if hasattr(tile, 'value'):
            if 4 <= tile.value <= 6:
                base_score *= 1.2
                
        return base_score

    def _record_discard(self, tile: Tile):
        """记录出牌"""
        self.discard_history.append(tile)
        self.prob_engine.update_seen_tiles(tile)

    def _update_history(self, tiles: List[Tile]):
        """更新历史记录"""
        self.history.append(tiles)
        for tile in tiles:
            self.prob_engine.update_seen_tiles(tile)

class GameContext:
    """游戏上下文管理"""
    def __init__(self):
        self.turn_count = 0
        self.opponent_actions = defaultdict(list)
        self.game_stage = "early"  # early, middle, late
        
    def update_opponent_action(self, action_type: str, tiles: List[Tile]):
        """更新对手行为数据"""
        self.opponent_actions[action_type].append(tiles)
        self.turn_count += 1
        self._update_game_stage()
        
    def _update_game_stage(self):
        """更新游戏阶段"""
        if self.turn_count < 8:
            self.game_stage = "early"
        elif self.turn_count < 16:
            self.game_stage = "middle"
        else:
            self.game_stage = "late"
            
    def get_stage_factor(self) -> float:
        """获取游戏阶段因子"""
        stage_factors = {
            "early": 1.2,    # 早期更激进
            "middle": 1.0,   # 中期平稳
            "late": 0.8      # 后期保守
        }
        return stage_factors[self.game_stage]
