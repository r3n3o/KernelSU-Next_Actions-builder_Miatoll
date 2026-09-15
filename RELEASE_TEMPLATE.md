# 🚀 Release Template: Miatoll NetHunter & KernelSU-Next Engine

Utiliza este template al publicar nuevas versiones en **GitHub Releases** o foros de desarrollo como **XDA Developers**.

---

## 🏷️ [RELEASE TAG: v3.3.0-A16-STABLE]

### 🛡️ Miatoll NetHunter & KernelSU-Next Engine — Release Notes

> ⚠️ **DISCLAIMER & LIABILITY (USO BAJO TU PROPIO RIESGO):**
> * Flashing custom kernels is done **entirely at your own risk**. The maintainer assumes no responsibility for bricked devices, lost data, hardware damage, or bootloops.
> * Always make a NANDroid backup of your `/boot` and `/dtbo` partitions before flashing.
>
> 🔬 **HARDWARE VALIDATION (PROBADO EXCLUSIVAMENTE EN JOYEUSE):**
> * This release has been **exclusively compiled, tested, and validated on physical hardware using the Xiaomi Redmi Note 9 Pro (`joyeuse`)** running **crDroid 16.0 (Android 16 / SDK 36)**.
> * Other Miatoll family variants (`curtana`, `gram`, `excalibur`) originate from the same unified source tree, but have **NOT** been directly tested on hardware by the author. Use at your own discretion.

---

### ✨ Key Features & Capabilities

- ⚡ **KernelSU-Next v3.3.0 Core**: Native kernel-level root with Non-GKI legacy manual syscall hooks. Fully functional superuser with zero `/system` partition footprint.
- 📡 **Wireless Ingestion & Monitor Mode**: Full `mac80211` / `cfg80211` packet injection support with Minstrel HT rate control for USB OTG adapters (Atheros AR9271, Realtek RTL8187/RTL8812AU, Ralink RT3070).
- ⌨️ **BadUSB & HID Gadget Subsystem**: Native ConfigFS HID endpoints (`/dev/hidg0`, `/dev/hidg1`) enabled for DuckHunter / BadUSB attacks.
- 📦 **Full Chroot Isolation & Namespaces**: `CONFIG_NAMESPACES`, `CONFIG_USER_NS`, `CONFIG_PID_NS`, `CONFIG_NET_NS`, `CONFIG_SYSVIPC`, `CONFIG_BLK_DEV_LOOP` for seamless Kali NetHunter & container operation.
- 📺 **NetHunter KeX Desktop Ready**: Integrated support for full graphical desktop (`XFCE4` / `TigerVNC`) on display `:1` (port `5901`).
- 🛠️ **AnyKernel3 UFS Packaging**: Universal flashable ZIP targeting dynamic UFS blocks (`/dev/block/bootdevice/by-name/boot`).

---

### 📥 Download & Verification

| Asset File | Package Type | Integrity Verification |
| :--- | :--- | :--- |
| **`Miatoll-NetHunter-Kernel.zip`** | AnyKernel3 Flashable ZIP | `sha256sum Miatoll-NetHunter-Kernel.zip` |
| **`Image`** | Raw Uncompressed Kernel Image | `sha256sum Image` |

---

### 📋 Installation Instructions

1. Boot into **OrangeFox** or **TWRP** recovery.
2. **Backup your current `/boot` and `/dtbo` partitions** (Essential safety measure).
3. Flash **`Miatoll-NetHunter-Kernel.zip`**.
4. Wipe Dalvik / ART Cache and reboot to system.
5. Install **[KernelSU-Next Manager APK (v3.3.0+)](https://github.com/rifsxd/KernelSU-Next/releases)**.
6. Grant root access per-app in the Superuser tab.

---

### 🚨 Emergency Recovery (Soft-Brick Fix)

If you experience a bootloop due to existing conflicting modules:
1. Boot into **Fastboot** mode (`Vol Down + Power`).
2. Flash your stock boot image:
   ```bash
   fastboot flash boot stock_boot.img
   fastboot reboot
   ```

---

**License:** [GNU General Public License v2.0 (GPL-2.0)](LICENSE)  
**Full Documentation & Source Code:** [GitHub Repository](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll)
