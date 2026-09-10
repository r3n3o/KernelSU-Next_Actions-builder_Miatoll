<div align="center">

# Miatoll NetHunter & KernelSU-Next Kernel

Automated build workflow providing a security-auditing kernel for Xiaomi SM6250 devices, integrating KernelSU-Next, wireless packet injection, OTG network drivers, SDR, BadUSB emulation, and AnyKernel3 packaging.

[![Build Status](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=flat-square&label=Build)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions)
[![Kernel](https://img.shields.io/badge/Kernel-Linux%204.14%20(SM6250)-0052cc?style=flat-square)](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250)
[![Root](https://img.shields.io/badge/Root-KernelSU--Next-0e8a16?style=flat-square)](https://github.com/rifsxd/KernelSU-Next)
[![Security](https://img.shields.io/badge/Security-Kali%20NetHunter-b60205?style=flat-square)](https://www.kali.org)

</div>

---

## Supported Devices

Unified build for the Xiaomi Snapdragon 720G (SM6250) platform:

| Codename | Target Device | SoC |
| :--- | :--- | :--- |
| `joyeuse` | Xiaomi Redmi Note 9 Pro (Global / EU) | Qualcomm Snapdragon 720G |
| `curtana` | Xiaomi Redmi Note 9S / 9 Pro (India) | Qualcomm Snapdragon 720G |
| `gram` | POCO M2 Pro | Qualcomm Snapdragon 720G |
| `excalibur` | Xiaomi Redmi Note 9 Pro Max | Qualcomm Snapdragon 720G |

---

## Features

* **KernelSU-Next Integration**: Integrated kernel-level superuser support via the official `legacy` branch for Linux 4.14 non-GKI.
* **Wireless Auditing**: Monitor mode and packet injection support with Minstrel HT rate control (`mac80211`, `cfg80211`, `wext`).
* **OTG Wi-Fi Drivers**: Built-in support for Atheros (`ath9k_htc`, `carl9170`), Realtek (`rtl8187`, `rtl8xxxu`), Ralink (`rt2800usb`, `rt2500usb`, `rt73usb`), and MediaTek (`mt7601u`).
* **Ethernet OTG Support**: Drivers for ASIX (`ax88179_178a`, `ax8817x`), Realtek (`r8152`), CDC Ethernet (`cdc_ether`, `cdc_ncm`), and Davicom (`dm9601`).
* **External Bluetooth**: Support for USB Bluetooth adapters (`btusb`) for NetHunter RF/Bluetooth operations.
* **Software-Defined Radio (SDR)**: USB digital video and RTL-SDR tuner support (`dvb_usb_rtl28xxu`) for radio frequency scanning.
* **BadUSB & DriveDroid**: Hardware HID emulation (`/dev/hidg0`, `/dev/hidg1`) and USB Mass Storage CD-ROM gadget support.
* **Kali NetHunter Compatibility**: Full System V IPC and namespace isolation (`USER_NS`, `PID_NS`, `NET_NS`) for chroot operation.
* **AnyKernel3 Deployment**: Automated flashable zip with partition resolution for custom recoveries.

---

## Installation

1. **Download the Kernel Package**:
   Download the latest `AK3-Miatoll-NetHunter-KSU` artifact from [GitHub Actions](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/actions).

2. **Boot Custom Recovery**:
   Reboot the device into TWRP or OrangeFox recovery.

3. **Backup (Recommended)**:
   Create a backup of your existing `Boot` partition.

4. **Flash AnyKernel3 Zip**:
   Install `Miatoll-NetHunter-Kernel.zip` via recovery.

5. **Reboot & Install Manager**:
   Reboot to system and install the [KernelSU-Next Manager](https://github.com/rifsxd/KernelSU-Next/releases) APK.

---

## Upstream & Credits

* **Kernel Source**: [crDroid Android](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250) (`android_kernel_xiaomi_sm6250`)
* **KernelSU-Next**: [rifsxd/KernelSU-Next](https://github.com/rifsxd/KernelSU-Next)
* **AnyKernel3 Template**: [osm0sis/AnyKernel3](https://github.com/osm0sis/AnyKernel3)
* **Kali NetHunter**: [Offensive Security](https://www.kali.org)
* **Toolchains & Patches**: [LineageOS](https://github.com/LineageOS)
