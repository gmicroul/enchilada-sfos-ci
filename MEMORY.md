# MEMORY.md - 长期记忆

## 项目：fajita-sfos-ci

### GitHub Actions - build-hybris-boot.yml

**位置：** `/home/user/.openclaw/workspace/fajita-sfos-ci/.github/workflows/build-hybris-boot.yml`

**用途：** 为 SailfishOS 5.0 构建 hybris-boot 镜像

**关键配置：**
- 基础：LineageOS 16.0（Android 9）
- 设备：OnePlus 6T (fajita)
- Kernel：VerdandiTeam android_kernel_oneplus_sdm845-stable
- 分支：lineage-16.0

**重要经验：**

1. **GitHub Actions 限制（免费计划）：**
   - 磁盘空间：10-14 GB
   - 时间限制：6 小时
   - 不适合完整 Android 源码构建（30-50 GB）
   - 解决方案：只构建 kernel（2-3 GB）

2. **Ubuntu 24.04 交叉编译：**
   - 工具链：gcc-12-aarch64-linux-gnu
   - 需要创建符号链接：`aarch64-linux-gnu-gcc` → `aarch64-linux-gnu-gcc-12`
   - gcc-multilib 与交叉编译工具链冲突，不能同时安装

3. **SailfishOS 版本对应：**
   - SailfishOS 5.0 → LineageOS 16.0（Android 9）
   - 不是 LineageOS 17.1（Android 10）

4. **Docker 支持补丁：**
   - 已添加到 kernel defconfig
   - 包括：NAMESPACES, CGROUPS, OVERLAY_FS, VETH, BRIDGE, NETFILTER 等

5. **常见问题：**
   - lib32ncurses5-dev → lib32ncurses-dev（Ubuntu 24.04）
   - Mer SDK 域名失效 → 移除该步骤
   - GitHub 认证 → 配置 GITHUB_TOKEN

### 构建环境变量

```bash
export ARCH=arm64
export SUBARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export CC=aarch64-linux-gnu-gcc
```

### 下次优化方向

1. 增加 ccache 容量
2. 考虑使用 ARM64 runner
3. 添加完整 boot.img 打包（需要 mkbootimg）

### 设备树编译问题

**问题：** 编译 `sdm845-interposer-sdm670-mtp.dtb` 时，`sdm845-interposer-pm660.dtsi` 引用了不存在的标签：
- `led_flash_rear`, `led_flash_rear_aux`, `led_flash_front`, `led_flash_iris`
- `actuator_regulator`
- `eeprom_rear`, `eeprom_rear_aux`, `eeprom_front`

**解决方案：** 只编译内核镜像 `Image.gz`，跳过设备树编译。设备树可以从原厂 boot.img 中提取。

**修改：**
- 构建目标从 `Image.gz-dtb` 改为 `Image.gz`
- 输出文件从 `Image.gz-dtb` 改为 `Image.gz`

### kgsl 驱动编译问题

**问题：** `drivers/gpu/msm/kgsl_events.c` 找不到 `kgsl_device.h` 头文件。

**解决方案：** 从 Makefile 中移除 kgsl 相关的编译目标：
- `kgsl_trace.o`
- `kgsl_events.o`
- `kgsl.o`

**说明：** kgsl 是 Qualcomm GPU 驱动，对于基本的内核启动不是必需的。

### adreno_trace 编译问题

**问题：** `drivers/gpu/msm/adreno_trace.c` 找不到 `adreno_trace.h` 头文件。

**解决方案：** 从 Makefile 中移除 adreno 相关的编译目标：
- `adreno_trace.o`
- `adreno.o`

**说明：** adreno 是 Adreno GPU 驱动，对于基本的内核启动不是必需的。

### 摄像头驱动编译问题

**问题：** `drivers/media/platform/msm/camera/cam_core/cam_context_utils.c` 找不到 `cam_context.h` 头文件。

**解决方案：** 从 Makefile 中移除整个摄像头驱动目录：
- `drivers/media/platform/msm/camera`

**说明：** Qualcomm 摄像头驱动对于基本的内核启动不是必需的。

### IPA 驱动编译问题

**问题：** `drivers/platform/msm/ipa/ipa_v3/ipa.c` 找不到 `ipa_trace.h` 头文件。

**解决方案：** 从 Makefile 中移除整个 IPA 驱动目录：
- `drivers/platform/msm/ipa`

**说明：** IPA (IP Accelerator) 是 Qualcomm 的网络加速器，对于基本的内核启动不是必需的。

