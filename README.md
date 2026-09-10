# Miatoll NetHunter and KernelSU-Next Automated Build Pipeline

<div align="center">

[![Build Pipeline](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white&label=CI%2FCD%20Pipeline)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions)
[![Kernel Architecture](https://img.shields.io/badge/Architecture-ARM64%20%7C%20Linux%204.14-0052cc?style=flat-square&logo=linux&logoColor=white)](https://kernel.org)
[![Root Framework](https://img.shields.io/badge/Root-KernelSU--Next%20Legacy-0e8a16?style=flat-square&logo=android&logoColor=white)](https://github.com/rifsxd/KernelSU-Next)
[![Security Platform](https://img.shields.io/badge/Security-Kali%20NetHunter%20Ready-b60205?style=flat-square&logo=kalilinux&logoColor=white)](https://www.kali.org/docs/nethunter/)
[![License](https://img.shields.io/badge/License-GPL--2.0-blue?style=flat-square)](LICENSE)

<p align="center">
  Automated continuous integration and build framework for the Xiaomi Snapdragon 720G (SM6250 / Miatoll) platform.<br>
  Designed for wireless security auditing, KernelSU-Next root integration, USB HID emulation, and AnyKernel3 deployment.
</p>

</div>

---

## 1. System Overview

This repository hosts an automated continuous integration pipeline that compiles and packages an enhanced Linux 4.14 kernel for the Qualcomm Snapdragon 720G (`SM6250`) platform. The build environment injects native kernel-level support for penetration testing tools, wireless frame injection, USB hardware emulation, and KernelSU-Next superuser management.

### Key Subsystems

* **Kernel-Level Superuser**: Native integration of the KernelSU-Next driver directly into the kernel source tree, providing root control and bypassing user-space detection vectors.
* **Wireless Auditing Engine**: Full frame injection and monitor mode capabilities via `mac80211` and `cfg80211` wireless stacks.
* **Integrated Hardware Drivers**: Native compilation (`=y`) of external USB OTG network controller drivers, allowing immediate operation upon connection without external module dependencies.
* **Hardware Emulation Interface**: USB Gadget subsystem configured with HID keyboard and mouse function drivers for automated keystroke injection workflows.
* **Containerization and Isolation**: Full kernel namespace support and System V IPC primitives required for unprivileged chroot execution in Kali NetHunter.

---

## 2. Target Hardware Compatibility

The compiled kernel image targets the unified **Xiaomi Miatoll** platform and supports all regional hardware variants running AOSP, LineageOS, or crDroid based distributions:

| Device Codename | Commercial Designation | Processor (SoC) | Storage Technology | Partition Path |
| :--- | :--- | :--- | :--- | :--- |
| **`joyeuse`** | Xiaomi Redmi Note 9 Pro (Global / EU) | Qualcomm Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`curtana`** | Xiaomi Redmi Note 9S / 9 Pro (India) | Qualcomm Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`gram`** | POCO M2 Pro | Qualcomm Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`excalibur`** | Xiaomi Redmi Note 9 Pro Max | Qualcomm Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |

---

## 3. Kernel Configuration and Injected Flags

The automated build process injects the following configuration flags into `arch/arm64/configs/vendor/xiaomi/miatoll_defconfig`:

```ini
# KernelSU-Next and Probing Subsystem
CONFIG_KSU=y
CONFIG_KSU_DEBUG=n
CONFIG_KPROBES=y
CONFIG_HAVE_KPROBES=y
CONFIG_KRETPROBES=y

# Inter-Process Communication
CONFIG_SYSVIPC=y
CONFIG_SYSVIPC_SYSCTL=y

# Dynamic Module Support
CONFIG_MODULES=y
CONFIG_MODULE_UNLOAD=y

# Wireless Stack and Packet Injection
CONFIG_WIRELESS=y
CONFIG_CFG80211=y
CONFIG_MAC80211=y
CONFIG_CFG80211_WEXT=y

# Integrated OTG Network Controllers (Built-in)
CONFIG_WLAN_VENDOR_ATH=y
CONFIG_ATH_CARDS=y
CONFIG_ATH9K_HTC=y
CONFIG_WLAN_VENDOR_REALTEK=y
CONFIG_RTL8187=y
CONFIG_WLAN_VENDOR_RALINK=y
CONFIG_RT2X00=y
CONFIG_RT2800USB=y

# USB Gadget and HID Emulation
CONFIG_USB_G_ANDROID=y
CONFIG_USB_F_HID=y
CONFIG_USB_CONFIGFS_F_HID=y

# Namespaces and Container Isolation
CONFIG_NAMESPACES=y
CONFIG_USER_NS=y
CONFIG_PID_NS=y
CONFIG_NET_NS=y
CONFIG_BLK_DEV_LOOP=y
```

---

## 4. Deployment and Installation

### Method A: Custom Recovery Installation (Recommended)

1. **Backup Existing Partitions**: Boot into TWRP or OrangeFox and generate a partition backup of `/boot` and `/dtbo`.
2. **Retrieve Distribution Package**: Download the `AK3-Miatoll-NetHunter-KSU` artifact from the latest successful GitHub Actions workflow run.
3. **Flash Archive**: Transfer `Miatoll-NetHunter-Kernel.zip` to the device storage and execute the flash procedure via Recovery.
4. **Post-Installation Setup**: Boot into Android and install the KernelSU-Next Manager application to manage root permissions and access control.

### Method B: Non-Destructive RAM Boot (Fastboot)

To evaluate the kernel image without writing to physical flash memory:

```bash
# Extract the compiled image from the zip archive
adb reboot bootloader
fastboot boot Image.gz-dtb
```

---

## 5. Build Environment and Toolchain

The continuous integration pipeline is executed on GitHub Actions runners with the following toolchain parameters:

* **Host Environment**: Ubuntu 22.04 LTS x86_64
* **Swap Space**: 10 GB Virtual Memory Allocation
* **C/C++ Compiler**: Google AOSP Clang toolchain (`clang-6443078` / LLVM 10.0 based)
* **Cross-Compilers**:
  * GNU Binutils aarch64 (`aarch64-linux-android-4.9`)
  * GNU Binutils arm32 (`arm-linux-androideabi-4.9`)
* **Linker**: LLVM Linker (`ld.lld`)
* **Deployment Packaging**: AnyKernel3 template with static block mapping targeting `/dev/block/bootdevice/by-name/boot`

---

## 6. Credits and Open Source Attributions

* **Maintainer and Lead Developer**: [r3n3o](https://github.com/r3n3o) - Hardware testing, kernel customization, and pipeline maintenance.
* **AI Architecture and Automation**: **Antigravity** (Google DeepMind) - Continuous integration engineering, static AnyKernel3 delivery architecture, and build diagnostics.
* **Research and Diagnostics**: **NotebookLM** - Architecture analysis, partition resolution research, and subsystem documentation.
* **Upstream Communities and Projects**:
  * [osm0sis](https://github.com/osm0sis) - AnyKernel3 Universal Android Kernel Packaging System.
  * [crDroid Android](https://github.com/crdroidandroid) - Base kernel source tree for Qualcomm SM6250.
  * [tiann](https://github.com/tiann) and [KernelSU-Next Team](https://github.com/rifsxd/KernelSU-Next) - Next-generation kernel-based superuser solution.
  * [Offensive Security](https://www.offensive-security.com/) - Kali NetHunter mobile penetration testing platform.
  * [LineageOS Project](https://github.com/LineageOS) - Prebuilt compiler toolchains and Android kernel patches.

---

<div align="center">
  <sub>Licensed under the GNU General Public License v2.0. Developed for the Android security community.</sub>
</div>
