# Hybris Boot Image 编译指南

## GitHub Actions 自动编译

### 快速开始

1. **触发编译**
   - 访问 GitHub Actions 页面
   - 选择 "Build Hybris Boot Image" 工作流
   - 点击 "Run workflow"
   - 输入设备代号（默认：fajita）
   - 输入SailfishOS版本（默认：5.0.0.73）

2. **下载产物**
   - 编译完成后，在 Artifacts 中下载：
     - `hybris-boot-fajita-5.0.0.73`
     - `kernel-config-fajita`

3. **刷入设备**
   ```bash
   # 进入 fastboot 模式
   adb reboot bootloader

   # 备份原 boot 分区
   fastboot boot boot.img

   # 刷入新的 hybris-boot.img
   fastboot flash boot hybris-boot.img

   # 重启
   fastboot reboot
   ```

## 本地编译（如果需要）

### 前置条件

```bash
# 安装依赖
sudo apt-get install -y \
  git \
  wget \
  curl \
  unzip \
  build-essential \
  ccache \
  python3 \
  python3-pip \
  openjdk-8-jdk \
  repo \
  rsync \
  bc \
  bison \
  flex \
  g++-multilib \
  gcc-multilib \
  lib32ncurses5-dev \
  lib32z1-dev \
  libssl-dev \
  libxml2-utils \
  xsltproc \
  zip
```

### 编译步骤

```bash
# 1. 克隆源码
mkdir -p ~/android
cd ~/android
repo init -u https://github.com/LineageOS/android.git -b lineage-17.1
repo sync -c -j4

# 2. 应用 Docker 内核补丁
cd kernel/oneplus/sdm845/
cp arch/arm64/configs/fajita_defconfig arch/arm64/configs/fajita_defconfig.bak

# 添加 Docker 内核选项（见下方配置）
vim arch/arm64/configs/fajita_defconfig

# 3. 编译
cd ~/android
source build/envsetup.sh
lunch fajita-userdebug
make bootimage -j$(nproc)

# 4. 提取 boot.img
cp out/target/product/fajita/boot.img ~/hybris-boot.img
```

## Docker 内核配置

### 必需的内核选项

```bash
# Namespaces（命名空间）
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_IPC_NS=y
CONFIG_PID_NS=y
CONFIG_NET_NS=y
CONFIG_USER_NS=y

# Cgroups（控制组）
CONFIG_CGROUPS=y
CONFIG_CGROUP_FREEZER=y
CONFIG_CGROUP_PIDS=y
CONFIG_CGROUP_DEVICE=y
CONFIG_CPUSETS=y
CONFIG_CGROUP_CPUACCT=y
CONFIG_MEMCG=y
CONFIG_BLK_CGROUP=y

# 存储驱动
CONFIG_OVERLAY_FS=y
CONFIG_DM_THIN_PROVISIONING=y
CONFIG_MD=y

# 网络功能
CONFIG_VETH=y
CONFIG_BRIDGE=y
CONFIG_NETFILTER=y
CONFIG_NF_NAT=y
CONFIG_NF_NAT_IPV4=y
CONFIG_NF_NAT_IPV6=y
CONFIG_IP_NF_IPTABLES=y
CONFIG_IP6_NF_IPTABLES=y

# 安全功能
CONFIG_KEYS=y
CONFIG_SECCOMP=y
```

## 验证 Docker 支持

### 在设备上验证

```bash
# 检查内核配置
zcat /proc/config.gz | grep -E "NAMESPACES|CGROUP|OVERLAY|VETH|BRIDGE"

# 或者
cat /boot/config-$(uname -r) | grep -E "NAMESPACES|CGROUP|OVERLAY|VETH|BRIDGE"

# 测试 Docker
docker info
docker run --rm hello-world
```

## 故障排除

### 编译失败

1. **空间不足**
   ```bash
   # 清理构建缓存
   make clean
   ccache -C
   ```

2. **依赖缺失**
   ```bash
   # 重新安装依赖
   sudo apt-get install -y $(cat requirements.txt)
   ```

3. **Java 版本问题**
   ```bash
   # 设置 Java 8
   export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
   export PATH=$JAVA_HOME/bin:$PATH
   ```

### 刷入失败

1. **设备未解锁**
   ```bash
   # 解锁 Bootloader
   fastboot oem unlock
   ```

2. **分区错误**
   ```bash
   # 检查分区
   fastboot getvar current-slot
   fastboot getvar partition-type:boot
   ```

3. **恢复原镜像**
   ```bash
   # 从备份恢复
   fastboot flash boot boot-backup.img
   ```

## 相关资源

- [SailfishOS HADK 文档](https://docs.sailfishos.org/HADK/)
- [OnePlus 6T 内核源码](https://github.com/OnePlusSE/android_kernel_oneplus_sdm845)
- [Docker 内核要求](https://docs.docker.com/engine/install/linux-postinstall/#kernel-requirements)
- [Hybris 项目](https://github.com/mer-hybris)

## 注意事项

⚠️ **重要提醒**：
- 编译需要大量磁盘空间（40-60GB）
- 编译时间较长（2-4小时）
- 需要稳定的网络连接
- 刷入前务必备份原 boot 镜像
- 可能会导致设备变砖（谨慎操作）

## 下一步

编译完成后，可以：
1. 刷入设备测试 Docker 支持
2. 部署 Waydroid
3. 安装 Flowpilot
4. 构建巡查机器人系统
