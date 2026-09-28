# 🏷️ GitHub Release Publication Notes

Copia y pega el siguiente contenido en el formulario de **New Release** en GitHub.

---

### 📌 Campos del formulario en GitHub:
* **Choose a tag / Tag version:** `v3.4.0-A16-STABLE`
* **Target branch:** `main`
* **Release title:** `🛡️ NetHunter & KernelSU-Next v3.4.0 Engine for Miatoll (crDroid 16.0 / Android 16)`

---

### 📝 Contenido para la descripción del Release (Markdown):

```markdown
## 🛡️ NetHunter & KernelSU-Next Engine v3.4.0 (Android 16 / crDroid 16.0 Vanilla)

**Enterprise-grade security auditing and superuser kernel engine for Xiaomi Snapdragon 720G (SM6250 / Miatoll).**

> [!CAUTION]
> ### ⚠️ DISCLAIMER & USER RESPONSIBILITY (USO BAJO SU PROPIO RIESGO)
> * **Your warranty is now void.** Modifying Android kernel partitions and rooting carries inherent risks of bootloops or bricking.
> * Flashing this custom kernel is done **strictly at your own risk**. The author assumes **no responsibility** for damaged hardware, unbootable devices, bootloops, or data loss.
> * Always maintain a verified **NANDroid backup of your `/boot` and `/dtbo` partitions** in custom recovery before proceeding.

> [!IMPORTANT]
> ### 🔬 HARDWARE VALIDATION BOUNDARY: EXCLUSIVELY TESTED ON `joyeuse`
> * This release has been **compiled, flashed, debugged, and validated for long-term daily driver use exclusively on the Xiaomi Redmi Note 9 Pro (`joyeuse`)** running **crDroid 16.0 Vanilla Edition (Android 16 / SDK 36, without pre-installed GApps)** with 100% stability.
> * Other Miatoll platform variants (`curtana` [Redmi Note 9S], `gram` [POCO M2 Pro], `excalibur` [Redmi Note 9 Pro Max]) share the unified source base but have **NOT been tested on physical hardware** by the author. Flashing on non-`joyeuse` devices is done under your own responsibility.

---

### ✨ What's New & Included Features

- ⚡ **KernelSU-Next v3.4.0 Core (Build 33294 / UAPI v4)**: Native kernel-level root with manual Non-GKI syscall hooks (`3.4.0:KernelSU`). Fully compatible with KernelSU-Next Manager v3.4.0 (33294-4) via UAPI v4 supercall protocol. Invisibility to userspace root detection with zero `/system` modification.
- 📡 **Wireless Ingestion & Monitor Mode**: Full `mac80211` and `cfg80211` packet injection support with Minstrel HT rate control for USB OTG adapters (Atheros AR9271 `ath9k_htc`, Realtek RTL8187 / RTL8812AU / `rtl8xxxu`, Ralink RT3070 `rt2800usb`, MediaTek MT7601U).
- ⌨️ **BadUSB & HID Gadget Subsystem**: Native ConfigFS HID endpoints (`/dev/hidg0`, `/dev/hidg1`) enabled for DuckHunter / BadUSB attacks.
- 📦 **Full Chroot Isolation & Namespaces**: `CONFIG_NAMESPACES`, `CONFIG_USER_NS`, `CONFIG_PID_NS`, `CONFIG_NET_NS`, `CONFIG_SYSVIPC`, `CONFIG_BLK_DEV_LOOP` for seamless Kali NetHunter & Docker container operation.
- 📺 **NetHunter KeX Desktop Ready**: Integrated support for full graphical desktop (`XFCE4` / `TigerVNC`) on display `:1` (port `5901`).
- 🛠️ **AnyKernel3 UFS Packaging**: Universal flashable ZIP targeting dynamic UFS blocks (`/dev/block/bootdevice/by-name/boot`).

---

### 📸 Tested & Verified Screenshots
<div align="center">
  <img src="https://raw.githubusercontent.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/main/.screenshots/Configuraci%C3%B3n.png" width="45%" alt="KernelSU Manager Working" />
  <img src="https://raw.githubusercontent.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/main/.screenshots/NetHunter.png" width="45%" alt="NetHunter Environment" />
</div>

---

### 📋 Step-by-Step Installation

1. Reboot your phone into **OrangeFox** (R11.1+) or **TWRP** (3.7.0+) recovery.
2. **Create a NANDroid Backup** of your `/boot` and `/dtbo` partitions.
3. Flash **`Miatoll-NetHunter-Kernel.zip`**.
4. Wipe **Dalvik / ART Cache**.
5. Reboot into System.
6. Install the official **[KernelSU-Next Manager APK (v3.4.0+)](https://github.com/rifsxd/KernelSU-Next/releases)**.
7. Open the KernelSU Manager app and verify:
   - **Status:** `Working`
   - **Version:** `3.4.0:KernelSU` (Build `33294`)
   - **Mode:** `Non-GKI (Legacy)`
8. In the **Superuser** tab, grant root permissions to Termux and NetHunter.

---

### 🔧 Essential Android 16 & NetHunter Setup Guide

#### 1. Termux Root Dynamic Linker Fix (Mandatory for Android 16)
Termux preloads `libtermux-exec.so` which causes `/system/bin/su` to fail. Always unset `LD_PRELOAD` before invoking root:
```bash
# In Termux:
unset LD_PRELOAD
su
```
*(Tip: Add `alias su="unset LD_PRELOAD; /system/bin/su"` to your `~/.bashrc`)*

#### 2. Kali NetHunter Debian Chroot Postinst Fix
Prevent daemon errors during `apt update && apt upgrade` inside Kali chroot:
```bash
# In Kali root shell:
cat << 'EOF' > /usr/sbin/policy-rc.d
#!/bin/sh
exit 101
EOF
chmod +x /usr/sbin/policy-rc.d
```

#### 3. NetHunter KeX (XFCE4 Graphical Desktop)
```bash
# Start TigerVNC server on port 5901 (Display :1):
kex-start

# Connect via NetHunter KeX app:
# Host: 127.0.0.1 | Port: 5901 | Password: kali

# Stop KeX session when finished:
kex-stop
```

#### 4. Hardware Verification Commands
```bash
# Verify KernelSU:
su -c "uname -a; /data/adb/ksud -V; su -v"

# Verify BadUSB HID nodes:
su -c "ls -la /dev/hidg*"

# Verify External Wi-Fi Monitor Mode (USB OTG):
su -c "lsusb; ip link; airmon-ng start wlan1"
```

---

### 🚨 Emergency Recovery (Soft-Brick Fix)
If you encounter a bootloop due to conflicting Magisk modules:
1. Boot into **Fastboot** mode (`Volume Down + Power`).
2. Flash your stock boot image:
   ```bash
   fastboot flash boot stock_boot.img
   fastboot reboot
   ```

---

### 📜 Upstream Credits & License
- **Kernel Base:** [crDroid Android](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250) & [LineageOS](https://github.com/LineageOS)
- **KernelSU-Next:** [rifsxd](https://github.com/rifsxd/KernelSU-Next) & [tiann](https://github.com/tiann/KernelSU)
- **Kali NetHunter:** [Offensive Security](https://www.kali.org)
- **AnyKernel3:** [osm0sis](https://github.com/osm0sis/AnyKernel3)
- **License:** [GNU General Public License v2.0 (GPL-2.0)](https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/blob/main/LICENSE)
```
