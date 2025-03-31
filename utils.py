import random
import time
import numpy as np
from collections import defaultdict
from typing import List, Dict, Any
from .tiles import Tile, TileType

class ProbabilityEngine:
    def __init__(self):
        self.tile_stats = defaultdict(int)
        self.pattern_weights = self._initialize_weights()
        self.seen_tiles = set()

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'pair': 1.2,
            'sequence': 1.5,
            'triplet': 1.8,
            'potential': 1.3
        }

    def calculate_tile_scores(self, tiles: List[Tile]) -> Dict[Tile, float]:
        """计算每张牌的得分"""
        scores = {}
        for tile in tiles:
            base_score = self._calculate_base_score(tile)
            pattern_score = self._evaluate_patterns(tile, tiles)
            potential_score = self._evaluate_potential(tile, tiles)
            
            scores[tile] = base_score * pattern_score * potential_score
            
        return scores

    def _calculate_base_score(self, tile: Tile) -> float:
        """基础分计算"""
        if tile.type in [TileType.WIND, TileType.DRAGON]:
            return 1.0 + (0.2 if tile not in self.seen_tiles else 0)
        
        # 数牌的基础分计算
        middle_bonus = 1.2 if 4 <= tile.value <= 6 else 1.0
        return middle_bonus * (1.1 if tile not in self.seen_tiles else 1.0)

    def _evaluate_patterns(self, tile: Tile, tiles: List[Tile]) -> float:
        """评估牌型分"""
        score = 1.0
        
        # 检查对子
        if sum(1 for t in tiles if t == tile) >= 2:
            score *= self.pattern_weights['pair']
            
        # 检查顺子潜力
        if tile.type in [TileType.WAN, TileType.TONG, TileType.SUO]:
            sequence_potential = self._check_sequence_potential(tile, tiles)
            score *= (1 + sequence_potential * self.pattern_weights['sequence'])
            
        return score

    def _evaluate_potential(self, tile: Tile, tiles: List[Tile]) -> float:
        """评估潜在价值"""
        potential = 1.0
        
        # 根据已见牌数调整概率
        seen_count = sum(1 for t in self.seen_tiles if t == tile)
        potential *= (1 - seen_count * 0.1)
        
        # 位置价值
        if tile.type in [TileType.WAN, TileType.TONG, TileType.SUO]:
            if 3 <= tile.value <= 7:
                potential *= 1.2
                
        return max(potential, 0.5)  # 确保最小值为0.5

    def _check_sequence_potential(self, tile: Tile, tiles: List[Tile]) -> float:
        """检查顺子潜力"""
        if tile.type not in [TileType.WAN, TileType.TONG, TileType.SUO]:
            return 0.0
            
        potential = 0.0
        value = tile.value
        
        # 检查前后连续性
        for v in range(max(1, value - 2), min(10, value + 3)):
            if any(t for t in tiles if t.type == tile.type and t.value == v):
                potential += 0.2
                
        return min(potential, 1.0)

    def enhance_quality(self, tiles: List[Tile]) -> List[Tile]:
        """增强牌型质量"""
        scores = self.calculate_tile_scores(tiles)
        return sorted(tiles, key=lambda t: scores[t], reverse=True)

    def update_seen_tiles(self, tile: Tile):
        """更新已见牌信息"""
        self.seen_tiles.add(tile)
        self.tile_stats[str(tile)] += 1

class OperationDelay:
    """操作延迟模拟器"""
    def __init__(self):
        self.last_action_time = defaultdict(float)
        self.action_patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> Dict[str, Dict[str, float]]:
        return {
            'select': {'min': 0.3, 'max': 1.2, 'mean': 0.6},
            'discard': {'min': 0.5, 'max': 2.0, 'mean': 1.0},
            'peng': {'min': 0.8, 'max': 2.5, 'mean': 1.5},
            'gang': {'min': 1.0, 'max': 3.0, 'mean': 1.8}
        }

    def random_delay(self, action_type: str):
        """生成人性化延迟"""
        pattern = self.action_patterns.get(action_type, 
                                         {'min': 0.5, 'max': 1.5, 'mean': 0.8})
        
        # 考虑上次操作时间
        time_since_last = time.time() - self.last_action_time[action_type]
        if time_since_last < pattern['min']:
            base_delay = pattern['mean']
        else:
            base_delay = random.gauss(pattern['mean'], 0.2)
            
        # 添加随机波动
        delay = max(pattern['min'], 
                   min(pattern['max'], 
                       base_delay * random.uniform(0.8, 1.2)))
                       
        time.sleep(delay)
        self.last_action_time[action_type] = time.time()

    def add_natural_variance(self, delay: float) -> float:
        """添加自然变化"""
        return delay * random.uniform(0.85, 1.15)
