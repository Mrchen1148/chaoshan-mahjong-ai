import random
import time
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from collections import deque

class BehaviorRandomizer:
    """行为随机化器"""
    def __init__(self):
        self.action_history = deque(maxlen=100)
        self.pattern_detector = PatternDetector()
        self.last_action_time = time.time()
        
    def randomize_delay(self, action_type: str) -> float:
        """随机化延迟时间"""
        # 基础延迟范围
        base_delays = {
            'click': (0.3, 0.8),
            'move': (0.2, 0.5),
            'drag': (0.4, 0.9),
            'decision': (0.8, 2.0)
        }
        
        # 获取基础延迟
        min_delay, max_delay = base_delays.get(
            action_type, (0.5, 1.0))
            
        # 添加随机性
        delay = self._generate_natural_delay(min_delay, max_delay)
        
        # 根据历史模式调整
        if self.pattern_detector.detect_pattern(self.action_history):
            delay = self._break_pattern(delay)
            
        self.action_history.append({
            'type': action_type,
            'delay': delay,
            'time': time.time()
        })
        
        return delay
        
    def _generate_natural_delay(
        self, min_delay: float, max_delay: float) -> float:
        """生成自然的延迟时间"""
        # 使用beta分布生成更自然的随机数
        alpha = 2
        beta = 5
        raw = np.random.beta(alpha, beta)
        
        # 映射到目标范围
        delay = min_delay + raw * (max_delay - min_delay)
        
        # 添加微小的随机扰动
        noise = np.random.normal(0, 0.05)
        delay = max(min_delay, min(max_delay, delay + noise))
        
        return delay
        
    def _break_pattern(self, delay: float) -> float:
        """打破规律性"""
        # 随机增加或减少延迟
        if random.random() < 0.5:
            delay *= random.uniform(1.2, 1.5)
        else:
            delay *= random.uniform(0.7, 0.9)
            
        return delay

class PatternDetector:
    """模式检测器"""
    def __init__(self):
        self.pattern_window = 10
        self.similarity_threshold = 0.8
        
    def detect_pattern(self, history: deque) -> bool:
        """检测行为模式"""
        if len(history) < self.pattern_window * 2:
            return False
            
        recent = list(history)[-self.pattern_window:]
        previous = list(history)[-(self.pattern_window*2):-self.pattern_window]
        
        # 计算时间间隔的相似度
        time_diffs1 = [
            h['time'] - history[i-1]['time'] 
            for i, h in enumerate(previous) 
            if i > 0
        ]
        time_diffs2 = [
            h['time'] - history[i-1]['time'] 
            for i, h in enumerate(recent) 
            if i > 0
        ]
        
        # 计算相似度
        similarity = self._calculate_similarity(
            time_diffs1, time_diffs2)
            
        return similarity > self.similarity_threshold
        
    def _calculate_similarity(
        self, seq1: List[float], seq2: List[float]) -> float:
        """计算序列相似度"""
        if not seq1 or not seq2:
            return 0
            
        # 标准化序列
        seq1_norm = self._normalize_sequence(seq1)
        seq2_norm = self._normalize_sequence(seq2)
        
        # 计算欧氏距离
        distance = np.sqrt(np.mean(
            [(a - b) ** 2 for a, b in zip(seq1_norm, seq2_norm)]))
            
        # 转换为相似度分数
        similarity = 1 / (1 + distance)
        
        return similarity
        
    def _normalize_sequence(self, seq: List[float]) -> List[float]:
        """标准化序列"""
        if not seq:
            return seq
        min_val = min(seq)
        max_val = max(seq)
        if max_val == min_val:
            return [0.5] * len(seq)
        return [(x - min_val) / (max_val - min_val) for x in seq]

class BehaviorSimulator:
    """行为模拟器"""
    def __init__(self):
        self.randomizer = BehaviorRandomizer()
        self.error_rate = 0.05  # 基础错误率
        self.learning_rate = 0.01  # 学习速率
        self.performance_history = deque(maxlen=50)
        
    def simulate_decision(self, options: List[Any]) -> Any:
        """模拟决策过程"""
        # 计算当前错误率
        current_error_rate = self._calculate_error_rate()
        
        # 根据错误率决定是否做出次优选择
        if random.random() < current_error_rate:
            # 选择次优选项
            if len(options) > 1:
                options = sorted(options, key=lambda x: x[1], reverse=True)
                return random.choice(options[1:min(len(options), 3)])
        
        # 返回最优选项
        return max(options, key=lambda x: x[1])
        
    def simulate_reaction(self, event_type: str) -> float:
        """模拟反应时间"""
        base_delay = self.randomizer.randomize_delay(event_type)
        
        # 添加认知负荷影响
        cognitive_load = self._calculate_cognitive_load()
        delay = base_delay * (1 + cognitive_load)
        
        # 记录性能
        self.performance_history.append({
            'type': event_type,
            'delay': delay,
            'time': time.time()
        })
        
        return delay
        
    def _calculate_error_rate(self) -> float:
        """计算动态错误率"""
        # 基础错误率
        rate = self.error_rate
        
        # 根据最近表现调整
        recent_performance = list(self.performance_history)[-10:]
        if recent_performance:
            avg_delay = np.mean([p['delay'] for p in recent_performance])
            rate += self.learning_rate * (avg_delay - 0.5)
            
        # 确保错误率在合理范围内
        return max(0.01, min(0.15, rate))
        
    def _calculate_cognitive_load(self) -> float:
        """计算认知负荷"""
        # 分析最近的操作频率
        recent_actions = list(self.performance_history)[-5:]
        if not recent_actions:
            return 0
            
        # 计算操作间隔
        intervals = [
            actions[i]['time'] - actions[i-1]['time']
            for i in range(1, len(recent_actions))
        ]
        
        if not intervals:
            return 0
            
        # 根据操作频率估算认知负荷
        avg_interval = np.mean(intervals)
        load = max(0, 1 - avg_interval / 2)  # 标准化到0-1范围
        
        return load
