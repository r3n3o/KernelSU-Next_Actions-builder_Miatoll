<div align="center">

# 🛡️ Miatoll NetHunter & KernelSU-Next Engine

**Enterprise-Grade Security Auditing & Kernel-Level Superuser Engine for Qualcomm Snapdragon 720G (SM6250 / Miatoll)**

[![CI/CD Build Pipeline](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%2FCD%20Build)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions)
[![Kernel Version](https://img.shields.io/badge/Kernel-Linux%204.14.357--openela-blue?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250)
[![Target Android](https://img.shields.io/badge/Android%20Target-16%20(crDroid%2016%20%2F%20LOS%2022.2)-green?style=for-the-badge&logo=android&logoColor=white)](https://crdroid.net)
[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-v3.3.0%20(Legacy%20UAPI)-red?style=for-the-badge&logo=roots&logoColor=white)](https://github.com/rifsxd/KernelSU-Next)
[![Architecture](https://img.shields.io/badge/Arch-ARM64%20(aarch64)-orange?style=for-the-badge&logo=arm&logoColor=white)](https://arm.com)
[![License](https://img.shields.io/badge/License-GPL--2.0-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

</div>

---

> [!WARNING]
> ### ⚖️ LEGAL DISCLAIMER & ETHICAL USAGE STATEMENT
> This custom kernel package integrates high-privilege kernel-level security auditing, packet injection, and hardware emulation capabilities. It is developed and distributed exclusively for **authorized educational research, professional penetration testing, hardware diagnostics, and defensive infrastructure auditing**. 
> 
> Executing wireless packet injection, unauthorized network interception, or HID payload execution against infrastructure, networks, or devices without explicit, written authorization from the owner is illegal under national and international cybercrime legislation (e.g., Computer Fraud and Abuse Act, GDPR, Cybersecurity Laws). The maintainers and contributors assume **no liability** for misuse or damages resulting from this software.

---

## 📑 Table of Contents

- [1. Hardware & Software Compatibility Matrix](#-1-hardware--software-compatibility-matrix)
- [2. Technical Architecture & Component Stack](#-2-technical-architecture--component-stack)
- [3. Deep-Dive Kernel Flags Breakdown (`defconfig`)](#-3-deep-dive-kernel-flags-breakdown-defconfig)
- [4. Step-by-Step Production Installation](#-4-step-by-step-production-installation)
- [5. Diagnostics, Logging & Disaster Recovery](#-5-diagnostics-logging--disaster-recovery)
- [6. Post-Installation Verification & Cheat Sheet](#-6-post-installation-verification--cheat-sheet)
- [7. Build System & Toolchain Specification](#-7-build-system--toolchain-specification)
- [8. Upstream Credits & Acknowledgments](#-8-upstream-credits--acknowledgments)

---

## 🖧 1. Hardware & Software Compatibility Matrix

This kernel is targeted and validated for the **Qualcomm SM6250 (Snapdragon 720G / ATOLL-AB)** SoC platform utilizing UFS storage controllers (`1d84000.ufshc`).

### 📱 Target Device Family (Xiaomi Miatoll Unified)

| Device Marketing Name | Codename | SoC | Storage Controller | Baseband / Region |
| :--- | :--- | :--- | :--- | :--- |
| **Xiaomi Redmi Note 9 Pro** | `joyeuse` | Snapdragon 720G | UFS 2.1 (`/dev/block/bootdevice`) | Global / EEA / LATAM |
| **Xiaomi Redmi Note 9S / 9 Pro** | `curtana` | Snapdragon 720G | UFS 2.1 (`/dev/block/bootdevice`) | Global / India |
| **POCO M2 Pro** | `gram` | Snapdragon 720G | UFS 2.1 (`/dev/block/bootdevice`) | Global / India |
| **Xiaomi Redmi Note 9 Pro Max** | `excalibur`| Snapdragon 720G | UFS 2.1 (`/dev/block/bootdevice`) | India |

### 💿 ROM & Operating System Compatibility

| Operating System / Base | Version / Android API | Status | Technical Notes |
| :--- | :--- | :--- | :--- |
| **crDroid Android** | **16.0 (Android 16 / SDK 36)** | 🟢 **Fully Supported** | Primary reference target; full namespace & PTY stability. |
| **LineageOS** | **22.2 (Android 16 / SDK 36)** | 🟢 **Fully Supported** | Tested with AOSP base and official Lineage recovery/TWRP. |
| **AOSP / Generic Custom ROMs** | **Android 15 / 16 (A15/A16)** | 🟢 **Supported** | Compatible with standard dynamic partition layout. |
| **Stock MIUI / HyperOS** | Any (Android 10 - 14) | 🔴 **Incompatible** | Proprietary Xiaomi display/camera drivers will bootloop. |
| **Legacy Custom ROMs** | Android 14 or lower | ⚠️ **Untested / Deprecated**| SELinux rules and init definitions tailored for A16. |

---

## 🏗️ 2. Technical Architecture & Component Stack

```
+===========================================================================+
|                     USERSPACE & SECURITY PLATFORMS                        |
+---------------------------------------------------------------------------+
|  Kali NetHunter KeX (XFCE4 GUI)  |  NetHunter CLI  |  Termux Native Chroot|
+----------------------------------+-----------------+----------------------+
|  KernelSU-Next Manager (v3.3.0)  |  Android Apps (Isolated Mount NS)      |
+===========================================================================+
|                      KERNELSPACE INTEGRATION LAYER                        |
+---------------------------------------------------------------------------+
|  [KernelSU-Next Driver v3.3.0]   |  Supercall Handlers & Syscall Intercept|
|  - UAPI Interface (2==2)         |  - Zero /system Partition Footprint    |
|  - App Profile Enforcement       |  - Root Isolated by App UID            |
+----------------------------------+----------------------------------------+
|  [Wireless Ingestion Engine]     |  [Hardware Gadget Subsystem]           |
|  - mac80211 / cfg80211 Injection |  - ConfigFS USB HID (/dev/hidg0, hidg1)|
|  - Minstrel HT Rate Control      |  - USB Mass Storage CD-ROM Emulation   |
+----------------------------------+----------------------------------------+
|  [Virtualization & Isolation]    |  [OTG External Drivers Subsystem]      |
|  - CONFIG_USER_NS / PID / NET_NS |  - Atheros (ath9k_htc, carl9170)       |
|  - System V IPC (CONFIG_SYSVIPC) |  - Realtek (rtl8187, rtl8812au/8xxxu)  |
|  - Loopback Device Loop Mounting |  - Ralink / MediaTek (rt2800usb, mt76) |
+===========================================================================+
|                  QUALCOMM SNAPDRAGON 720G HARDWARE (SM6250)               |
+===========================================================================+
```

---

## ⚙️ 3. Deep-Dive Kernel Flags Breakdown (`defconfig`)

The build pipeline injects a hardened, audited patchset directly into `arch/arm64/configs/vendor/xiaomi/miatoll_defconfig`.

```
===============================================================================
 CONFIGURATION FLAG              VALUE   SUBSYSTEM IMPACT & FUNCTION
===============================================================================
 CONFIG_KSU                      y       Enables KernelSU-Next core runtime
 CONFIG_KSU_MANUAL_HOOK          y       Deterministic manual syscall hooking
 CONFIG_NAMESPACES               y       Process isolation for Kali NetHunter
 CONFIG_UTS_NS                   y       Host/domain virtualization per chroot
 CONFIG_IPC_NS                   y       Inter-Process Comm virtualization
 CONFIG_USER_NS                  y       Unprivileged rootless container mapping
 CONFIG_PID_NS                   y       Process tree separation for chroot
 CONFIG_NET_NS                   y       Dedicated network stack per namespace
 CONFIG_SYSVIPC                  y       Shared memory/semaphores for multithreading
 CONFIG_SYSVIPC_SYSCTL           y       Userspace control for IPC allocations
 CONFIG_BLK_DEV_LOOP             y       Loop device mounting (ext4/img rootfs)
 CONFIG_USB_F_HID                y       USB Human Interface Device function
 CONFIG_USB_CONFIGFS_F_HID       y       ConfigFS HID endpoints (/dev/hidg*)
 CONFIG_USB_CONFIGFS_MASS_STORAGE y      DriveDroid bootable ISO/IMG emulation
 CONFIG_CFG80211                 y       Linux Wireless Configuration API
 CONFIG_MAC80211                 y       Generic 802.11 Protocol Stack (Injection)
 CONFIG_CFG80211_WEXT            y       Wireless Extensions API backward compat
 CONFIG_MAC80211_RC_MINSTREL_HT  y       High-throughput dynamic rate control
 CONFIG_ATH9K_HTC                y/m     Atheros AR9271 USB adapter support
 CONFIG_CARL9170                 y/m     Atheros AR9170 802.11n USB support
 CONFIG_RTL8187                  y/m     Realtek RTL8187L high-power Wi-Fi
 CONFIG_RTL8XXXU                 y/m     Realtek 802.11n modern USB driver
 CONFIG_RT2800USB                y/m     Ralink RT2870/RT3070/RT5370 wireless
 CONFIG_MT7601U                  y/m     MediaTek MT7601U Wi-Fi adapter
 CONFIG_USB_RTL8152              y/m     Realtek RTL8152/RTL8153 USB-to-LAN
 CONFIG_USB_NET_AX88179_178A     y/m     ASIX AX88179 Gigabit Ethernet OTG
 CONFIG_USB_NET_CDC_ETHER        y/m     USB CDC Ethernet standard adapter
 CONFIG_DVB_USB_RTL28XXU         y/m     RTL-SDR Software-Defined Radio Tuner
===============================================================================
```

---

## 📦 4. Step-by-Step Production Installation

### 📋 Pre-Flight Checklist
- [x] **Unlocked Bootloader**: The device must have its bootloader unlocked.
- [x] **Installed Custom Recovery**: OrangeFox Recovery (R11.1+) or Official TWRP (3.7.0+) installed.
- [x] **Battery Level**: Ensure the battery is charged to at least 50%.
- [x] **Backup**: Perform an explicit **NANDroid backup of `/boot` and `/dtbo` partitions** in recovery.

---

### Step 1: Download & Integrity Verification

Download the latest flashable ZIP artifact (`AK3-Miatoll-NetHunter-KSU`) from [GitHub Releases](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/releases) or GitHub Actions.

Verify the SHA-256 integrity hash on your workstation before flashing:

```bash
# On Linux / macOS
sha256sum Miatoll-NetHunter-Kernel.zip

# On Windows (PowerShell)
Get-FileHash .\Miatoll-NetHunter-Kernel.zip -Algorithm SHA256
```

---

### Step 2: Flashing via Recovery (AnyKernel3)

1. Reboot into recovery mode:
   ```bash
   adb reboot recovery
   ```
2. In OrangeFox / TWRP, navigate to **Backup** ➔ select **Boot** ➔ Swipe to backup.
3. Transfer the kernel ZIP to internal storage:
   ```bash
   adb push Miatoll-NetHunter-Kernel.zip /sdcard/
   ```
   *(Or flash directly via ADB Sideload: `adb sideload Miatoll-NetHunter-Kernel.zip`)*
4. Select `Miatoll-NetHunter-Kernel.zip` ➔ **Swipe to Confirm Flash**.
5. Wipe **Dalvik / ART Cache**.
6. Select **Reboot System**.

---

### Step 3: Install KernelSU-Next Manager APK

Once Android boots:
1. Download and install the matching **KernelSU-Next Manager APK (v3.3.0+)**.
2. Open the Manager app. It must report:
   * **State**: `Working`
   * **Version**: `3.3.0:KernelSU` (or higher)
   * **Mode**: `Non-GKI (Legacy)`
3. Navigate to **Superuser** ➔ Enable Root access individually for your target applications (e.g., `Termux`, `NetHunter`).

---

## 🚨 5. Diagnostics, Logging & Disaster Recovery

### 🩹 Scenario A: Bootloop / Soft-Brick Emergency Recovery

If the device hangs at the boot logo due to incompatible ROM modules or dirty system modifications, recover instantly without data loss:

1. Hold `Volume Down (-) + Power` to enter **Fastboot Mode**.
2. Connect to PC and flash your backed-up stock `boot.img` (or extract `boot.img` from your current ROM ZIP):
   ```bash
   fastboot flash boot boot.img
   fastboot reboot
   ```
3. The device will boot normally with the stock kernel.

---

### 📋 Scenario B: Extracting Recovery Logs for Bug Reporting

If the AnyKernel3 installer errors out during recovery installation:

```bash
# Extract AnyKernel3 runtime log
adb shell "cat /tmp/anykernel.log" > anykernel_install.log

# Extract recovery execution log
adb pull /tmp/recovery.log recovery.log
```

---

## 💻 6. Post-Installation Verification & Cheat Sheet

Verify all kernel security features directly via root shell (`su`) in Termux or KeX:

### 1. KernelSU-Next Core Driver Verification
```bash
su -c "uname -a; /data/adb/ksud -V; su -v"
```
*Expected Output:*
```text
Linux crDroid-joyeuse 4.14.357-openela-Stormbreaker-g8b4afb3dd59e ... aarch64
KernelSU-Next v3.3.0
3.3.0:KernelSU
```

---

### 2. USB HID BadUSB Hardware Nodes
```bash
su -c "ls -la /dev/hidg*"
```
*Expected Output:*
```text
crw------- 1 root root 241, 0 /dev/hidg0
crw------- 1 root root 241, 1 /dev/hidg1
```

---

### 3. Wireless Monitor Mode & Packet Injection (External USB OTG)
Connect an external adapter (e.g., Alfa AWUS036NHA / TP-Link TL-WN722N v1):
```bash
su -c "lsusb; ip link; airmon-ng start wlan1"
su -c "aireplay-ng --test wlan1mon"
```

---

### 4. Kali NetHunter KeX Desktop Manager Control
```bash
# Launch NetHunter XFCE4 graphical session on port 5901 (Display :1)
kex-start

# Terminate running KeX VNC desktop session
kex-stop

# Instant interactive CLI root terminal
kali
```

---

## 🛠️ 7. Build System & Toolchain Specification

The CI/CD build engine automates multi-stage cross-compilation on GitHub Actions runners (`ubuntu-22.04`):

| Build Parameter | Specification / Toolchain |
| :--- | :--- |
| **Host OS** | Ubuntu 22.04 LTS (x86_64) |
| **C/C++ Compiler** | Google Clang 6443078 (r383902) |
| **Linker** | `LD=ld.lld` (LLVM Integrated Linker) |
| **Cross Compilers** | AArch64 GCC 4.9 & ARM32 GCC 4.9 |
| **Kernel Base Source**| `crdroidandroid/android_kernel_xiaomi_sm6250` (Branch `16.0`) |
| **Target Architecture**| `ARCH=arm64` (`SUBARCH=arm64`) |
| **Packager** | AnyKernel3 with dynamic UFS block discovery |

---

## 🤝 8. Upstream Credits & Acknowledgments

* **Kernel Source Base**: [crDroid Android Team](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250) & [LineageOS](https://github.com/LineageOS)
* **KernelSU-Next Framework**: [rifsxd](https://github.com/rifsxd/KernelSU-Next) & [tiann](https://github.com/tiann/KernelSU)
* **Offensive Security NetHunter Project**: [Kali Linux NetHunter Team](https://www.kali.org)
* **AnyKernel3 Deployment Engine**: [osm0sis](https://github.com/osm0sis/AnyKernel3)
* **Community Contributors**: [The Miatoll Development Community](https://github.com/topics/miatoll)

---

<div align="center">
<b>Developed with ❤️ for the Cybersecurity and Open-Source Android Community</b><br>
<sub>Redmi Note 9 Pro | Redmi Note 9S | POCO M2 Pro | Redmi Note 9 Pro Max</sub>
</div>
