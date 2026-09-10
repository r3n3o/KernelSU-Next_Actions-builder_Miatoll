# Miatoll NetHunter & KernelSU-Next Kernel

[![Build Status](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=flat-square&label=Build)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions)
[![Kernel](https://img.shields.io/badge/Kernel-Linux%204.14%20(SM6250)-0052cc?style=flat-square)](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250)
[![Root](https://img.shields.io/badge/Root-KernelSU--Next-0e8a16?style=flat-square)](https://github.com/rifsxd/KernelSU-Next)
[![Security](https://img.shields.io/badge/Security-Kali%20NetHunter-b60205?style=flat-square)](https://www.kali.org)

Automated continuous integration pipeline building a Kali NetHunter and KernelSU-Next enabled Linux 4.14 kernel for Xiaomi SM6250 devices, packaged as a flashable AnyKernel3 zip.

---

## Supported Devices

Unified build for the Xiaomi Snapdragon 720G (SM6250) platform:

| Codename | Device | SoC |
| :--- | :--- | :--- |
| `joyeuse` | Xiaomi Redmi Note 9 Pro (Global / EU) | Qualcomm Snapdragon 720G |
| `curtana` | Xiaomi Redmi Note 9S / 9 Pro (India) | Qualcomm Snapdragon 720G |
| `gram` | POCO M2 Pro | Qualcomm Snapdragon 720G |
| `excalibur` | Xiaomi Redmi Note 9 Pro Max | Qualcomm Snapdragon 720G |

---

## Features

* **KernelSU-Next**: Integrated kernel-level root support via the official `legacy` branch for Linux 4.14.
* **Wireless Auditing**: Monitor mode and packet injection support (`mac80211`, `cfg80211`, `wext`).
* **Built-in OTG Wi-Fi Drivers**: Built-in kernel support for Atheros (`ath9k_htc`), Realtek (`rtl8187`), and Ralink (`rt2800usb`, `rt2x00`).
* **USB HID Gadget**: Hardware keyboard and mouse emulation (`/dev/hidg0`, `/dev/hidg1`) for BadUSB operations.
* **Kali NetHunter Compatibility**: Full System V IPC and namespace isolation (`USER_NS`, `PID_NS`, `NET_NS`) for chroot environments.
* **AnyKernel3 Deployment**: Flashable zip with automatic block device detection for custom recoveries.

---

## Installation

1. Download `AK3-Miatoll-NetHunter-KSU` from the latest [GitHub Actions](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions) workflow run.
2. Boot device into custom recovery (TWRP or OrangeFox).
3. (Optional but recommended) Perform a backup of the `Boot` partition.
4. Flash `Miatoll-NetHunter-Kernel.zip`.
5. Reboot to system and install the [KernelSU-Next Manager](https://github.com/rifsxd/KernelSU-Next/releases) APK.

---

## Upstream & Credits

* [crDroid Android](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250) - SM6250 kernel source
* [KernelSU-Next](https://github.com/rifsxd/KernelSU-Next) - KernelSU-Next driver and manager
* [osm0sis](https://github.com/osm0sis/AnyKernel3) - AnyKernel3 flashing backend
* [Offensive Security](https://www.kali.org) - Kali NetHunter
* [LineageOS](https://github.com/LineageOS) - Clang toolchain and kernel patches