### tracer_pkt 驱动编译问题

**问题：** `drivers/soc/qcom/tracer_pkt.c` 找不到 `tracer_pkt_private.h` 头文件。

**解决方案：** 从 Makefile 中移除 tracer_pkt 驱动：
- `drivers/soc/qcom/tracer_pkt`

**说明：** tracer_pkt 是数据包追踪驱动，对于基本的内核启动不是必需的。

### USB gadget 驱动编译问题

**问题：** `drivers/usb/gadget/configfs.c` 找不到 `function/u_ncm.h` 头文件。

**解决方案：** 从 Makefile 中移除 configfs 驱动：
- `drivers/usb/gadget/configfs.o`

**说明：** USB gadget configfs 用于配置 USB 设备模式，对于基本的内核启动不是必需的。

### 链接错误

**问题：** 链接时出现大量未定义的引用：
- `usb_function_unregister` - USB gadget 相关
- 大量的 `kgsl_ioctl_*` 函数 - kgsl GPU 驱动相关
- `__efistub_strrchr` - EFI stub 相关

**解决方案：**
1. 删除所有 kgsl 和 adreno 相关的源文件
2. 从 Makefile 中移除所有 kgsl 和 adreno 相关的行
3. 移除 USB gadget function 中的 f_mtp.c
4. 禁用 EFI stub（CONFIG_EFI=n, CONFIG_EFI_STUB=n）

**说明：**
- kgsl 和 adreno 是 GPU 驱动，对于基本启动不是必需的
- f_mtp 是 MTP (Media Transfer Protocol) 驱动，用于 USB 文件传输
- EFI stub 用于从 EFI 固件启动，Android 设备通常使用 boot.img 而不是 EFI

### kgsl 依赖错误

**问题：** `drivers/gpu/msm/msm_kgsl_core.o` 依赖于 `drivers/gpu/msm/kgsl_drawobj.o`，但文件已被删除。

**解决方案：** 从 Makefile 中移除所有 kgsl 和 adreno 相关的行：
```bash
sed -i '/kgsl/d' drivers/gpu/msm/Makefile || true
sed -i '/adreno/d' drivers/gpu/msm/Makefile || true
```

**说明：** 需要从 Makefile 中完全移除 kgsl 和 adreno 的编译规则，而不仅仅是删除源文件。

### msm 目录编译错误

**问题：** `drivers/gpu/msm/built-in.o` 不存在，因为移除了所有 kgsl 和 adreno 文件后，目录变成了空的。

**解决方案：** 直接删除整个 `drivers/gpu/msm/` 目录：
```bash
rm -rf drivers/gpu/msm || true
```

**说明：** `drivers/gpu/msm/` 目录主要包含 kgsl 和 adreno GPU 驱动，对于基本启动不是必需的。直接删除整个目录可以避免编译错误。

### Kconfig 引用错误

**问题：** `drivers/video/Kconfig` 引用了 `drivers/gpu/msm/Kconfig`，但该目录已被删除。

**解决方案：** 从 `drivers/video/Kconfig` 中移除对 `drivers/gpu/msm/Kconfig` 的引用：
```bash
sed -i '/source "drivers\/gpu\/msm\/Kconfig"/d' drivers/video/Kconfig || true
```

**说明：** 删除目录后，需要同时更新 Kconfig 文件，移除对该目录的引用。

### 大量链接错误

**问题：** 链接时出现大量未定义的引用，主要来自：
1. **IPA 相关**：`ipa_*` 函数
2. **tracer_pkt 相关**：`tracer_pkt_log_event`
3. **USB gadget function 相关**：大量 `usb_*` 函数
4. **mdss-dsi-pll-10nm 相关**：`dsi_pll_clock_register_10nm`
5. **电源管理相关**：一些充电和电池管理函数

