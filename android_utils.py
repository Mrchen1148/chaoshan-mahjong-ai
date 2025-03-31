from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android import activity
import time
from typing import Optional, Tuple

# Android类
Context = autoclass('android.content.Context')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
MediaProjectionManager = autoclass('android.media.projection.MediaProjectionManager')
ImageReader = autoclass('android.media.ImageReader')
PixelFormat = autoclass('android.graphics.PixelFormat')
Handler = autoclass('android.os.Handler')
Looper = autoclass('android.os.Looper')
Intent = autoclass('android.content.Intent')

class AndroidScreenCapture:
    """Android屏幕捕获工具"""
    def __init__(self):
        self.activity = PythonActivity.mActivity
        self.projection_manager = None
        self.media_projection = None
        self.image_reader = None
        self.virtual_display = None
        self.width = 0
        self.height = 0
        
    def start_capture(self) -> bool:
        """开始屏幕捕获"""
        try:
            self.projection_manager = cast(
                'android.media.projection.MediaProjectionManager',
                self.activity.getSystemService(Context.MEDIA_PROJECTION_SERVICE)
            )
            
            # 请求屏幕捕获权限
            intent = self.projection_manager.createScreenCaptureIntent()
            self.activity.startActivityForResult(intent, 1)
            return True
        except Exception as e:
            print(f"Failed to start capture: {e}")
            return False
            
    @run_on_ui_thread
    def on_activity_result(self, request_code: int, result_code: int, data: Intent):
        """处理权限请求结果"""
        if request_code == 1 and result_code == activity.RESULT_OK:
            self.media_projection = self.projection_manager.getMediaProjection(
                result_code, data)
            self._setup_virtual_display()
            
    def _setup_virtual_display(self):
        """设置虚拟显示"""
        metrics = self.activity.getResources().getDisplayMetrics()
        self.width = metrics.widthPixels
        self.height = metrics.heightPixels
        
        self.image_reader = ImageReader.newInstance(
            self.width, self.height, PixelFormat.RGBA_8888, 2)
            
        self.virtual_display = self.media_projection.createVirtualDisplay(
            "ScreenCapture",
            self.width, self.height,
            metrics.densityDpi,
            0x00000001,  # VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR
            self.image_reader.getSurface(),
            None, None
        )
        
    def capture_screen(self) -> Optional[bytes]:
        """捕获当前屏幕"""
        if not self.image_reader:
            return None
            
        image = self.image_reader.acquireLatestImage()
        if not image:
            return None
            
        try:
            planes = image.getPlanes()
            buffer = planes[0].getBuffer()
            pixels = bytes(buffer.array())
            return pixels
        finally:
            image.close()
            
    def stop_capture(self):
        """停止屏幕捕获"""
        if self.virtual_display:
            self.virtual_display.release()
        if self.media_projection:
            self.media_projection.stop()
        if self.image_reader:
            self.image_reader.close()

class AndroidInputSimulator:
    """Android输入模拟器"""
    def __init__(self):
        self.uiautomator = autoclass('androidx.test.uiautomator.UiDevice')
        self.instrumentation = autoclass('android.app.Instrumentation')
        self.device = self.uiautomator.getInstance(
            self.instrumentation())
            
    def tap(self, x: int, y: int):
        """模拟点击"""
        self.device.click(x, y)
        
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int):
        """模拟滑动"""
        self.device.swipe(start_x, start_y, end_x, end_y, duration)
        
    def long_press(self, x: int, y: int, duration: int):
        """模拟长按"""
        self.device.longClick(x, y, duration)

class AndroidAccessibilityService:
    """Android无障碍服务"""
    def __init__(self):
        self.service = None
        
    def start_service(self):
        """启动无障碍服务"""
        try:
            intent = Intent()
            intent.setAction("android.settings.ACCESSIBILITY_SETTINGS")
            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            print(f"Failed to start accessibility service: {e}")
            
    def get_window_content(self) -> str:
        """获取当前窗口内容"""
        if not self.service:
            return ""
        root = self.service.getRootInActiveWindow()
        if not root:
            return ""
        return root.getText()
