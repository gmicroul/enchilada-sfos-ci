# Diablo II 自动刷怪脚本

## 快速开始

### 推荐版本：简单刷怪脚本

```bash
cd /home/user/.openclaw/workspace/diablo2_scripts
python3 diablo_farm_simple.py
```

**使用步骤：**
1. 手动启动游戏，进到野外城外有怪的地方
2. 在桌面终端运行脚本
3. 按 Enter 开始
4. 每 3 分钟自动停止
5. 手动重启游戏（杀掉 wine 进程，重新进到野外）
6. 按 Enter 继续下一轮

## 脚本说明

### diablo_farm_simple.py ⭐ 推荐

**描述：** 简单版刷怪脚本，不带视觉识别，纯随机移动

**策略：**
- F8 冰雹 → 施展 2 次
- F7 瞬移 → 施展 1 次
- 随机走动 → 3 步（在屏幕中央区域周围）
- 每 3 分钟结束

**优点：**
- 简单稳定，不会误判
- 不会走到山脚卡住
- 适合有怪的野外区域

### diablo_farm_safe.py

**描述：** 带视觉识别的安全刷怪脚本

**特点：**
- 使用颜色识别找到角色位置
- 自动往东北方向走出城
- 视觉探索 NPC 和怪物

**注意：**
- 可能误判雇佣兵导致来回走动
- 角色容易走到山脚下卡住

### move_to_exit.py

**描述：** 让角色走到城外

**使用：**
```bash
python3 move_to_exit.py
```

角色会往东北方向走最多 30 秒，按 Ctrl+C 可提前停止。

### exit_game.py

**描述：** 退出游戏并保存

**使用：**
```bash
python3 exit_game.py
```

**步骤：**
1. 按 ESC 打开菜单
2. 按 Up 定位到"存储并离开游戏"
3. 按 Enter 确认
4. 点击退出按钮

每个步骤停留 2 秒。

### 工具脚本

- **check_windows.py** - 检查当前 Diablo II 窗口信息
- **find_window_class.sh** - 手动获取窗口类名

## 游戏启动

```bash
cd /home/user/Downloads/Diablo2
bash /home/user/.openclaw/workspace/Diablo2-openclaw.sh
```

或直接运行：
```bash
wine "Diablo II.exe"
```

## 杀掉游戏进程

```bash
pkill -9 wine wine64 wineserver
```

## 窗口信息参考

最新测试窗口信息：
- Window ID: 0x4200003
- WM_NAME: "Diablo II"
- WM_CLASS: ("game.exe" "game.exe")
- 绝对位置: (12, 948)
- 尺寸: 800x600

## 技能配置

- **F8** - 冰雹（施展 2 次）
- **F7** - 瞬移（施展 1 次）

可在脚本中修改 `SKILL_ICE` 和 `SKILL_TELEPORT` 常量。

## 注意事项

1. 确保 xdotool 已安装：`sudo apt install xdotool`
2. 脚本必须在桌面终端运行（OpenClaw 后台环境无法访问显示）
3. 手动进到野外/有怪的地方再运行脚本
4. 每 3 分钟需要手动重启游戏循环
5. 不要在角色选择界面运行脚本

## 开发历史

- 04:26-05:54 - 初始自动化测试
- 07:00-08:20 - 刷怪脚本开发与优化
- 最终方案 - 简单随机移动版本（稳定可用）
- 13:00-13:24 - 退出游戏脚本开发，学习正确的保存退出流程
- 18:00-18:20 - 音频优化，强制使用低延迟音频设备解决声音卡顿问题
