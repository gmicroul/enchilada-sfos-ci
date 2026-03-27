#!/usr/bin/env python3
"""
退出 Diablo II 游戏
- 按 ESC 打开菜单
- 按 Up 定位到"存储并离开游戏"
- 按 Enter 确认
- 点击退出按钮
"""

import os
os.environ['DISPLAY'] = ':0'

import subprocess
import time

def get_window_position():
    """获取游戏窗口位置"""
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
            
            return {"x": x, "y": y}
    except Exception as e:
        print(f"   ⚠ 获取窗口位置错误: {e}")
    
    return None

def press_key(key_name, duration=0.1):
    """按键盘按键"""
    try:
        subprocess.run(["xdotool", "key", key_name], check=True)
        time.sleep(duration)
    except Exception as e:
        print(f"   ⚠ 按键错误: {e}")


def click_at(x, y):
    """鼠标点击"""
    try:
        subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
        time.sleep(0.1)
        subprocess.run(["xdotool", "click", "1"], check=True)
        print(f"   ✓ 点击位置: ({x}, {y})")
    except Exception as e:
        print(f"   ⚠ 点击错误: {e}")


def exit_game():
    """退出游戏流程"""
    print("=" * 50)
    print("退出 Diablo II")
    print("=" * 50)

    # 获取窗口位置
    print("\n1. 获取游戏窗口位置...")
    window = get_window_position()
    if window:
        print(f"   ✓ 窗口位置: ({window['x']}, {window['y']})")
    else:
        print("   ✗ 未找到游戏窗口")
        return

    # 2. 按 ESC 打开菜单
    print("\n2. 按 ESC 打开菜单...")
    press_key("Escape")
    time.sleep(2)

    # 3. 按 Up 定位到"存储并离开游戏"
    print("3. 按 Up 定位到'存储并离开游戏'...")
    press_key("Up")
    time.sleep(2)

    # 4. 按 Enter 确认
    print("4. 按 Enter 确认...")
    press_key("Return")
    time.sleep(2)

    # 5. 点击退出按钮
    print("5. 点击退出按钮...")
    # 使用统一逻辑：游戏窗口右下角区域
    # 计算：(x + 400, y + 560)
    exit_x = window['x'] + 400
    exit_y = window['y'] + 560
    click_at(exit_x, exit_y)
    time.sleep(2)

    print("\n" + "=" * 50)
    print("✓ 已退出游戏")
    print("=" * 50)


def main():
    print("Diablo II 退出脚本")
    print("=" * 50)
    print("执行操作：")
    print("  1. 获取游戏窗口位置")
    print("  2. 按 ESC 打开菜单")
    print("  3. 按 Up 定位到'存储并离开游戏'")
    print("   4. 按 Enter 确认")
    print("  5. 点击退出按钮")
    print("=" * 50)

    try:
        exit_game()

    except KeyboardInterrupt:
        print("\n\n收到停止信号")
    except Exception as e:
        print(f"\n\n错误: {e}")


if __name__ == "__main__":
    main()
