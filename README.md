# ⚡ Miatoll NetHunter & KernelSU-Next Automated Builder

<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/r3n3o/KernelSU-Next_Actions-builder_Miatoll/miatoll_nethunter_kernelsu.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=Build%20Pipeline)
![Kernel Version](https://img.shields.io/badge/Kernel-4.14.x--SM6250-blue?style=for-the-badge&logo=linux&logoColor=white)
![KernelSU](https://img.shields.io/badge/Root-KernelSU--Next-success?style=for-the-badge&logo=android&logoColor=white)
![Kali NetHunter](https://img.shields.io/badge/Security-Kali%20NetHunter%20Ready-red?style=for-the-badge&logo=kalilinux&logoColor=white)
![License](https://img.shields.io/badge/License-GPL--2.0-yellow?style=for-the-badge)

<p align="center">
  <strong>High-performance automated kernel build pipeline for the Xiaomi Snapdragon 720G (SM6250 / Miatoll) family.</strong><br>
  Engineered for wireless security auditing, Kali NetHunter tools, USB Gadget/HID attacks, and KernelSU-Next root integration.
</p>

</div>

---

## 📱 Supported Devices (Xiaomi SM6250 Family)

This kernel is unified and fully compatible with all variants of the **Xiaomi Miatoll** platform running AOSP / LineageOS / crDroid based ROMs:

| Codename | Commercial Device Name | SoC | Storage Type | Boot Partition Mapping |
| :--- | :--- | :--- | :--- | :--- |
| **`joyeuse`** | Xiaomi Redmi Note 9 Pro (Global / EU) | Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`curtana`** | Xiaomi Redmi Note 9S / 9 Pro (India) | Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`gram`** | POCO M2 Pro | Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |
| **`excalibur`** | Xiaomi Redmi Note 9 Pro Max | Snapdragon 720G | UFS 2.1 | `/dev/block/bootdevice/by-name/boot` |

---

## 🚀 Kernel Highlights & Injected Capabilities

### 🛡️ 1. Native KernelSU / KernelSU-Next Integration
* Kernel-level root access providing full root capabilities with superior invisibility against safety detection mechanisms.
* Clean and seamless integration built directly into the kernel source tree.

### 📡 2. Advanced Wireless Security & Packet Injection
* Full support for wireless monitor mode and 802.11 frame injection:
  * `CONFIG_WIRELESS=y`, `CONFIG_CFG80211=y`, `CONFIG_MAC80211=y`, `CONFIG_CFG80211_WEXT=y`.
* Dynamic modular drivers included for popular external USB OTG WiFi adapters:
  * **Atheros:** `ath9k_htc` (AR9271 chipset).
  * **Realtek:** `rtl8187` (ALFA AWUS036H).
  * **Ralink:** `rt2x00`, `rt2800usb` (RT3070 / RT5370).

### ⌨️ 3. USB Gadget & BadUSB / HID Emulation
* Turn your phone into an interactive penetration testing device with hardware HID emulation:
  * `CONFIG_USB_G_ANDROID=y`
  * `CONFIG_USB_F_HID=y`
  * `CONFIG_USB_CONFIGFS_F_HID=y`
* Directly provides `/dev/hidg0` (keyboard) and `/dev/hidg1` (mouse) character devices for automated keystroke injection payloads.

### 📦 4. NetHunter Chroot & Namespace Isolation
* Kernel-level support for containerization, chroot environments, and system isolation:
  * `CONFIG_NAMESPACES=y`, `CONFIG_USER_NS=y`, `CONFIG_PID_NS=y`, `CONFIG_NET_NS=y`, `CONFIG_BLK_DEV_LOOP=y`.
  * Inter-process communication enabled: `CONFIG_SYSVIPC=y`, `CONFIG_SYSVIPC_SYSCTL=y`.

### ⚡ 5. Standardized AnyKernel3 Packaging
* Pre-configured static AnyKernel3 delivery system pointing to the universal `/dev/block/bootdevice/by-name/boot` partition path.
* Guarantees 100% successful installation across TWRP, OrangeFox, and Lineage Recovery without block allocation failures.

---

## 📥 Installation & Flashing Guide

### Method A: Flashing via Custom Recovery (Recommended)
1. **Create a Backup:** Boot into TWRP / OrangeFox and create a backup of your current **`Boot`** and **`DTBO`** partitions.
2. **Download Artifact:** Download the latest `AK3-Miatoll-NetHunter-KSU` package from GitHub Actions.
3. **Flash:** Copy `Miatoll-NetHunter-Kernel.zip` to your device and flash it in Recovery mode.
4. **Reboot:** Reboot to System and install the KernelSU Manager APK.

### Method B: Non-Destructive RAM Boot (Fastboot)
To test the kernel in RAM without modifying your physical storage:
```bash
# Extract Image.gz-dtb from the artifact
adb reboot bootloader
fastboot boot Image.gz-dtb
```

---

## 🛠️ Automated CI/CD Workflow

The kernel is built automatically using GitHub Actions with:
* **Host Environment:** Ubuntu 22.04 LTS (with 10 GB dedicated swap space).
* **Compiler:** Google AOSP Clang toolchain + GCC 4.9 cross-compilers (aarch64 & arm32).
* **Base Kernel Source:** crDroid Android 16.0 SM6250 kernel tree.

To trigger a build:
1. Go to the **Actions** tab in this repository.
2. Select **`Build Miatoll Hacking Kernel V13 (NetHunter WiFi Fix)`**.
3. Click **Run workflow** on branch `main`.

---

## 🤝 Credits & Acknowledgments

Special thanks to the open-source projects, maintainers, and developers who made this kernel possible:

* **Maintainer & Lead Developer:** [@r3n3o](https://github.com/r3n3o) - Project architecture, device testing, and build orchestration.
* **AI Automation & Architecture Engineer:** **Antigravity** (Google DeepMind) - CI/CD pipeline optimization, AnyKernel3 static configuration, and codebase maintenance.
* **Strategic Guidance & Knowledge Synthesis:** **NotebookLM** - Technical research, kernel diagnostics, and partition analysis.
* **[osm0sis](https://github.com/osm0sis):** Creator of the universal [AnyKernel3](https://github.com/osm0sis/AnyKernel3) flasher.
* **[crDroid Android](https://github.com/crdroidandroid):** Base kernel source tree for the Xiaomi SM6250 platform.
* **[tiann](https://github.com/tiann) & [KernelSU-Next](https://github.com/rifsxd/KernelSU-Next):** Next-generation kernel-based root solution.
* **[Offensive Security](https://www.offensive-security.com/):** Creators of the [Kali NetHunter](https://www.kali.org/docs/nethunter/) mobile penetration testing platform.
* **[LineageOS](https://github.com/LineageOS):** Toolchains, GCC prebuilts, and Android kernel patches.

---

<div align="center">
  <sub>Developed with ❤️ for the Android security community and the Xiaomi Miatoll family.</sub>
</div>
