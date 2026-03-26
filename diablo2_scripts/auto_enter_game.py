#!/usr/bin/env python3
"""
自动进入 Diablo II 游戏
- 杀掉旧进程
- 启动游戏
- 点击 单一玩家 → OK → 普通
"""

import os
# 设置 DISPLAY
os.environ['DISPLAY'] = ':0'

from Xlib import X, display
from Xlib.ext import xtest
import subprocess
import time
import re

GAME_PATH = "/home/user/Downloads/Diablo2/Diablo II.exe"
WINDOW_WAIT = 30  # 等待窗口出现的最大秒数


def find_window():
    """找到 Diablo II 窗口位置"""
    try:
        result = subprocess.run(
            ["xdotool", "search", "--name", "Diablo II"],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            result = subprocess.run(
                ["xdotool", "search", "--class", "game.exe"],
                capture_output=True, text=True
            )
    except FileNotFoundError:
        return None

    if result.returncode != 0 or not result.stdout.strip():
        return None

    window_id = result.stdout.strip().split('\n')[0]
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


def click_at(x, y):
    """点击"""
    d = display.Display()
    xtest.fake_input(d, X.MotionNotify, x=x, y=y)
    d.flush()
    time.sleep(0.1)
    xtest.fake_input(d, X.ButtonPress, 1)
    d.flush()
    time.sleep(0.05)
    xtest.fake_input(d, X.ButtonRelease, 1)
    d.flush()


def press_enter():
    """按 Enter 键"""
    d = display.Display()
    keycode = d.keysym_to_keycode("Return")
    xtest.fake_input(d, X.KeyPress, keycode)
    d.flush()
    time.sleep(0.05)
    xtest.fake_input(d, X.KeyRelease, keycode)
    d.flush()


def click_single_player(window):
    """点击单一玩家"""
    # 窗口中心: (412, 1248)
    center_x = 412
    center_y = 1248

    print("点击 单一玩家...")
    click_at(center_x, center_y)
    time.sleep(2)  # 等待到角色选择画面


def click_character_ok(window):
    """点击角色 OK"""
    # 根据测试结果：绝对位置 (712, 1498)
    click_x = 712
    click_y = 1498

    print("点击 角色 OK...")
    click_at(click_x, click_y)
    time.sleep(2)  # 等待到难度选择画面


def click_normal_difficulty(window):
    """点击普通难度"""
    # 根据测试结果：窗口中心往上5像素，即 (412, 1243)
    center_x = 412
    center_y = 1243

    print("选择 普通难度...")
    click_at(center_x, center_y)
    time.sleep(3)  # 等待进入游戏画面


def enter_game():
    """完整进入游戏流程"""
    print("=" * 50)
    print("开始进入 Diablo II")
    print("=" * 50)

    # 0. 设置音频设备
    print("\n0. 设置音频设备...")
    subprocess.run(["pactl", "set-default-sink", "sink.primary_output"],
                   stderr=subprocess.DEVNULL)
    time.sleep(1)

    # 1. 杀掉旧进程
    print("\n1. 杀掉旧游戏进程...")
    subprocess.run(["pkill", "-9", "wine", "wine64", "wineserver"],
                   stderr=subprocess.DEVNULL)
    time.sleep(1)

    # 2. 启动游戏
    print("2. 启动游戏...")
    # 在后台启动
    subprocess.Popen(
        ["wine", GAME_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 3. 等待窗口
    print(f"3. 等待游戏窗口（最多{WINDOW_WAIT}秒）...")
    window = None
    for i in range(WINDOW_WAIT):
        window = find_window()
        if window:
            print(f"   ✓ 窗口已找到: ({window['x']}, {window['y']})")
            break
        time.sleep(1)
    else:
        print("   ✗ 未找到窗口，请检查游戏是否正常启动")
        return False

    # 4. 进入游戏流程
    print("\n4. 进入游戏...")
    time.sleep(20)  # 基础等待

    # 点击单一玩家上方30像素位置，跳过视频
    skip_x = 412
    skip_y = 1248 - 30  # 1218
    print(f"点击视频跳过位置: ({skip_x}, {skip_y}) x3")
    for i in range(3):
        click_at(skip_x, skip_y)
        time.sleep(0.3)

    time.sleep(2)  # 等待主菜单出现

    click_single_player(window)
    click_character_ok(window)
    click_normal_difficulty(window)

    # 5. 移动音频流到低延迟设备
    print("\n5. 移动音频流到低延迟设备...")
    time.sleep(2)  # 等待音频流创建
    try:
        # 查找游戏的音频流
        result = subprocess.run(
            ["pactl", "list", "sink-inputs"],
            capture_output=True, text=True
        )
        if "Blizzard North Diablo II" in result.stdout:
            # 提取sink-input ID
            import re
            match = re.search(r'Sink Input #(\d+)', result.stdout)
            if match:
                sink_input_id = match.group(1)
                # 移动到sink.primary_output (sink #0)
                subprocess.run(
                    ["pactl", "move-sink-input", sink_input_id, "0"],
                    stderr=subprocess.DEVNULL
                )
                print(f"   ✓ 音频流已移动到低延迟设备")
    except Exception as e:
        print(f"   ⚠ 音频流移动失败: {e}")

    print("\n" + "=" * 50)
    print("✓ 已进入游戏")
    print("现在喊'简单刷怪'，开始刷怪")
    print("=" * 50)

    return True


def main():
    print("Diablo II 自动进入脚本")
    print("=" * 50)
    print("执行操作：")
    print("  1. 杀掉旧进程")
    print("  2. 启动游戏")
    print("  3. 进入游戏（单一玩家 → 角色 → 普通）")
    print("=" * 50)

    try:
        success = enter_game()

        if success:
            print("\n现在可以运行刷怪脚本了：")
            print("  python3 diablo_farm_simple.py")

    except KeyboardInterrupt:
        print("\n\n收到停止信号")
    except Exception as e:
        print(f"\n\n错误: {e}")


if __name__ == "__main__":
    main()