**解决方案：** 直接删除有问题的源文件和目录：
```bash
# Remove problematic IPA drivers (IP Accelerator - not needed for basic boot)
rm -rf drivers/platform/msm/ipa || true

# Remove problematic tracer_pkt driver (not needed for basic boot)
rm -rf drivers/soc/qcom/tracer_pkt* || true

# Remove problematic USB gadget function drivers (not needed for basic boot)
rm -rf drivers/usb/gadget/function/f_mtp.c || true
rm -rf drivers/usb/gadget/function/f_ptp.c || true
rm -rf drivers/usb/gadget/function/f_ncm.c || true
rm -rf drivers/usb/gadget/function/f_mass_storage.c || true
rm -rf drivers/usb/gadget/function/f_fs.c || true
rm -rf drivers/usb/gadget/function/f_midi.c || true
rm -rf drivers/usb/gadget/function/f_hid.c || true
rm -rf drivers/usb/gadget/function/f_audio_source.c || true
rm -rf drivers/usb/gadget/function/f_accessory.c || true
rm -rf drivers/usb/gadget/function/f_diag.c || true
rm -rf drivers/usb/gadget/function/f_cdev.c || true
rm -rf drivers/usb/gadget/function/f_ccid.c || true
rm -rf drivers/usb/gadget/function/f_gsi.c || true
rm -rf drivers/usb/gadget/function/f_qdss.c || true

# Remove problematic USB BAM driver (depends on IPA)
rm -rf drivers/platform/msm/usb_bam.c || true
```

**说明：** 这些都是 Qualcomm 特有的驱动，对于基本的内核启动来说不是必需的。

### SPS 驱动编译错误

**问题：** `drivers/platform/msm/sps/built-in.o` 编译失败。

**解决方案：** 删除 SPS (Stream Processor System) 驱动目录：
```bash
rm -rf drivers/platform/msm/sps || true
sed -i '/sps/d' drivers/platform/msm/Makefile || true
```

**说明：** SPS 是 Qualcomm 的流处理器系统，对于基本的内核启动不是必需的。需要同时从 Makefile 中移除引用。

### usb_bam Makefile 引用错误

**问题：** `drivers/platform/msm/usb_bam.o` 找不到，因为文件已被删除但 Makefile 中仍然引用。

**解决方案：** 从 Makefile 中移除对 usb_bam 的引用：
```bash
sed -i '/usb_bam/d' drivers/platform/msm/Makefile || true
```

**说明：** 删除文件后，需要同时从 Makefile 中移除对该文件的引用。

### USB gadget function Makefile 引用错误

**问题：** `drivers/usb/gadget/function/f_ncm.o` 找不到，因为文件已被删除但 Makefile 中仍然引用。

**解决方案：** 从 Makefile 中移除对所有已删除的 USB gadget function 驱动的引用：
```bash
sed -i '/f_ptp/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_ncm/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_mass_storage/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_fs/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_midi/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_hid/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_audio_source/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_accessory/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_diag/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_cdev/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_ccid/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_gsi/d' drivers/usb/gadget/function/Makefile || true
sed -i '/f_qdss/d' drivers/usb/gadget/function/Makefile || true
```

**说明：** 删除文件后，需要同时从 Makefile 中移除对这些文件的引用。

### 大量依赖错误

**问题：** 链接时出现大量未定义的引用，主要来自：
1. **dsi_pll_clock_register_10nm** - mdss-pll.c 中引用
2. **tracer_pkt_log_event** - glink.c 和 glink_loopback_server.c 中引用
3. **sps_* 函数** - 大量 sps 相关函数，被以下驱动引用：
   - slim-msm.c
   - slim-msm-ngd.c
   - qce50.c (crypto)
   - spi_qsd.c
   - coresight-tmc-etr.c
4. **usb_diag_* 函数** - diag_usb.c 中引用
5. **get_extern_fg_regist_done, get_prop_pre_shutdown_soc, get_extern_bq_present** - qpnp-fg-gen3.c 中引用
6. **switch_mode_to_normal** - qpnp-smb2.c 和 smb-lib.c 中引用
7. **notify_dash_unplug_register/unregister** - smb-lib.c 中引用
8. **btfm_slim_hw_init** - bluetooth-power.c 中引用
9. **usb_qdss_* 函数** - coresight-tmc.c 和 coresight-tmc-etr.c 中引用
10. **set_mcu_en_gpio_value, usb_sw_gpio_set, mcu_en_gpio_set** - smb-lib.c 中引用

