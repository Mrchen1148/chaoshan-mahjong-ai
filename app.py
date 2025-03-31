from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

import cv2
import numpy as np
from functools import partial
import threading
import time

from ..core import ChaoshanMJPlugin
from .android_utils import AndroidScreenCapture, AndroidInputSimulator, AndroidAccessibilityService

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
        self.plugin = None
        self.screen_capture = AndroidScreenCapture()
        self.input_simulator = AndroidInputSimulator()
        self.accessibility_service = AndroidAccessibilityService()
        self.is_running = False
        
    def setup_ui(self):
        """设置UI界面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = MDLabel(
            text="潮汕麻将助手",
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        layout.add_widget(title)
        
        # 游戏选择
        self.game_spinner = Spinner(
            text='选择游戏',
            values=('游戏A', '游戏B', '游戏C'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': .5}
        )
        layout.add_widget(self.game_spinner)
        
        # 功能开关
        features_card = MDCard(
            orientation='vertical',
            padding=10,
            spacing=10,
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={'center_x': .5}
        )
        
        # 智能出牌开关
        discard_layout = BoxLayout(orientation='horizontal')
        discard_label = MDLabel(text="智能出牌")
        self.discard_switch = Switch(active=True)
        discard_layout.add_widget(discard_label)
        discard_layout.add_widget(self.discard_switch)
        features_card.add_widget(discard_layout)
        
        # 智能选牌开关
        select_layout = BoxLayout(orientation='horizontal')
        select_label = MDLabel(text="智能选牌")
        self.select_switch = Switch(active=True)
        select_layout.add_widget(select_label)
        select_layout.add_widget(self.select_switch)
        features_card.add_widget(select_layout)
        
        layout.add_widget(features_card)
        
        # 控制按钮
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': .5}
        )
        
        self.start_button = MDRaisedButton(
            text="开始",
            on_release=self.toggle_service
        )
        buttons_layout.add_widget(self.start_button)
        
        self.permission_button = MDRaisedButton(
            text="权限设置",
            on_release=self.request_permissions
        )
        buttons_layout.add_widget(self.permission_button)
        
        layout.add_widget(buttons_layout)
        
        # 状态标签
        self.status_label = MDLabel(
            text="就绪",
            halign="center",
            theme_text_color="Secondary"
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
        
    def toggle_service(self, instance):
        """切换服务状态"""
        if not self.is_running:
            self.start_service()
        else:
            self.stop_service()
            
    def start_service(self):
        """启动服务"""
        if not self.plugin:
            self.plugin = ChaoshanMJPlugin()
            
        # 启动屏幕捕获
        if self.screen_capture.start_capture():
            self.is_running = True
            self.start_button.text = "停止"
            self.status_label.text = "运行中"
            
            # 启动主循环
            threading.Thread(
                target=self.main_loop,
                daemon=True
            ).start()
        else:
            self.status_label.text = "启动失败"
            
    def stop_service(self):
        """停止服务"""
        self.is_running = False
        self.screen_capture.stop_capture()
        self.start_button.text = "开始"
        self.status_label.text = "已停止"
        
    def request_permissions(self, instance):
        """请求权限"""
        self.accessibility_service.start_service()
        self.screen_capture.start_capture()
        
    def main_loop(self):
        """主循环"""
        while self.is_running:
            try:
                # 捕获屏幕
                screen_data = self.screen_capture.capture_screen()
                if screen_data:
                    # 转换为OpenCV格式
                    nparr = np.frombuffer(screen_data, np.uint8)
                    screen_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    # 处理游戏画面
                    game_state = self.plugin.process_game_screen(screen_img)
                    
                    # 根据开关状态执行相应功能
                    if self.discard_switch.active and 'tiles' in game_state:
                        tile = self.plugin.intelligent_discard(game_state['tiles'])
                        if tile:
                            # 模拟点击出牌
                            pos = self.plugin._find_tile_position(tile)
                            if pos:
                                self.input_simulator.tap(pos[0], pos[1])
                                
                    if self.select_switch.active and 'available_tiles' in game_state:
                        selected = self.plugin.tile_selection(
                            game_state['available_tiles'])
                        for tile in selected:
                            pos = self.plugin._find_tile_position(tile)
                            if pos:
                                self.input_simulator.tap(pos[0], pos[1])
                                time.sleep(0.1)
                                
            except Exception as e:
                print(f"Error in main loop: {e}")
                
            time.sleep(0.1)  # 控制循环频率

class ChaoshanMJApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return MainScreen()
