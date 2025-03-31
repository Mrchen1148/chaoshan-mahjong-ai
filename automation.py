import pyautogui
import random
import time
from typing import Tuple, List, Optional
import logging
import win32gui
import win32con
import win32api
from .utils import OperationDelay

class HumanLikeControl:
    """人性化控制模块"""
    def __init__(self):
        self.delay = OperationDelay()
        self.last_action_time = time.time()
        self.movement_patterns = self._init_movement_patterns()
        
    def _init_movement_patterns(self) -> dict:
        """初始化移动模式"""
        return {
            'linear': lambda x, y: (x, y),
            'bezier': self._bezier_curve,
            'natural': self._natural_curve
        }
        
    def click(self, x: int, y: int, button: str = 'left'):
        """模拟人类点击"""
        # 移动到目标位置
        self.move_to(x, y)
        
        # 随机微调最终位置
        final_x = x + random.randint(-2, 2)
        final_y = y + random.randint(-2, 2)
        
        # 模拟点击前的短暂停顿
        time.sleep(random.uniform(0.1, 0.3))
        
        # 执行点击
        pyautogui.click(final_x, final_y, button=button)
        
        # 记录动作时间
        self.last_action_time = time.time()
        
    def move_to(self, x: int, y: int):
        """模拟人类鼠标移动"""
        # 选择移动模式
        pattern = random.choice(list(self.movement_patterns.keys()))
        
        # 获取当前位置
        current_x, current_y = pyautogui.position()
        
        # 生成路径点
        points = self._generate_movement_path(
            current_x, current_y, x, y, pattern)
            
        # 执行移动
        for px, py in points:
            # 添加速度变化
            speed = random.uniform(0.1, 0.3)
            pyautogui.moveTo(px, py, duration=speed)
            
    def _generate_movement_path(
        self, start_x: int, start_y: int, 
        end_x: int, end_y: int, pattern: str) -> List[Tuple[int, int]]:
        """生成移动路径"""
        points = []
        
        if pattern == 'linear':
            points = self._linear_interpolation(
                start_x, start_y, end_x, end_y)
        elif pattern == 'bezier':
            points = self._bezier_curve(
                start_x, start_y, end_x, end_y)
        else:
            points = self._natural_curve(
                start_x, start_y, end_x, end_y)
            
        return points
        
    def _linear_interpolation(
        self, start_x: int, start_y: int, 
        end_x: int, end_y: int) -> List[Tuple[int, int]]:
        """线性插值"""
        points = []
        steps = random.randint(10, 20)
        
        for i in range(steps + 1):
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            points.append((int(x), int(y)))
            
        return points
        
    def _bezier_curve(
        self, start_x: int, start_y: int, 
        end_x: int, end_y: int) -> List[Tuple[int, int]]:
        """贝塞尔曲线"""
        points = []
        steps = random.randint(20, 30)
        
        # 生成控制点
        ctrl_x = random.randint(
            min(start_x, end_x), max(start_x, end_x))
        ctrl_y = random.randint(
            min(start_y, end_y), max(start_y, end_y))
        
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**2 * start_x + 2*(1-t)*t * ctrl_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * ctrl_y + t**2 * end_y
            points.append((int(x), int(y)))
            
        return points
        
    def _natural_curve(
        self, start_x: int, start_y: int, 
        end_x: int, end_y: int) -> List[Tuple[int, int]]:
        """自然曲线"""
        points = []
        steps = random.randint(15, 25)
        
        # 添加随机偏移
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-20, 20)
        
        for i in range(steps + 1):
            t = i / steps
            # 使用正弦函数添加波动
            wave = math.sin(t * math.pi) * random.uniform(5, 10)
            x = start_x + (end_x - start_x) * t + wave + offset_x * t
            y = start_y + (end_y - start_y) * t + wave + offset_y * t
            points.append((int(x), int(y)))
            
        return points

class WindowManager:
    """窗口管理器"""
    def __init__(self):
        self.target_window = None
        self.window_rect = None
        
    def find_game_window(self, window_title: str) -> bool:
        """查找游戏窗口"""
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title.lower() in title.lower():
                    self.target_window = hwnd
                    return False
            return True
            
        win32gui.EnumWindows(callback, None)
        return self.target_window is not None
        
    def get_window_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取窗口位置和大小"""
        if self.target_window:
            try:
                self.window_rect = win32gui.GetWindowRect(self.target_window)
                return self.window_rect
            except Exception as e:
                logging.error(f"Failed to get window rect: {e}")
        return None
        
    def activate_window(self):
        """激活窗口"""
        if self.target_window:
            if win32gui.IsIconic(self.target_window):  # 如果窗口最小化
                win32gui.ShowWindow(self.target_window, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.target_window)
            
    def get_client_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取客户区域"""
        if self.target_window:
            try:
                return win32gui.GetClientRect(self.target_window)
            except Exception as e:
                logging.error(f"Failed to get client rect: {e}")
        return None

class GameController:
    """游戏控制器"""
    def __init__(self, window_title: str):
        self.window = WindowManager()
        self.control = HumanLikeControl()
        self.window_title = window_title
        
    def initialize(self) -> bool:
        """初始化控制器"""
        if not self.window.find_game_window(self.window_title):
            logging.error("Game window not found")
            return False
            
        self.window.activate_window()
        return True
        
    def click_tile(self, tile_pos: Tuple[int, int]):
        """点击麻将牌"""
        window_rect = self.window.get_window_rect()
        if not window_rect:
            return
            
        # 转换相对坐标为屏幕坐标
        screen_x = window_rect[0] + tile_pos[0]
        screen_y = window_rect[1] + tile_pos[1]
        
        # 执行点击
        self.control.click(screen_x, screen_y)
        
    def drag_tile(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        """拖动麻将牌"""
        window_rect = self.window.get_window_rect()
        if not window_rect:
            return
            
        # 转换坐标
        start_x = window_rect[0] + start_pos[0]
        start_y = window_rect[1] + start_pos[1]
        end_x = window_rect[0] + end_pos[0]
        end_y = window_rect[1] + end_pos[1]
        
        # 执行拖动
        self.control.move_to(start_x, start_y)
        pyautogui.mouseDown()
        self.control.move_to(end_x, end_y)
        pyautogui.mouseUp()