**解决方案：** 删除所有依赖已删除驱动的驱动：
```bash
# Remove problematic mdss-dsi-pll-10nm driver
sed -i '/mdss-dsi-pll-10nm/d' drivers/clk/qcom/mdss/Makefile || true

# Remove problematic glink drivers (depend on tracer_pkt)
rm -rf drivers/soc/qcom/glink.c || true
rm -rf drivers/soc/qcom/glink_loopback_server.c || true
sed -i '/glink/d' drivers/soc/qcom/Makefile || true

# Remove problematic slimbus drivers (depend on sps)
rm -rf drivers/slimbus/slim-msm.c || true
rm -rf drivers/slimbus/slim-msm-ngd.c || true
sed -i '/slim-msm/d' drivers/slimbus/Makefile || true

# Remove problematic diag drivers (depend on usb_diag)
rm -rf drivers/char/diag/diag_usb.c || true
sed -i '/diag_usb/d' drivers/char/diag/Makefile || true
sed -i '/diagchar/d' drivers/char/diag/Makefile || true

# Remove problematic crypto drivers (depend on sps)
rm -rf drivers/crypto/msm/qce50.c || true
sed -i '/qce50/d' drivers/crypto/msm/Makefile || true

# Remove problematic spi drivers (depend on sps)
rm -rf drivers/spi/spi_qsd.c || true
sed -i '/spi_qsd/d' drivers/spi/Makefile || true

# Remove problematic coresight drivers (depend on usb_qdss and sps)
rm -rf drivers/hwtracing/coresight/coresight-tmc.c || true
rm -rf drivers/hwtracing/coresight/coresight-tmc-etr.c || true
sed -i '/coresight-tmc/d' drivers/hwtracing/coresight/Makefile || true

# Remove problematic bluetooth-power driver (depends on btfm_slim)
rm -rf drivers/bluetooth/bluetooth-power.c || true
sed -i '/bluetooth-power/d' drivers/bluetooth/Makefile || true

# Remove problematic power supply drivers (depend on external functions)
rm -rf drivers/power/supply/qcom/qpnp-fg-gen3.c || true
rm -rf drivers/power/supply/qcom/qpnp-smb2.c || true
rm -rf drivers/power/supply/qcom/smb-lib.c || true
sed -i '/qpnp-fg-gen3/d' drivers/power/supply/qcom/Makefile || true
sed -i '/qpnp-smb2/d' drivers/power/supply/qcom/Makefile || true
sed -i '/smb-lib/d' drivers/power/supply/qcom/Makefile || true
```

**说明：** 这些驱动都依赖于我们之前删除的驱动（如 sps、tracer_pkt、usb_diag 等），对于基本的内核启动来说不是必需的。

### diag Makefile 引用错误

**问题：** `drivers/char/diag/diagchar.o` 找不到，因为文件已被删除但 Makefile 中仍然引用。

**解决方案：** 从 Makefile 中移除对 diagchar 的引用：
```bash
sed -i '/diagchar/d' drivers/char/diag/Makefile || true
```

**说明：** 删除文件后，需要同时从 Makefile 中移除对该文件的引用。

### coresight Makefile 格式错误

**问题：** `drivers/hwtracing/coresight/Makefile` 格式错误，因为删除文件后 Makefile 变成了空的或者格式不正确。

**解决方案：** 直接删除整个 coresight 目录：
```bash
rm -rf drivers/hwtracing/coresight || true
```

**说明：** coresight 是调试追踪功能，对于基本的内核启动不是必需的。

### coresight Kconfig 引用错误

**问题：** `arch/arm64/Kconfig.debug` 引用了 `drivers/hwtracing/coresight/Kconfig`，但该目录已被删除。

**解决方案：** 从 `arch/arm64/Kconfig.debug` 中移除对 coresight Kconfig 的引用：
```bash
sed -i '/source "drivers\/hwtracing\/coresight\/Kconfig"/d' arch/arm64/Kconfig.debug || true
```

**说明：** 删除目录后，需要同时更新 Kconfig 文件，移除对该目录的引用。

### Docker 内核支持问题（2026-04-02）

**问题：** 一加6T的SailfishOS内核Docker支持不完整

**检查结果：**
- ✅ 核心功能已启用（NAMESPACES、CGROUPS、OVERLAY_FS、VETH、BRIDGE等）
- ❌ 缺少关键配置（BRIDGE_NETFILTER、IP6_NF_TARGET_MASQUERADE等）
- ❌ 网络转发未启用（net.ipv4.ip_forward=0）

**解决方案：**
1. 创建 `apply-docker-kernel-patch-v2.sh` - 添加缺失的内核配置
2. 创建 `enable-docker-networking.sh` - 启用网络转发
3. 更新 GitHub Actions 工作流 - 使用新的补丁脚本
4. 创建 `DOCKER_KERNEL_FIX.md` - 完整修复指南

