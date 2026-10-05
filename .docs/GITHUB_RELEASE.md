# 🚀 Alien Miatoll Kernel Edition (Stable Release)

**Target OS:** crDroid 16.0 (Android 16) | **Device:** Xiaomi Redmi Note 9 Pro (joyeuse)
**Security Stack:** Kali NetHunter + KernelSU-Next v3.4.0
**Lead Developer:** René Ortez | **Co-Dev:** Antigravity

---

## 🌟 What's New in this Release

This is a major stable release that brings a completely unified offensive security kernel to your daily driver. After extensive research and low-level kernel patching, we have successfully integrated **KernelSU-Next v3.4.0** natively into the kernel alongside full **Kali NetHunter** capabilities.

### 🔥 Key Features & Technical Highlights

* **KernelSU-Next v3.4.0 Integration (UAPI v4)**
  * Custom in-kernel spoofing architecture to bypass modern GKI restrictions.
  * Direct VFS interception for Manager APK detection (`com.rifsxd.ksunext`).
  * Patched SECCOMP filters and Magic Handshake (`0xdeadbeef`) via `sys_reboot` supercalls for completely hidden, native root access.
  * Embedded legacy daemon disabled, ensuring the modern `ksud` binary takes full control on boot.
* **Flawless Kali NetHunter Support**
  * Full support for BadUSB / HID interfaces.
  * Native USB Wi-Fi adapter support for packet injection (Monitor Mode).
  * **Kernel Panic Fix:** Resolved the terminal PTY null-pointer dereference bug (device no longer reboots when launching NetHunter Terminal).
* **Optimized AnyKernel3 Installer**
  * Silent, bloat-free installer with a perfectly symmetrical, professional text UI.
  * Automatically creates necessary `/data/adb` directory structures during flashing.

---

## 🛠️ Installation Instructions

1. Download the `Miatoll-NetHunter-Kernel.zip` file below.
2. Reboot your device into your custom recovery (OrangeFox / TWRP).
3. Flash the `Miatoll-NetHunter-Kernel.zip` file.
4. Reboot to System.
5. Install the latest [KernelSU-Next Manager (v3.4.0)](https://github.com/KernelSU-Next/KernelSU-Next/releases) APK.
6. **Enjoy!**

---

### ⚠️ Warning & Disclaimer
> *Flash at your own risk. Always keep a backup of your stock `boot.img` in case you need to recover from a bootloop caused by incompatible Magisk/KernelSU modules.*
