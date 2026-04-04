# 快速开始指南

## 🚀 5分钟快速上手

### 前置条件

- OnePlus 6T 设备
- 已解锁 Bootloader
- GitHub 账号
- 基础 Linux 命令行知识

### 步骤 1：准备代码

```bash
# 克隆或更新你的仓库
cd /home/user/.openclaw/workspace
git add .
git commit -m "Add Docker kernel support for OnePlus 6T"
git push origin main
```

### 步骤 2：触发 GitHub Actions 编译

1. 访问你的 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Build Hybris Boot Image" 工作流
4. 点击 "Run workflow"
5. 确认参数（默认即可）
6. 点击 "Run workflow" 按钮

### 步骤 3：等待编译完成

- 编译时间：约 2-4 小时
- 你会收到 GitHub 通知
- 编译完成后，Artifacts 会显示下载链接

### 步骤 4：下载产物

1. 在 Actions 页面找到完成的运行
2. 滚动到 "Artifacts" 部分
3. 下载：
   - `hybris-boot-fajita-5.0.0.73`
   - `kernel-config-fajita`

### 步骤 5：刷入设备

```bash
# 解压下载的文件
unzip hybris-boot-fajita-5.0.0.73.zip

# 进入 fastboot 模式
adb reboot bootloader

# 备份原 boot 分区（重要！）
fastboot boot boot.img

# 刷入新的 hybris-boot.img
fastboot flash boot hybris-boot.img

# 重启设备
fastboot reboot
```

### 步骤 6：验证 Docker 支持

```bash
# 等待设备启动后，通过 ADB 连接
adb shell

# 检查内核配置
zcat /proc/config.gz | grep -E "NAMESPACES|CGROUP|OVERLAY|VETH|BRIDGE"

# 应该看到类似这样的输出：
# CONFIG_NAMESPACES=y
# CONFIG_CGROUPS=y
# CONFIG_OVERLAY_FS=y
# CONFIG_VETH=y
# CONFIG_BRIDGE=y
# CONFIG_NETFILTER=y

# 测试 Docker
docker info
docker run --rm hello-world
```

## 🎉 完成！

现在你的 OnePlus 6T 已经支持 Docker 了！

## 📝 下一步

### 选项 A：部署 Waydroid + Flowpilot

```bash
# 安装 Waydroid
sudo zypper in waydroid

# 初始化
sudo waydroid init

# 启动
sudo waydroid session start

# 下载 Flowpilot APK
wget https://github.com/flowdriveai/flowpilot/releases/latest/download/flowpilot.apk

# 安装
waydroid app install flowpilot.apk
```

### 选项 B：启动 Docker 服务

```bash
# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  vision-ai:
    image: vision-ai:latest
    ports:
      - "8080:8080"
EOF

# 启动服务
docker-compose up -d
```

## 🔧 故障排除

### 编译失败

**问题**: GitHub Actions 编译失败

**解决方案**:
1. 检查 Actions 日志
2. 确认网络连接正常
3. 尝试重新触发编译

### 刷入失败

**问题**: fastboot flash 失败

**解决方案**:
```bash
# 检查设备连接
fastboot devices

# 重新进入 fastboot
adb reboot bootloader

# 检查分区
fastboot getvar current-slot
```

### Docker 无法启动

**问题**: docker info 报错

**解决方案**:
```bash
# 检查内核配置
zcat /proc/config.gz | grep DOCKER

# 重启 Docker 服务
sudo systemctl restart docker

# 检查日志
sudo journalctl -u docker
```

## 📚 更多信息

- 详细编译指南：[BUILD_HYBRIS_BOOT.md](BUILD_HYBRIS_BOOT.md)
- Docker 内核支持：[DOCKER_KERNEL_SUPPORT.md](DOCKER_KERNEL_SUPPORT.md)
- Docker 支持分析：[DOCKER_SUPPORT_ANALYSIS.md](DOCKER_SUPPORT_ANALYSIS.md)

## 💡 提示

1. **备份重要数据**：刷入前务必备份
2. **保持电量充足**：确保设备电量 > 50%
3. **使用稳定网络**：编译需要稳定网络
4. **耐心等待**：编译需要时间，不要中断

## 🆘 需要帮助？

- 查看 GitHub Issues
- 加入社区讨论
- 查阅相关文档

---

祝你编译顺利！🎊