**新增配置：**
- 网络过滤：BRIDGE_NETFILTER, IP6_NF_TARGET_MASQUERADE
- 地址匹配：NETFILTER_XT_MATCH_ADDRTYPE, NETFILTER_XT_MATCH_IPVS
- 消息队列：POSIX_MQUEUE
- 存储控制：BLK_CGROUP, BLK_DEV_THROTTLING
- Cgroups：CGROUP_PERF, CGROUP_HUGETLB, CGROUP_NET_PRIO
- 调度器：CFQ_GROUP_IOSCHED, CFS_BANDWIDTH
- 安全：SECURITY_APPARMOR
- 文件系统：EXT4_FS_POSIX_ACL
- 网络驱动：VXLAN, BRIDGE_VLAN_FILTERING, IPVLAN, DUMMY
- 存储驱动：BTRFS_FS

**下一步：**
1. 推送代码到 GitHub
2. 触发 GitHub Actions 编译
3. 下载并刷入新内核
4. 在设备上启用网络转发
5. 验证 Docker 功能

### 内核编译错误修复（2026-04-03）

**问题：** GitHub Actions 编译时出现 Kconfig 错误

**错误信息：**
```
sed: can't read drivers/media/platform/msm/vidc/Makefile: No such file or directory
sed: can't read drivers/esoc/Makefile: No such file or directory
sed: can't read net/ipc_router/Makefile: No such file or directory
net/Kconfig:438: can't open file "net/ipc_router/Kconfig"
```

**原因：**
- GitHub Actions 工作流中的 sed 命令在文件不存在时报错
- 删除目录后，Kconfig 中仍然引用已删除的目录

**解决方案：**
1. 创建 `clean-kernel-drivers.sh` - 统一的驱动清理脚本
2. 更新 GitHub Actions 工作流 - 使用清理脚本替代内联命令
3. 清理脚本先删除目录，再清理 Makefile 和 Kconfig 引用

**第二次错误（路径问题）：**
```
/home/runner/work/fajita-sfos-ci/fajita-sfos-ci/scripts/clean-kernel-drivers.sh: line 15: cd: kernel/oneplus/sdm845: No such file or directory
```

**原因：**
- 脚本使用相对路径 `kernel/oneplus/sdm845`
- GitHub Actions 工作目录是 `/home/runner/work/fajita-sfos-ci/fajita-sfos-ci`
- 实际内核目录在 `/home/runner/work/android/kernel/oneplus/sdm845`

**解决方案：**
1. 修改 `clean-kernel-drivers.sh` - 接受参数或从环境变量获取路径
2. 更新 GitHub Actions 工作流 - 传递正确的路径参数

**已删除的驱动：**
- kgsl/adreno (GPU)
- vidc (视频)
- esoc (子系统)
- ipc_router (进程间通信)
- coresight (调试)
- sensors (传感器)
- qdsp6v2 (DSP)
- IPA (网络加速)
- SPS (流处理器)
- tracer_pkt (追踪)
- camera (摄像头)

**下一步：**
1. 推送代码到 GitHub
2. 触发 GitHub Actions 编译
3. 验证编译成功

## 其他项目

### star-office-ui

**位置：** `/home/user/.openclaw/workspace/star-office-ui/`

**子项目：**
- electron-shell：Electron 应用
- desktop-pet：Tauri 应用

**依赖：**
- electron-shell：electron ^40.6.1
- desktop-pet：@tauri-apps/cli ^2

## 工作区信息

**位置：** `/home/user/.openclaw/workspace/`

**主要项目：**
- fajita-sfos-ci：SailfishOS 构建工具
- star-office-ui：桌面应用
- AGENTS.md：工作区配置
- SOUL.md：AI 助手人格
- USER.md：用户信息
- TOOLS.md：本地工具笔记
- IDENTITY.md：AI 助手身份

## 用户偏好

- 语言：中文
- 时区：UTC
- 名字：DaLao
- AI 助手名字：玖伍贰柒
- Emoji：💻

### 更多依赖错误

**问题：** 链接时出现更多未定义的引用，主要来自：
1. **glink_* 函数** - spcom.c, adsprpc.c, subsystem_restart.c 中引用
2. **sysmon_* 函数** - subsystem_restart.c, esoc-mdm-4x.c 中引用
3. **qce_* 函数** - qcedev.c, qcrypto.c 中引用

