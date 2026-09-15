# 🚀 Release Template: Miatoll NetHunter & KernelSU-Next Engine

Utiliza este template al publicar nuevas versiones en **GitHub Releases** o foros de desarrollo como **XDA Developers**.

---

## 🏷️ [RELEASE TAG: v3.3.0-A16-STABLE]

### 🛡️ Miatoll NetHunter & KernelSU-Next Engine — Release Notes

**Target Devices:** Xiaomi Redmi Note 9 Pro (`joyeuse`), Redmi Note 9S (`curtana`), POCO M2 Pro (`gram`), Redmi Note 9 Pro Max (`excalibur`)  
**Target ROMs:** crDroid 16.0 / LineageOS 22.2 (Android 16 / SDK 36)  
**Linux Kernel Version:** `4.14.357-openela` (Clang 6443078 + GCC 4.9, LD=lld)

---

### ✨ What's Included in this Build?

- ⚡ **KernelSU-Next v3.3.0 Core**: Native kernel-level root with Non-GKI legacy manual syscall hooks. Passes SafetyNet/Play Integrity out of the box with zero `/system` modification.
- 📡 **Wireless Ingestion & Monitor Mode**: Full `mac80211` / `cfg80211` packet injection support with Minstrel HT rate control for USB OTG adapters (Atheros AR9271, Realtek RTL8187/RTL8812AU, Ralink RT3070).
- ⌨️ **BadUSB & HID Gadget Subsystem**: Native ConfigFS HID endpoints (`/dev/hidg0`, `/dev/hidg1`) enabled for DuckHunter / BadUSB attacks.
- 📦 **Full Chroot Isolation & Namespaces**: `CONFIG_NAMESPACES`, `CONFIG_USER_NS`, `CONFIG_PID_NS`, `CONFIG_NET_NS`, `CONFIG_SYSVIPC`, `CONFIG_BLK_DEV_LOOP` for seamless Kali NetHunter & Docker container operation.
- 📺 **NetHunter KeX Desktop Ready**: Integrated support for full graphical desktop (`XFCE4` / `TigerVNC`) on display `:1` (port `5901`).
- 🛠️ **AnyKernel3 UFS Packaging**: Universal flashable ZIP targeting dynamic UFS blocks (`/dev/block/bootdevice/by-name/boot`).

---

### 📥 Download & Verification

| Asset | Type | Recommended Verification |
| :--- | :--- | :--- |
| **`Miatoll-NetHunter-Kernel.zip`** | AnyKernel3 Flashable ZIP | `sha256sum Miatoll-NetHunter-Kernel.zip` |
| **`Image`** | Standalone Raw Kernel Image | `fastboot flash boot Image` (via unpacked boot) |

---

### 📋 Installation Instructions

1. Boot into **OrangeFox** or **TWRP** recovery.
2. **Backup your current `/boot` partition** (Essential safety measure).
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

**Full Technical Documentation & Source Code:** [GitHub Repository](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll)
