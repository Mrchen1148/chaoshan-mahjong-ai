import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import List, Tuple, Dict, Optional
import logging

class TileRecognizer:
    """麻将牌识别器"""
    def __init__(self, template_dir: str = "templates/"):
        self.template_dir = template_dir
        self.templates = {}
        self.load_templates()
        
    def load_templates(self):
        """加载模板图像"""
        # 实际使用时需要准备对应APP的麻将牌模板
        pass
        
    def recognize_tiles(self, screen_img: np.ndarray) -> List[Tuple[str, float]]:
        """识别屏幕上的麻将牌"""
        results = []
        gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        
        for tile_name, template in self.templates.items():
            # 使用多尺度模板匹配
            scales = np.linspace(0.8, 1.2, 5)
            for scale in scales:
                resized = cv2.resize(template, None, fx=scale, fy=scale)
                result = cv2.matchTemplate(gray, resized, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= 0.8)
                
                for pt in zip(*locations[::-1]):
                    results.append((tile_name, result[pt[1], pt[0]]))
                    
        return sorted(results, key=lambda x: x[1], reverse=True)

class GameStateAnalyzer:
    """游戏状态分析器"""
    def __init__(self):
        self.last_state = None
        self.state_history = []
        
    def analyze_screen(self, screen_img: np.ndarray) -> Dict:
        """分析当前游戏画面状态"""
        state = {
            'phase': self._detect_game_phase(screen_img),
            'player_tiles': self._detect_player_tiles(screen_img),
            'opponent_actions': self._detect_opponent_actions(screen_img),
            'available_actions': self._detect_available_actions(screen_img)
        }
        
        self.last_state = state
        self.state_history.append(state)
        return state
        
    def _detect_game_phase(self, img: np.ndarray) -> str:
        """检测游戏阶段"""
        # 使用OCR识别游戏阶段文字
        text = pytesseract.image_to_string(img, lang='chi_sim')
        
        phase_keywords = {
            'early': ['开局', '准备'],
            'middle': ['进行中', '打牌'],
            'late': ['结束', '流局']
        }
        
        for phase, keywords in phase_keywords.items():
            if any(keyword in text for keyword in keywords):
                return phase
                
        return 'unknown'
        
    def _detect_player_tiles(self, img: np.ndarray) -> List[str]:
        """检测玩家手牌"""
        # 实现手牌区域识别和分析
        pass
        
    def _detect_opponent_actions(self, img: np.ndarray) -> List[Dict]:
        """检测对手动作"""
        # 实现对手动作区域识别和分析
        pass
        
    def _detect_available_actions(self, img: np.ndarray) -> List[str]:
        """检测可用动作"""
        # 实现可用动作按钮识别
        pass

class ScreenProcessor:
    """屏幕处理器"""
    def __init__(self):
        self.recognizer = TileRecognizer()
        self.analyzer = GameStateAnalyzer()
        
    def process_screen(self, screen_img: np.ndarray) -> Dict:
        """处理屏幕图像"""
        # 预处理图像
        processed = self._preprocess_image(screen_img)
        
        # 识别麻将牌
        tiles = self.recognizer.recognize_tiles(processed)
        
        # 分析游戏状态
        state = self.analyzer.analyze_screen(processed)
        
        return {
            'tiles': tiles,
            'state': state
        }
        
    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """图像预处理"""
        # 增强对比度
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        enhanced = cv2.merge((cl,a,b))
        
        # 降噪
        denoised = cv2.fastNlMeansDenoisingColored(enhanced)
        
        return denoised