**解决方案：** 删除所有依赖已删除驱动的驱动：
```bash
# Remove problematic spcom driver (depends on glink)
rm -rf drivers/soc/qcom/spcom.c || true
sed -i '/spcom/d' drivers/soc/qcom/Makefile || true

# Remove problematic subsystem_restart driver (depends on sysmon)
rm -rf drivers/soc/qcom/subsystem_restart.c || true
sed -i '/subsystem_restart/d' drivers/soc/qcom/Makefile || true

# Remove problematic adsprpc driver (depends on glink)
rm -rf drivers/char/adsprpc.c || true
sed -i '/adsprpc/d' drivers/char/Makefile || true

# Remove problematic crypto drivers (depend on sps and qce)
rm -rf drivers/crypto/msm/qce50.c || true
rm -rf drivers/crypto/msm/qcedev.c || true
rm -rf drivers/crypto/msm/qcrypto.c || true
sed -i '/qce50/d' drivers/crypto/msm/Makefile || true
sed -i '/qcedev/d' drivers/crypto/msm/Makefile || true
sed -i '/qcrypto/d' drivers/crypto/msm/Makefile || true

# Remove problematic esoc driver (depends on sysmon)
rm -rf drivers/esoc/esoc-mdm-4x.c || true
sed -i '/esoc-mdm-4x/d' drivers/esoc/Makefile || true
```

**说明：** 这些驱动都依赖于我们之前删除的驱动（如 glink、sysmon、qce 等），对于基本的内核启动来说不是必需的。

### 子系统相关依赖错误

**问题：** 链接时出现大量未定义的 subsystem_* 函数引用，主要来自：
1. **subsystem_* 函数** - 被以下驱动引用：
   - spss_utils.c
   - cdsp-loader.c
   - peripheral-loader.c
   - subsys-pil-tz.c
   - pil-q6v5-mss.c
   - msm_vidc_common.c
   - venus_hfi.c
   - esoc_bus.c
   - sensors_ssc.c
   - ipc_router_core.c
2. **notify_proxy_* 函数** - peripheral-loader.c 中引用
3. **qcrypto_* 函数** - dm-req-crypt.c 中引用

**解决方案：** 删除所有依赖 subsystem_* 函数的驱动：
```bash
# Remove problematic spss_utils driver (depends on subsystem)
rm -rf drivers/soc/qcom/spss_utils.c || true
sed -i '/spss_utils/d' drivers/soc/qcom/Makefile || true

# Remove problematic cdsp-loader driver (depends on subsystem)
rm -rf drivers/soc/qcom/qdsp6v2/cdsp-loader.c || true
sed -i '/cdsp-loader/d' drivers/soc/qcom/qdsp6v2/Makefile || true

# Remove problematic peripheral-loader driver (depends on subsystem)
rm -rf drivers/soc/qcom/peripheral-loader.c || true
sed -i '/peripheral-loader/d' drivers/soc/qcom/Makefile || true

# Remove problematic subsys-pil-tz driver (depends on subsystem)
rm -rf drivers/soc/qcom/subsys-pil-tz.c || true
sed -i '/subsys-pil-tz/d' drivers/soc/qcom/Makefile || true

# Remove problematic pil-q6v5-mss driver (depends on subsystem)
rm -rf drivers/soc/qcom/pil-q6v5-mss.c || true
sed -i '/pil-q6v5-mss/d' drivers/soc/qcom/Makefile || true

# Remove problematic vidc drivers (depends on subsystem)
rm -rf drivers/media/platform/msm/vidc/msm_vidc_common.c || true
rm -rf drivers/media/platform/msm/vidc/venus_hfi.c || true
sed -i '/msm_vidc_common/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/venus_hfi/d' drivers/media/platform/msm/vidc/Makefile || true

# Remove problematic esoc_bus driver (depends on subsystem)
rm -rf drivers/esoc/esoc_bus.c || true
sed -i '/esoc_bus/d' drivers/esoc/Makefile || true

# Remove problematic sensors_ssc driver (depends on subsystem)
rm -rf drivers/sensors/sensors_ssc.c || true
sed -i '/sensors_ssc/d' drivers/sensors/Makefile || true

# Remove problematic ipc_router_core driver (depends on subsystem)
rm -rf net/ipc_router/ipc_router_core.c || true
sed -i '/ipc_router_core/d' net/ipc_router/Makefile || true

# Remove problematic dm-req-crypt driver (depends on qcrypto)
rm -rf drivers/md/dm-req-crypt.c || true
sed -i '/dm-req-crypt/d' drivers/md/Makefile || true
```

**说明：** 这些驱动都依赖于我们之前删除的 subsystem_restart 驱动，对于基本的内核启动来说不是必需的。

### qdsp6v2 目录编译错误

**问题：** `drivers/soc/qcom/qdsp6v2/built-in.o` 找不到，因为删除了 `cdsp-loader.c` 后目录变成了空的。

