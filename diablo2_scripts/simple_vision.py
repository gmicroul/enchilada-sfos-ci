#!/usr/bin/env python3
"""
Diablo II 简单视觉识别
- 使用xdotool search功能查找窗口元素
- 不需要额外依赖
"""

import os
os.environ['DISPLAY'] = ':0'

import subprocess
import time
import re

def find_window():
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

def click_at(x, y):
    """点击指定坐标"""
    try:
        subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
        time.sleep(0.1)
        subprocess.run(["xdotool", "click", "1"], check=True)
        print(f"   ✓ 点击位置: ({x}, {y})")
    except Exception as e:
        print(f"   ⚠ 点击错误: {e}")

def click_relative(window, rel_x, rel_y):
    """点击相对于窗口的位置"""
    abs_x = window['x'] + rel_x
    abs_y = window['y'] + rel_y
    click_at(abs_x, abs_y)

def main():
    print("Diablo II 简单视觉识别")
    print("=" * 50)
    
    # 查找游戏窗口
    print("\n查找游戏窗口...")
    window = find_window()
    if window:
        print(f"✓ 窗口位置: ({window['x']}, {window['y']})")
        print(f"✓ 窗口尺寸: {window['width']}x{window['height']}")
    else:
        print("✗ 未找到游戏窗口")
        return
    
    # 测试点击
    print("\n测试点击...")
    print("点击窗口中心...")
    center_x = window['x'] + window['width'] // 2
    center_y = window['y'] + window['height'] // 2
    click_at(center_x, center_y)
    
    print("\n" + "=" * 50)
    print("简单视觉识别功能已就绪")
    print("可以基于窗口位置计算相对坐标")
    print("=" * 50)

if __name__ == "__main__":
    main()
