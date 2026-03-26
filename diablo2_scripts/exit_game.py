#!/usr/bin/env python3
"""
退出 Diablo II 游戏
- 按 ESC 打开菜单
- 按 Up 定位到"存储并离开游戏"
- 按 Enter 确认
- 点击退出按钮
"""

import os
# 设置 DISPLAY
os.environ['DISPLAY'] = ':0'

import subprocess
import time

def press_key(key_name):
    """按键盘按键"""
    try:
        subprocess.run(["xdotool", "key", key_name], check=True)
    except Exception as e:
        print(f"   ⚠ 按键错误: {e}")


def click_at(x, y):
    """鼠标点击"""
    try:
        subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
        time.sleep(0.1)
        subprocess.run(["xdotool", "click", "1"], check=True)
    except Exception as e:
        print(f"   ⚠ 点击错误: {e}")


def exit_game():
    """退出游戏流程"""
    print("=" * 50)
    print("退出 Diablo II")
    print("=" * 50)

    print("\n1. 按 ESC 打开菜单...")
    press_key("Escape")
    time.sleep(2)

    print("2. 按 Up 定位到'存储并离开游戏'...")
    press_key("Up")
    time.sleep(2)

    print("3. 按 Enter 确认...")
    press_key("Return")
    time.sleep(2)

    print("4. 点击退出按钮 (412, 1498)...")
    click_at(412, 1498)
    time.sleep(2)

    print("\n" + "=" * 50)
    print("✓ 已退出游戏")
    print("=" * 50)


def main():
    print("Diablo II 退出脚本")
    print("=" * 50)
    print("执行操作：")
    print("  1. 按 ESC 打开菜单")
    print("  2. 按 Up 定位到'存储并离开游戏'")
    print("  3. 按 Enter 确认")
    print("  4. 点击退出按钮")
    print("=" * 50)

    try:
        exit_game()

    except KeyboardInterrupt:
        print("\n\n收到停止信号")
    except Exception as e:
        print(f"\n\n错误: {e}")


if __name__ == "__main__":
    main()