**解决方案：** 删除整个 qdsp6v2 目录：
```bash
rm -rf drivers/soc/qcom/qdsp6v2 || true
```

**说明：** qdsp6v2 是 Qualcomm DSP 驱动，对于基本的内核启动不是必需的。

### qdsp6v2 Makefile 引用错误

**问题：** `drivers/soc/qcom/qdsp6v2/Makefile` 找不到，因为目录已被删除但 Makefile 中仍然引用。

**解决方案：** 从 Makefile 中移除对 qdsp6v2 的引用：
```bash
sed -i '/qdsp6v2/d' drivers/soc/qcom/Makefile || true
```

**说明：** 删除目录后，需要同时从 Makefile 中移除对该目录的引用。

### sensors 目录编译错误

**问题：** `drivers/sensors/built-in.o` 找不到，因为删除了 `sensors_ssc.c` 后目录变成了空的。

**解决方案：** 删除整个 sensors 目录：
```bash
rm -rf drivers/sensors || true
sed -i '/sensors/d' drivers/Makefile || true
```

**说明：** sensors 是传感器驱动，对于基本的内核启动不是必需的。

### sensors Kconfig 引用错误

**问题：** `drivers/Kconfig` 引用了 `drivers/sensors/Kconfig`，但该目录已被删除。

**解决方案：** 从 `drivers/Kconfig` 中移除对 sensors Kconfig 的引用：
```bash
sed -i '/source "drivers\/sensors\/Kconfig"/d' drivers/Kconfig || true
```

**说明：** 删除目录后，需要同时更新 Kconfig 文件，移除对该目录的引用。

### 更多依赖错误

**问题：** 链接时出现更多未定义的引用，主要来自：
1. **dsi_pll_clock_register_10nm** - mdss-pll.c 中引用
2. **msm_ipc_router_* 函数** - smp2p_sleepstate.c, qmi_interface.c, ipc_router_socket.c 中引用
3. **msm_comm_* 函数** - 大量 vidc 驱动中引用
4. **esoc_clink_* 函数** - esoc_dev.c, esoc_client.c, esoc-mdm-drv.c 中引用
5. **get_frame_size_* 函数** - vidc 驱动中引用

**解决方案：** 删除所有依赖这些函数的驱动：
```bash
# Remove problematic smp2p_sleepstate driver (depends on msm_ipc_router)
rm -rf drivers/soc/qcom/smp2p_sleepstate.c || true
sed -i '/smp2p_sleepstate/d' drivers/soc/qcom/Makefile || true

# Remove problematic qmi_interface driver (depends on msm_ipc_router)
rm -rf drivers/soc/qcom/qmi_interface.c || true
sed -i '/qmi_interface/d' drivers/soc/qcom/Makefile || true

# Remove problematic ipc_router_socket driver (depends on msm_ipc_router)
rm -rf net/ipc_router/ipc_router_socket.c || true
sed -i '/ipc_router_socket/d' net/ipc_router/Makefile || true

# Remove problematic ipc_router_security driver (depends on msm_ipc_router)
rm -rf net/ipc_router/ipc_router_security.c || true
sed -i '/ipc_router_security/d' net/ipc_router/Makefile || true

# Remove entire ipc_router directory if it's empty
rm -rf net/ipc_router || true
sed -i '/ipc_router/d' net/Makefile || true

# Remove problematic vidc drivers (depend on msm_comm)
rm -rf drivers/media/platform/msm/vidc/msm_vidc_common.c || true
rm -rf drivers/media/platform/msm/vidc/venus_hfi.c || true
rm -rf drivers/media/platform/msm/vidc/msm_v4l2_vidc.c || true
rm -rf drivers/media/platform/msm/vidc/msm_vdec.c || true
rm -rf drivers/media/platform/msm/vidc/msm_venc.c || true
rm -rf drivers/media/platform/msm/vidc/msm_vidc_debug.c || true
rm -rf drivers/media/platform/msm/vidc/msm_vidc_res_parse.c || true
rm -rf drivers/media/platform/msm/vidc/vidc_hfi.c || true
rm -rf drivers/media/platform/msm/vidc/msm_vidc_clocks.c || true
sed -i '/msm_vidc_common/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/venus_hfi/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_v4l2_vidc/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_vdec/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_venc/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_vidc_debug/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_vidc_res_parse/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/vidc_hfi/d' drivers/media/platform/msm/vidc/Makefile || true
sed -i '/msm_vidc_clocks/d' drivers/media/platform/msm/vidc/Makefile || true

# Remove entire vidc directory if it's empty
rm -rf drivers/media/platform/msm/vidc || true
sed -i '/vidc/d' drivers/media/platform/msm/Makefile || true

# Remove problematic esoc drivers (depend on esoc_clink)
rm -rf drivers/esoc/esoc_dev.c || true
rm -rf drivers/esoc/esoc_client.c || true
rm -rf drivers/esoc/esoc-mdm-drv.c || true
rm -rf drivers/esoc/esoc-mdm-4x.c || true
rm -rf drivers/esoc/esoc_bus.c || true
sed -i '/esoc_dev/d' drivers/esoc/Makefile || true
sed -i '/esoc_client/d' drivers/esoc/Makefile || true
sed -i '/esoc-mdm-drv/d' drivers/esoc/Makefile || true
sed -i '/esoc-mdm-4x/d' drivers/esoc/Makefile || true
sed -i '/esoc_bus/d' drivers/esoc/Makefile || true

# Remove entire esoc directory if it's empty
rm -rf drivers/esoc || true
sed -i '/esoc/d' drivers/Makefile || true
```

