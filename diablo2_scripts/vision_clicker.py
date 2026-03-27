#!/usr/bin/env python3
"""
Diablo II 视觉识别点击功能
- 使用图像识别找到按钮位置
- 动态计算点击坐标
- 支持多种按钮识别
"""

import os
os.environ['DISPLAY'] = ':0'

import subprocess
import time
import numpy as np
from PIL import Image, ImageGrab
import cv2

class VisionClicker:
    """视觉识别点击类"""
    
    def __init__(self):
        self.screenshot_dir = "/home/user/.openclaw/workspace/diablo2_scripts/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self):
        """截取屏幕截图"""
        timestamp = int(time.time())
        screenshot_path = f"{self.screenshot_dir}/screenshot_{timestamp}.png"
        
        # 使用ImageGrab截取屏幕
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        
        return screenshot_path
    
    def find_template(self, template_path, threshold=0.8):
        """在屏幕中查找模板图像"""
        # 截取屏幕
        screenshot_path = self.take_screenshot()
        screenshot = cv2.imread(screenshot_path)
        
        # 读取模板
        template = cv2.imread(template_path)
        if template is None:
            print(f"   ⚠ 无法读取模板: {template_path}")
            return None
        
        # 模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # 计算中心点
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)
        
        return None
    
    def click_at(self, x, y):
        """点击指定坐标"""
        try:
            subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
            time.sleep(0.1)
            subprocess.run(["xdotool", "click", "1"], check=True)
            print(f"   ✓ 点击位置: ({x}, {y})")
        except Exception as e:
            print(f"   ⚠ 点击错误: {e}")
    
    def find_and_click(self, template_path, threshold=0.8):
        """查找并点击模板"""
        print(f"查找模板: {template_path}")
        
        result = self.find_template(template_path, threshold)
        
        if result:
            x, y, confidence = result
            print(f"   ✓ 找到模板，置信度: {confidence:.2f}")
            self.click_at(x, y)
            return True
        else:
            print(f"   ✗ 未找到模板 (阈值: {threshold})")
            return False
    
    def find_game_window(self):
        """找到游戏窗口位置"""
        try:
            result = subprocess.run(
                ["xdotool", "search", "--name", "Diablo II"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                window_id = result.stdout.strip().split('\n')[0]
                
                # 获取窗口位置
                result = subprocess.run(
                    ["xwininfo", "-id", window_id],
                    capture_output=True, text=True
                )
                
                info = result.stdout
                import re
                match = re.search(r'Absolute upper-left X:\s+(\d+)', info)
                x = int(match.group(1)) if match else 0
                match = re.search(r'Absolute upper-left Y:\s+(\d+)', info)
                y = int(match.group(1)) if match else 0
                match = re.search(r'Width:\s+(\d+)', info)
                width = int(match.group(1)) if match else 800
                match = re.search(r'Height:\s+(\d+)', info)
                height = int(match.group(1)) if match else 600
                
                return {"id": window_id, "x": x, "y": y, "width": width, "height": height}
        except Exception as e:
            print(f"   ⚠ 查找窗口错误: {e}")
        
        return None


def main():
    print("Diablo II 视觉识别点击")
    print("=" * 50)
    
    # 检查依赖
    try:
        import cv2
        import numpy as np
        from PIL import Image, ImageGrab
        print("✓ 所有依赖已安装")
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请安装: pip install opencv-python numpy Pillow")
        return
    
    vision = VisionClicker()
    
    # 查找游戏窗口
    print("\n查找游戏窗口...")
    window = vision.find_game_window()
    if window:
        print(f"✓ 窗口位置: ({window['x']}, {window['y']})")
    else:
        print("✗ 未找到游戏窗口")
        return
    
    # 截取屏幕
    print("\n截取屏幕...")
    screenshot_path = vision.take_screenshot()
    print(f"✓ 截图已保存: {screenshot_path}")
    
    print("\n" + "=" * 50)
    print("视觉识别功能已就绪")
    print("需要提供按钮模板图像才能进行识别")
    print("=" * 50)


if __name__ == "__main__":
    main()
