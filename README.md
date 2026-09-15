<div align="center">

# 🛡️ Miatoll NetHunter & KernelSU-Next Engine

**Enterprise-Grade Security Auditing & Kernel-Level Superuser Engine for Qualcomm Snapdragon 720G (SM6250 / Miatoll)**

[![CI/CD Build Pipeline](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%2FCD%20Build)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions)
[![Kernel Version](https://img.shields.io/badge/Kernel-Linux%204.14.357--openela-blue?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250)
[![Target Android](https://img.shields.io/badge/Android%20Target-16%20(crDroid%2016%20%2F%20LOS%2022.2)-green?style=for-the-badge&logo=android&logoColor=white)](https://crdroid.net)
[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-v3.3.0%20(Legacy%20UAPI)-red?style=for-the-badge&logo=roots&logoColor=white)](https://github.com/rifsxd/KernelSU-Next)
[![Tested Device](https://img.shields.io/badge/Tested%20Device-Joyeuse%20Only-success?style=for-the-badge&logo=xiaomi&logoColor=white)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll#1-hardware--software-compatibility-matrix)
[![License](https://img.shields.io/badge/License-GPL--2.0-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

</div>

---

> [!CAUTION]
> ### ⚠️ DISCLAIMER & USER RESPONSIBILITY (USE ENTIRELY AT YOUR OWN RISK / BAJO SU PROPIO RIESGO)
> * **Your warranty is now void.** Modifying Android kernel components, rooting, and flashing low-level boot partitions carries inherent risks of bootloops, data loss, or bricking.
> * **You choose to use this software entirely at your own risk.** The maintainers and contributors assume **NO RESPONSIBILITY** for damaged hardware, unbootable devices, bootloops, bricked devices, lost data, corrupted storage, or compromised communications.
> * Always create a verified **NANDroid backup of your `/boot` and `/dtbo` partitions** in custom recovery before flashing any kernel.
>
> *(Español: Todo cambio o modificación se realiza bajo tu propia y absoluta responsabilidad. No nos hacemos responsables por daños materiales, pérdida de datos o dispositivos bloqueados).*

> [!IMPORTANT]
> ### 🔬 HARDWARE VALIDATION BOUNDARY: STRICTLY TESTED ON `joyeuse` ONLY
> This kernel release has been **compiled, flashed, debugged, and verified on real hardware EXCLUSIVELY on the Xiaomi Redmi Note 9 Pro (`joyeuse`)**.
> 
> Although the upstream kernel source tree is unified for the Qualcomm SM6250 (Miatoll) platform, other variant devices (**`curtana`** [Redmi Note 9S], **`gram`** [POCO M2 Pro], and **`excalibur`** [Redmi Note 9 Pro Max]) have **NOT BEEN TESTED** on hardware by the author. Flashing on non-`joyeuse` variants is done under your own discretion and testing responsibility.

> [!WARNING]
> ### ⚖️ LEGAL & ETHICAL AUDITING NOTICE
> This kernel enables raw 802.11 packet injection, monitor mode, HID keyboard emulation (BadUSB), and unprivileged container namespaces. It is distributed strictly for **authorized educational research, defensive security engineering, and penetration testing on hardware and networks you own or have explicit written permission to assess**. Unauthorized interception, disruption, or exploitation of computer systems is strictly prohibited by law.

---

## 📑 Table of Contents

- [1. Hardware & Software Compatibility Matrix](#-1-hardware--software-compatibility-matrix)
- [2. Technical Architecture & Feature Stack](#-2-technical-architecture--feature-stack)
- [3. Deep-Dive Kernel Flags Breakdown (`defconfig`)](#-3-deep-dive-kernel-flags-breakdown-defconfig)
- [4. Step-by-Step Production Installation](#-4-step-by-step-production-installation)
- [5. Userspace Setup (Kali NetHunter KeX & Termux)](#-5-userspace-setup-kali-nethunter-kex--termux)
- [6. Diagnostics, Logging & Disaster Recovery](#-6-diagnostics-logging--disaster-recovery)
- [7. Post-Installation Verification & Verification Commands](#-7-post-installation-verification--verification-commands)
- [8. Build System & Toolchain Specification](#-8-build-system--toolchain-specification)
- [9. License & Warranty Disclaimer](#-9-license--warranty-disclaimer)
- [10. Upstream Credits & Acknowledgments](#-10-upstream-credits--acknowledgments)

---

## 🖧 1. Hardware & Software Compatibility Matrix

Targeting the **Qualcomm Snapdragon 720G (SM6250 / ATOLL-AB)** architecture with UFS 2.1 storage controllers (`1d84000.ufshc`).

### 📱 Target Device Family (Xiaomi Miatoll)

| Device Marketing Name | Codename | SoC | Hardware Verification Status | Regional Models |
| :--- | :--- | :--- | :--- | :--- |
| **Xiaomi Redmi Note 9 Pro** | `joyeuse` | Snapdragon 720G | 🟢 **Verified & Tested on Physical Device** | Global / EEA / LATAM / RU |
| **Xiaomi Redmi Note 9S / 9 Pro** | `curtana` | Snapdragon 720G | 🟡 *Unified Source Base (Untested on Hardware)* | Global / India / China |
| **POCO M2 Pro** | `gram` | Snapdragon 720G | 🟡 *Unified Source Base (Untested on Hardware)* | India / Global |
| **Xiaomi Redmi Note 9 Pro Max** | `excalibur`| Snapdragon 720G | 🟡 *Unified Source Base (Untested on Hardware)* | India |

---

### 💿 ROM & Operating System Compatibility

| Operating System / Base | Version / Android API | Status | Technical Profile |
| :--- | :--- | :--- | :--- |
| **crDroid Android** | **16.0 (Android 16 / SDK 36)** | 🟢 **Fully Supported** | Primary reference ROM; full PTY & namespace stability. |
| **LineageOS** | **22.2 (Android 16 / SDK 36)** | 🟢 **Fully Supported** | Compatible with standard LineageOS A16 device tree. |
| **AOSP / Generic Custom ROMs** | **Android 15 / 16 (A15/A16)** | 🟢 **Supported** | Compatible with modern dynamic super partition layouts. |
| **Stock MIUI / HyperOS** | Any (Android 10 - 14) | 🔴 **Incompatible** | Proprietary Xiaomi display drivers will bootloop. |
| **Legacy Custom ROMs** | Android 14 or lower | ⚠️ **Deprecated** | SELinux policies tailored specifically for A16. |

---

## 🏗️ 2. Technical Architecture & Feature Stack

```
+=============================================================================+
|                       USERSPACE & SECURITY PLATFORMS                        |
+-----------------------------------------------------------------------------+
|  Kali NetHunter KeX (XFCE4 GUI)  |  NetHunter CLI     |  Termux Root chroot |
+----------------------------------+--------------------+---------------------+
|  KernelSU-Next Manager (v3.3.0)  |  Android Root Apps (Isolated Mount NS)   |
+=============================================================================+
|                        KERNELSPACE INTEGRATION LAYER                        |
+-----------------------------------------------------------------------------+
|  [KernelSU-Next Driver v3.3.0]   |  Supercall Handlers & Syscall Intercept  |
|  - UAPI Interface (2==2)         |  - Zero /system Partition Footprint      |
|  - App Profile Enforcement       |  - Root Isolation by App UID             |
+----------------------------------+------------------------------------------+
|  [Wireless Ingestion Engine]     |  [Hardware Gadget Subsystem]             |
|  - mac80211 / cfg80211 Injection |  - ConfigFS USB HID (/dev/hidg0, hidg1)  |
|  - Minstrel HT Rate Control      |  - USB Mass Storage CD-ROM Emulation     |
+----------------------------------+------------------------------------------+
|  [Virtualization & Isolation]    |  [OTG External Drivers Subsystem]        |
|  - CONFIG_USER_NS / PID / NET_NS |  - Atheros (ath9k_htc, carl9170)         |
|  - System V IPC (CONFIG_SYSVIPC) |  - Realtek (rtl8187, rtl8812au/8xxxu)    |
|  - Loopback Device Loop Mounting |  - Ralink / MediaTek (rt2800usb, mt76)   |
+=============================================================================+
|                    QUALCOMM SNAPDRAGON 720G HARDWARE (SM6250)               |
+=============================================================================+
```

### 🌟 Key Feature Highlights
* **Native KernelSU-Next v3.3.0**: Embedded into the kernel tree with manual legacy syscall hooks for pristine su management and complete invisibility to userspace root detection.
* **BadUSB & HID Injection**: Emulate USB keyboards and mice directly from your phone through `/dev/hidg0` and `/dev/hidg1`.
* **Wireless Packet Injection**: Full support for external Wi-Fi USB OTG adapters running in monitor mode and packet injection.
* **Full Linux Namespace Isolation**: Comprehensive `CONFIG_USER_NS`, `CONFIG_PID_NS`, `CONFIG_NET_NS`, and `CONFIG_IPC_NS` allowing full chroot and rootless container virtualization.
* **KeX Desktop Ready**: Integrated support for full XFCE4 desktop environments via TigerVNC on display `:1` (port `5901`).

---

## ⚙️ 3. Deep-Dive Kernel Flags Breakdown (`defconfig`)

The build pipeline injects a hardened, audited patchset directly into `arch/arm64/configs/vendor/xiaomi/miatoll_defconfig`:

```text
=================================================================================
 CONFIGURATION FLAG               VALUE   SUBSYSTEM IMPACT & FUNCTION
=================================================================================
 CONFIG_KSU                       y       Enables KernelSU-Next core runtime
 CONFIG_KSU_MANUAL_HOOK           y       Deterministic manual syscall hooking
 CONFIG_NAMESPACES                y       Process isolation for Kali NetHunter
 CONFIG_UTS_NS                    y       Host/domain virtualization per chroot
 CONFIG_IPC_NS                    y       Inter-Process Comm virtualization
 CONFIG_USER_NS                   y       Unprivileged rootless container mapping
 CONFIG_PID_NS                    y       Process tree separation for chroot
 CONFIG_NET_NS                    y       Dedicated network stack per namespace
 CONFIG_SYSVIPC                   y       Shared memory/semaphores for multithreading
 CONFIG_SYSVIPC_SYSCTL            y       Userspace control for IPC allocations
 CONFIG_BLK_DEV_LOOP              y       Loop device mounting (ext4/img rootfs)
 CONFIG_USB_F_HID                 y       USB Human Interface Device function
 CONFIG_USB_CONFIGFS_F_HID        y       ConfigFS HID endpoints (/dev/hidg*)
 CONFIG_USB_CONFIGFS_MASS_STORAGE y       DriveDroid bootable ISO/IMG emulation
 CONFIG_CFG80211                  y       Linux Wireless Configuration API
 CONFIG_MAC80211                  y       Generic 802.11 Protocol Stack (Injection)
 CONFIG_CFG80211_WEXT             y       Wireless Extensions API backward compat
 CONFIG_MAC80211_RC_MINSTREL_HT   y       High-throughput dynamic rate control
 CONFIG_ATH9K_HTC                 y/m     Atheros AR9271 USB adapter support
 CONFIG_CARL9170                  y/m     Atheros AR9170 802.11n USB support
 CONFIG_RTL8187                   y/m     Realtek RTL8187L high-power Wi-Fi
 CONFIG_RTL8XXXU                  y/m     Realtek 802.11n modern USB driver
 CONFIG_RT2800USB                 y/m     Ralink RT2870/RT3070/RT5370 wireless
 CONFIG_MT7601U                   y/m     MediaTek MT7601U Wi-Fi adapter
 CONFIG_USB_RTL8152               y/m     Realtek RTL8152/RTL8153 USB-to-LAN
 CONFIG_USB_NET_AX88179_178A      y/m     ASIX AX88179 Gigabit Ethernet OTG
 CONFIG_USB_NET_CDC_ETHER         y/m     USB CDC Ethernet standard adapter
 CONFIG_DVB_USB_RTL28XXU          y/m     RTL-SDR Software-Defined Radio Tuner
=================================================================================
```

---

## 📦 4. Step-by-Step Production Installation

### 📋 Pre-Flight Checklist
- [x] **Unlocked Bootloader**: The device must have its bootloader unlocked.
- [x] **Custom Recovery**: OrangeFox Recovery (R11.1+) or Official TWRP (3.7.0+) installed.
- [x] **Battery Level**: Minimum 50% battery charged.
- [x] **Verified Backup**: Perform an explicit **NANDroid backup of `/boot` and `/dtbo` partitions** in recovery.

---

### Step 1: Download & Integrity Verification

Download the flashable package (`Miatoll-NetHunter-Kernel.zip`) from [GitHub Releases](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/releases).

Verify SHA-256 hash before flashing:

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
2. In OrangeFox / TWRP, go to **Backup** ➔ select **Boot** and **DTBO** ➔ Swipe to backup.
3. Transfer the kernel ZIP to internal storage:
   ```bash
   adb push Miatoll-NetHunter-Kernel.zip /sdcard/
   ```
   *(Or flash directly via sideload: `adb sideload Miatoll-NetHunter-Kernel.zip`)*
4. In recovery: Select `Miatoll-NetHunter-Kernel.zip` ➔ **Swipe to Confirm Flash**.
5. Wipe **Dalvik / ART Cache**.
6. Select **Reboot System**.

---

### Step 3: Install KernelSU-Next Manager APK

Once Android boots:
1. Download and install the **[KernelSU-Next Manager APK (v3.3.0+)](https://github.com/rifsxd/KernelSU-Next/releases)**.
2. Open the Manager app and verify:
   * **State**: `Working`
   * **Version**: `3.3.0:KernelSU`
   * **Mode**: `Non-GKI (Legacy)`
3. Go to **Superuser** ➔ Enable Root access individually for your target applications (e.g., `Termux`, `NetHunter`).

---

## 🚀 5. Userspace Setup (Kali NetHunter KeX & Termux)

### Termux PTY / Android Linker Fix
On Android 16, Termux utilizes `LD_PRELOAD` which can conflict with Android's system dynamic linker when calling `/system/bin/su`. Ensure `unset LD_PRELOAD` is executed before calling root binaries:

```bash
# In Termux:
unset LD_PRELOAD
su
```

### NetHunter KeX Desktop Service Control
```bash
# Launch NetHunter XFCE4 graphical session (Display :1 / Port 5901)
kex-start

# Terminate running KeX VNC desktop session
kex-stop

# Instant interactive CLI root terminal
kali
```

---

## 🚨 6. Diagnostics, Logging & Disaster Recovery

### 🩹 Soft-Brick / Bootloop Emergency Recovery

If you ever encounter a bootloop due to conflicting Magisk/KernelSU modules or incompatible system modifications:

1. Hold `Volume Down (-) + Power` to enter **Fastboot Mode**.
2. Connect to PC and flash your backed-up stock `boot.img` (or extract `boot.img` from your current ROM ZIP):
   ```bash
   fastboot flash boot boot.img
   fastboot reboot
   ```
3. The device will boot immediately with the original kernel.

---

### 📋 Extracting Installation & Recovery Logs

If the installer encounters any issues in recovery:

```bash
# Extract AnyKernel3 runtime installation log
adb shell "cat /tmp/anykernel.log" > anykernel_install.log

# Extract recovery execution log
adb pull /tmp/recovery.log recovery.log
```

---

## 💻 7. Post-Installation Verification & Verification Commands

Verify all kernel subsystems directly from a root shell (`su`):

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

## 🛠️ 8. Build System & Toolchain Specification

The CI/CD build engine cross-compiles on GitHub Actions runners (`ubuntu-22.04`):

| Build Parameter | Specification / Toolchain |
| :--- | :--- |
| **Host Environment** | Ubuntu 22.04 LTS (x86_64) |
| **C/C++ Compiler** | Google Clang 6443078 (r383902) |
| **Linker** | `LD=ld.lld` (LLVM Integrated Linker) |
| **Cross Compilers** | AArch64 GCC 4.9 & ARM32 GCC 4.9 |
| **Kernel Base Source**| `crdroidandroid/android_kernel_xiaomi_sm6250` (Branch `16.0`) |
| **Target Architecture**| `ARCH=arm64` (`SUBARCH=arm64`) |
| **Packager** | AnyKernel3 with dynamic UFS block discovery |

---

## 📜 9. License & Warranty Disclaimer

This project is licensed under the **[GNU General Public License v2.0 (GPL-2.0)](LICENSE)**.

### Disclaimer of Warranty (GPLv2 Sections 11 & 12)
```text
BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY FOR THE PROGRAM,
TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE
COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF
ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE
DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
```

To review the complete license terms, please visit the [LICENSE](LICENSE) file.

---

## 🤝 10. Upstream Credits & Acknowledgments

* **Kernel Source Base**: [crDroid Android Team](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250) & [LineageOS](https://github.com/LineageOS)
* **KernelSU-Next Framework**: [rifsxd](https://github.com/rifsxd/KernelSU-Next) & [tiann](https://github.com/tiann/KernelSU)
* **Offensive Security NetHunter Project**: [Kali Linux NetHunter Team](https://www.kali.org)
* **AnyKernel3 Deployment Engine**: [osm0sis](https://github.com/osm0sis/AnyKernel3)
* **Community Contributors**: [The Miatoll Development Community](https://github.com/topics/miatoll)

---

<div align="center">
<b>Developed with ❤️ for the Cybersecurity and Open-Source Android Community</b><br>
<sub>Verified on Redmi Note 9 Pro (joyeuse) | Unified tree for SM6250</sub>
</div>