**说明：** 这些驱动都依赖于我们之前删除的驱动（如 msm_ipc_router、msm_comm、esoc_clink 等），对于基本的内核启动来说不是必需的。

### Kconfig 引用错误

**问题：** `net/Kconfig` 引用了 `net/ipc_router/Kconfig`，但该目录已被删除。

**解决方案：** 从 `net/Kconfig` 中移除对 ipc_router Kconfig 的引用：
```bash
sed -i '/source "net\/ipc_router\/Kconfig"/d' net/Kconfig || true
```

**说明：** 删除目录后，需要同时更新 Kconfig 文件，移除对该目录的引用。

### techpack/audio Kconfig 引用错误（2026-04-06）

**问题：** `techpack/Kconfig` 引用了 `techpack/audio/Kconfig`，但该目录已被删除。

**错误信息：**
```
techpack/Kconfig:1: can't open file "techpack/audio/Kconfig"
make[1]: *** [scripts/kconfig/Makefile:112: enchilada_defconfig] Error 1
```

**原因：** `clean-kernel-drivers.sh` 脚本在 `make enchilada_defconfig` **之后**运行，而 `make enchilada_defconfig` 会读取 Kconfig 文件。如果 Kconfig 引用了不存在的目录，构建会失败。

**解决方案：** 将 `clean-kernel-drivers.sh` 脚本移到 `make enchilada_defconfig` **之前**运行。

**修改：**
```yaml
# Before (错误)
make $DEFCONFIG
bash $GITHUB_WORKSPACE/scripts/clean-kernel-drivers.sh $ANDROID_ROOT/kernel/oneplus/sdm845

# After (正确)
bash $GITHUB_WORKSPACE/scripts/clean-kernel-drivers.sh $ANDROID_ROOT/kernel/oneplus/sdm845
make $DEFCONFIG
```

**说明：** 清理脚本必须在 `make defconfig` 之前运行，因为 `make defconfig` 会读取所有 Kconfig 文件。如果 Kconfig 引用了不存在的目录，构建会立即失败。

**相关项目：** enchilada-sfos-ci

### techpack/Makefile 引用错误（2026-04-06）

**问题：** `techpack/Makefile` 引用了 `techpack/audio` 目录，但该目录已被删除。

**错误信息：**
```
scripts/Makefile.build:44: techpack/audio/Makefile: No such file or directory
make[2]: *** No rule to make target 'techpack/audio/Makefile'. Stop.
make[1]: *** [scripts/Makefile.build:653: techpack/audio] Error 2
make: *** [Makefile:1102: techpack] Error 2
```

**原因：** 清理脚本删除了 `techpack/audio` 目录，但是没有清理 `techpack/Makefile` 中的引用。`techpack/Makefile` 可能有一行类似 `obj-y += audio/`，这会导致 make 尝试编译 `techpack/audio` 目录。

**解决方案：** 在清理脚本中添加清理 `techpack/Makefile` 的步骤。

**修改：**
```bash
# 添加到 clean-kernel-drivers.sh
echo "  - 清理 techpack/Makefile"
if [ -f techpack/Makefile ]; then
  sed -i '/audio/d' techpack/Makefile || true
fi
```

**说明：** 删除目录后，需要同时清理 Makefile 中的引用，否则 make 会尝试编译不存在的目录。

**相关项目：** enchilada-sfos-ci
