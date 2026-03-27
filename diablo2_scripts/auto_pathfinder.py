#!/usr/bin/env python3
"""
Diablo II 自动寻路功能
- 计算从当前位置到目标位置的路径
- 自动移动到目标位置
- 简单的避障逻辑
"""

import os
os.environ['DISPLAY'] = ':0'

import subprocess
import time
import math

class AutoPathfinder:
    """自动寻路类"""
    
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.center_x = self.window_width // 2
        self.center_y = self.window_height // 2
        self.move_speed = 0.5  # 移动持续时间（秒）
        self.move_distance = 100  # 每次移动的像素距离
    
    def press_key(self, key_name, duration=0.1):
        """按键盘按键"""
        try:
            subprocess.run(["xdotool", "key", key_name], check=True)
            time.sleep(duration)
        except Exception as e:
            print(f"   ⚠ 按键错误: {e}")
    
    def move_to_direction(self, direction, duration=0.5):
        """向指定方向移动"""
        direction_keys = {
            'up': 'Up',
            'down': 'Down',
            'left': 'Left',
            'right': 'Right',
            'up-left': 'Up',
            'up-right': 'Up',
            'down-left': 'Down',
            'down-right': 'Down'
        }
        
        key = direction_keys.get(direction)
        if key:
            self.press_key(key, duration)
    
    def calculate_direction(self, target_x, target_y):
        """计算移动方向"""
        # 目标相对于中心的位置
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        
        # 计算角度
        angle = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle)
        
        # 确定主要方向
        if abs(dx) > abs(dy):
            # 水平移动为主
            if dx > 0:
                return 'right'
            else:
                return 'left'
        else:
            # 垂直移动为主
            if dy > 0:
                return 'down'
            else:
                return 'up'
    
    def move_to_target(self, target_x, target_y, max_steps=20):
        """移动到目标位置"""
        print(f"开始移动到目标位置: ({target_x}, {target_y})")
        
        for step in range(max_steps):
            # 计算当前距离
            dx = target_x - self.center_x
            dy = target_y - self.center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 如果距离足够近，停止移动
            if distance < 50:
                print(f"   ✓ 已到达目标位置 (距离: {distance:.1f})")
                return True
            
            # 计算移动方向
            direction = self.calculate_direction(target_x, target_y)
            
            # 移动
            print(f"   步骤 {step+1}/{max_steps}: 方向={direction}, 距离={distance:.1f}")
            self.move_to_direction(direction, self.move_speed)
            
            # 等待移动完成
            time.sleep(0.2)
        
        print(f"   ⚠ 达到最大步数，可能未完全到达目标")
        return False
    
    def walk_straight(self, direction, duration=2.0):
        """向指定方向直线行走"""
        print(f"向 {direction} 方向直线行走 {duration} 秒")
        self.move_to_direction(direction, duration)
    
    def walk_to_exit(self, duration=30.0):
        """向城外行走"""
        print("向城外行走...")
        # 假设城外在东北方向
        self.walk_straight('up-right', duration)


def main():
    print("Diablo II 自动寻路")
    print("=" * 50)
    
    pathfinder = AutoPathfinder()
    
    # 测试：移动到屏幕右上角
    print("\n测试1: 移动到屏幕右上角")
    pathfinder.move_to_target(700, 100)
    
    time.sleep(2)
    
    # 测试：移动到屏幕左下角
    print("\n测试2: 移动到屏幕左下角")
    pathfinder.move_to_target(100, 500)
    
    time.sleep(2)
    
    # 测试：移动到屏幕中心
    print("\n测试3: 移动到屏幕中心")
    pathfinder.move_to_target(pathfinder.center_x, pathfinder.center_y)
    
    print("\n" + "=" * 50)
    print("测试完成")


if __name__ == "__main__":
    main()
