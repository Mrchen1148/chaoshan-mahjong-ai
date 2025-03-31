# 潮汕麻将助手 (Chaoshan Mahjong Assistant)

一个智能的潮汕麻将辅助工具，使用先进的AI技术提供游戏分析和辅助功能。

## 功能特点

- 智能出牌建议
- 自动选牌优化
- 实时游戏分析
- 人性化操作模拟
- 防检测机制
- 美观的Material Design界面

## 系统要求

- Android 5.0 (API 21) 或更高版本
- 需要以下权限：
  - 屏幕录制权限
  - 无障碍服务权限
  - 悬浮窗权限

## 安装说明

1. 从Release页面下载最新的APK文件
2. 在Android设备上安装APK
3. 首次运行时，按照提示授予必要权限

## 使用方法

1. 启动应用
2. 点击"权限设置"并授予所需权限
3. 从下拉菜单选择目标游戏
4. 根据需要开启/关闭功能开关
5. 点击"开始"运行助手

## 开发环境设置

### 依赖安装

```bash
# 安装Python依赖
pip install -r requirements.txt
pip install -r requirements-app.txt

# 安装buildozer（用于构建APK）
pip install buildozer
```

### 本地构建

```bash
# 使用buildozer构建APK
buildozer android debug
```

### 使用GitHub Actions构建

1. Fork 本仓库
2. 启用GitHub Actions
3. 推送代码到main分支
4. 在Actions标签页查看构建进度
5. 构建完成后下载APK

## 安全特性

- 智能行为模拟
- 动态操作延迟
- 模式混淆技术
- 自适应防检测

## 注意事项

- 首次使用需要完成权限设置
- 建议在游戏开始前启动助手
- 如遇性能问题，可以关闭不需要的功能
- 请遵守当地法律法规

## 技术栈

- Python 3.9+
- Kivy/KivyMD (UI框架)
- OpenCV (图像处理)
- NumPy (数值计算)
- Android SDK
- Buildozer (打包工具)

## 构建状态

[![Build Android APK](https://github.com/[USERNAME]/chaoshan-mahjong-ai/actions/workflows/build.yml/badge.svg)](https://github.com/[USERNAME]/chaoshan-mahjong-ai/actions/workflows/build.yml)

## 许可证

MIT License
