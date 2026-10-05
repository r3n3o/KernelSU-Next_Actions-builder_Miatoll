# 📱 XDA Developers Thread Template

Utiliza este contenido para crear tu hilo oficial de lanzamiento en **XDA Developers** (sección *Xiaomi Redmi Note 9 Pro / Miatoll ROMs, Kernels, & Mods*).

Incluye tanto el formato **BBCode (estándar de XDA)** listo para copiar y pegar en el editor de XDA, como las instrucciones para el título y etiquetas.

---

## 🏷️ Título sugerido para el post en XDA

```text
[KERNEL][A16][STABLE] NetHunter & KernelSU-Next Engine v3.4.0 [joyeuse/miatoll][crDroid 16]
```

### Etiquetas (Tags) sugeridas en XDA:
`kernel`, `kernelsu`, `kernelsu-next`, `nethunter`, `kali-linux`, `joyeuse`, `miatoll`, `android-16`, `crdroid`, `security`

---

## 📋 Contenido BBCode para XDA (Copiar y Pegar)

```bbcode
[CENTER]
[SIZE=6][FONT=Trebuchet MS][B]🛡️ NetHunter & KernelSU-Next Engine 🛡️[/B][/FONT][/SIZE]
[SIZE=4][B]Enterprise-Grade Security Auditing & Superuser Kernel for Qualcomm Snapdragon 720G (SM6250)[/B][/SIZE]
[SIZE=3][COLOR=SeaGreen][B]Kernel Linux 4.14.357-openela | KernelSU-Next v3.4.0 | Android 16 (crDroid 16.0 / LOS 22.2)[/B][/COLOR][/SIZE]

[SIZE=3]
[B][COLOR=#ffffff][BGCOLOR=#2980b9] 🐧 Linux 4.14.357 [/BGCOLOR] [BGCOLOR=#c0392b] ⚡ KernelSU-Next v3.4.0 [/BGCOLOR] [BGCOLOR=#27ae60] 📱 Tested: joyeuse only [/BGCOLOR] [BGCOLOR=#d35400] 📜 GPL-2.0 [/BGCOLOR][/COLOR][/B]
[/SIZE]
[/CENTER]

[CODE]
/*
 * Your warranty is now void.
 *
 * I am not responsible for bricked devices, dead SD cards, bootloops,
 * thermonuclear war, or your alarm failing in the morning.
 *
 * Flashing custom kernels and modifying boot partitions is done
 * ENTIRELY AT YOUR OWN RISK (BAJO SU PROPIO RIESGO).
 *
 * Always maintain a verified NANDroid backup of your /boot and /dtbo partitions!
 */
[/CODE]

[SIZE=4][COLOR=Firebrick][B]🔬 HARDWARE VALIDATION NOTICE (IMPORTANT):[/B][/COLOR][/SIZE]
[QUOTE]
This release has been [B]extensively tested, debugged, and validated for daily-driver use on real physical hardware exclusively on the Xiaomi Redmi Note 9 Pro ([FONT=Courier New]joyeuse[/FONT])[/B] running [B]crDroid 16.0 Vanilla Edition (Android 16 / SDK 36, without pre-installed GApps)[/B].
All functions (KernelSU root, BadUSB HID, KeX Desktop, and packet injection) have been running with 100% stability and zero crashes.

[I]Note on other Miatoll devices:[/I] While the underlying kernel tree is unified for the SM6250 platform ([FONT=Courier New]curtana[/FONT], [FONT=Courier New]gram[/FONT], [FONT=Courier New]excalibur[/FONT]), these variants have [B]NOT[/B] been directly tested on hardware by the author. Flash at your own discretion.
[/QUOTE]

---

[SIZE=5][B]✨ Key Features & Technical Highlights[/B][/SIZE]

[LIST]
[*][B]⚡ KernelSU-Next v3.4.0 Core Engine (Build 33294):[/B] Native kernel-level root with custom Non-GKI UAPI v4 spoofing. Bypasses Android 16 SECCOMP restrictions via [FONT=Courier New]0xdeadbeef[/FONT] magic handshake and direct VFS interception for Manager APK detection.
[*][B]📡 Full Wireless Packet Injection & Monitor Mode:[/B] Backported and enabled [FONT=Courier New]mac80211[/FONT] and [FONT=Courier New]cfg80211[/FONT] wireless stacks with Minstrel HT rate control. Ready out-of-the-box for external USB OTG wireless cards (Atheros AR9271, Realtek RTL8812AU, Ralink RT3070).
[*][B]⌨️ BadUSB / USB HID Hardware Emulation:[/B] Native ConfigFS HID endpoints ([FONT=Courier New]/dev/hidg0[/FONT], [FONT=Courier New]/dev/hidg1[/FONT]) enabled for DuckHunter, BadUSB payload execution, and mouse/keyboard emulation.
[*][B]📦 Advanced Linux Namespaces & Virtualization:[/B] Full support for flawless Kali NetHunter chroot and rootless containers.
[*][B]🛠️ Resolved NetHunter Kernel Panics:[/B] Completely fixed the legacy PTY null-pointer dereference bug (SELinux Context issue) ensuring 100% stability when launching NetHunter Terminal or Termux.
[*][B]📺 NetHunter KeX Desktop Ready:[/B] Pre-configured for headless XFCE4 graphical sessions over TigerVNC on port 5901.
[*][B]🛡️ AnyKernel3 Universal Flashable ZIP:[/B] Silent, bloat-free installer with a perfectly symmetrical CLI UI and dynamic UFS block discovery.
[/LIST]

---

[SIZE=5][B]💿 Compatibility Matrix[/B][/SIZE]

[TABLE]
[TR]
[TH]Device / ROM[/TH]
[TH]Codename[/TH]
[TH]Status[/TH]
[TH]Notes[/TH]
[/TR]
[TR]
[TD][B]Xiaomi Redmi Note 9 Pro[/B][/TD]
[TD][FONT=Courier New]joyeuse[/FONT][/TD]
[TD][COLOR=SeaGreen][B]🟢 Tested & Verified (Stable)[/B][/COLOR][/TD]
[TD]Daily driver verified; zero bugs over long-term testing.[/TD]
[/TR]
[TR]
[TD][B]Xiaomi Redmi Note 9S[/B][/TD]
[TD][FONT=Courier New]curtana[/FONT][/TD]
[TD][COLOR=DarkOrange]🟡 Unified Tree (Untested)[/COLOR][/TD]
[TD]Compatible by source; test at your own risk.[/TD]
[/TR]
[TR]
[TD][B]POCO M2 Pro[/B][/TD]
[TD][FONT=Courier New]gram[/FONT][/TD]
[TD][COLOR=DarkOrange]🟡 Unified Tree (Untested)[/COLOR][/TD]
[TD]Compatible by source; test at your own risk.[/TD]
[/TR]
[TR]
[TD][B]Redmi Note 9 Pro Max[/B][/TD]
[TD][FONT=Courier New]excalibur[/FONT][/TD]
[TD][COLOR=DarkOrange]🟡 Unified Tree (Untested)[/COLOR][/TD]
[TD]Compatible by source; test at your own risk.[/TD]
[/TR]
[TR]
[TD][B]crDroid 16.0 (Vanilla)[/B][/TD]
[TD]Android 16 (SDK 36)[/TD]
[TD][COLOR=SeaGreen][B]🟢 Recommended Reference ROM (Tested)[/B][/COLOR][/TD]
[TD]100% PTY and namespace stability (Vanilla / No-GApps).[/TD]
[/TR]
[TR]
[TD][B]LineageOS 22.2 / AOSP[/B][/TD]
[TD]Android 15 / 16[/TD]
[TD][COLOR=SeaGreen][B]🟢 Supported[/B][/COLOR][/TD]
[TD]Compatible with standard dynamic partition layout.[/TD]
[/TR]
[TR]
[TD][B]Stock MIUI / HyperOS[/B][/TD]
[TD]Any[/TD]
[TD][COLOR=Red][B]🔴 Incompatible[/B][/COLOR][/TD]
[TD]Stock display blobs will bootloop.[/TD]
[/TR]
[/TABLE]

---

[SIZE=5][B]📥 Downloads & Source Code[/B][/SIZE]

[LIST]
[*][B]📦 Flashable Kernel ZIP:[/B] [URL='https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/releases'][B]GitHub Releases (v3.4.0-A16-STABLE)[/B][/URL]
[*][B]📱 KernelSU-Next Manager APK (v3.4.0+):[/B] [URL='https://github.com/rifsxd/KernelSU-Next/releases'][B]KernelSU-Next Official Releases[/B][/URL]
[*][B]💻 Kernel Source Code (GPL-2.0):[/B] [URL='https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll'][B]GitHub Repository[/B][/URL]
[/LIST]

---

[SIZE=5][B]📋 Flashing & Installation Guide[/B][/SIZE]

[SIZE=4][B]Pre-Requisites:[/B][/SIZE]
[LIST=1]
[*]Unlocked Bootloader on your Redmi Note 9 Pro ([FONT=Courier New]joyeuse[/FONT]).
[*]OrangeFox Recovery (R11.1+) or Official TWRP (3.7.0+) installed.
[*][B]MANDATORY:[/B] In Recovery, go to [B]Backup[/B] -> Select [B]Boot[/B] and [B]DTBO[/B] -> Swipe to create a NANDroid backup.
[/LIST]

[SIZE=4][B]Installation Steps:[/B][/SIZE]
[LIST=1]
[*]Reboot to Recovery mode.
[*]Flash [FONT=Courier New]Miatoll-NetHunter-Kernel.zip[/FONT].
[*]Wipe [B]Dalvik & Cache[/B].
[*]Reboot to System.
[*]Install the [URL='https://github.com/rifsxd/KernelSU-Next/releases'][B]KernelSU-Next Manager APK (v3.4.0+)[/B][/URL].
[*]Open KernelSU Manager -> Verify it says [B]Working (3.4.0:KernelSU / Mode: Non-GKI)[/B].
[*]In the Superuser tab, grant root privileges to Termux, NetHunter, and your desired apps.
[/LIST]

---

[SIZE=5][B]🔧 The "Secret Sauce": Essential Android 16 & NetHunter Setup Guide[/B][/SIZE]

[I]To achieve 100% full functionality without errors on Android 16, follow these precise configuration steps we established during testing:[/I]

[SPOILER="1. Termux Root Linker Fix (Crucial for Android 16)"]
On Android 16, Termux preloads [FONT=Courier New]libtermux-exec.so[/FONT] via [FONT=Courier New]LD_PRELOAD[/FONT]. When calling Android's root binary ([FONT=Courier New]/system/bin/su[/FONT]), Android's dynamic linker crashes with [I]"library libtermux-exec.so not found"[/I].

[B]The Solution:[/B]
Always unset [FONT=Courier New]LD_PRELOAD[/FONT] before executing root commands.

Add this alias to your [FONT=Courier New]~/.bashrc[/FONT] or [FONT=Courier New]~/.profile[/FONT] in Termux:
[CODE]
alias su="unset LD_PRELOAD; /system/bin/su"
[/CODE]
Or invoke root cleanly with:
[CODE]
unset LD_PRELOAD
su
[/CODE]
[/SPOILER]

[SPOILER="2. Kali Debian Chroot Postinst Fix (Policy-rc.d)"]
When updating packages in the NetHunter chroot ([FONT=Courier New]apt update && apt upgrade[/FONT]), daemon post-installation scripts (e.g., [FONT=Courier New]systemd[/FONT], [FONT=Courier New]mariadb[/FONT]) may fail because services cannot be started by systemd inside a chroot.

[B]The Solution:[/B]
Run the following inside the Kali root shell:
[CODE]
cat << 'EOF' > /usr/sbin/policy-rc.d
#!/bin/sh
exit 101
EOF
chmod +x /usr/sbin/policy-rc.d
[/CODE]
This forces Debian package managers to bypass daemon startup during package installation.
[/SPOILER]

[SPOILER="3. Launching NetHunter KeX (XFCE4 Desktop)"]
To start the XFCE4 graphical desktop environment via TigerVNC:

1. Inside your Termux / Kali shell, launch the KeX server:
[CODE]
kex-start
[/CODE]
*(This initializes TigerVNC on port [FONT=Courier New]5901[/FONT] for Display [FONT=Courier New]:1[/FONT]).*

2. Open the **NetHunter KeX app** (or any VNC Viewer).
3. Connect to:
[LIST]
[*][B]Host:[/B] [FONT=Courier New]127.0.0.1[/FONT]
[*][B]Port:[/B] [FONT=Courier New]5901[/FONT]
[*][B]Password:[/B] [FONT=Courier New]kali[/FONT]
[/LIST]
4. To stop the desktop session when finished:
[CODE]
kex-stop
[/CODE]
[/SPOILER]

[SPOILER="4. Verifying USB HID BadUSB & Wireless Monitor Mode"]
[B]Check HID BadUSB Nodes:[/B]
[CODE]
su -c "ls -la /dev/hidg*"
# Expected output: /dev/hidg0 and /dev/hidg1 present
[/CODE]

[B]Check External Wireless Injection (OTG):[/B]
Connect your USB Wi-Fi adapter (e.g. Alfa AWUS036NHA / TP-Link TL-WN722N) via OTG:
[CODE]
su -c "lsusb"
su -c "airmon-ng start wlan1"
su -c "aireplay-ng --test wlan1mon"
[/CODE]
[/SPOILER]

---

[SPOILER="📸 Screenshots / Proof of Work (Click to view)"]
[CENTER]
[I]KernelSU-Next v3.4.0 Working (joyeuse / crDroid 16.0 Vanilla) | NetHunter Environment[/I]

[IMG]https://raw.githubusercontent.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/main/.screenshots/Configuraci%C3%B3n.png[/IMG]

[IMG]https://raw.githubusercontent.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/main/.screenshots/NetHunter.png[/IMG]
[/CENTER]
[/SPOILER]

---

[SIZE=5][B]🚨 Emergency Recovery (Soft-Brick Fix)[/B][/SIZE]

If you ever encounter a bootloop due to conflicting Magisk modules or incompatible system tweaks:
[LIST=1]
[*]Hold [B]Volume Down (-) + Power[/B] to enter Fastboot Mode.
[*]Connect phone to PC via USB.
[*]Flash your original backed-up stock [FONT=Courier New]boot.img[/FONT] (or extract it from your ROM zip):
[CODE]
fastboot flash boot stock_boot.img
fastboot reboot
[/CODE]
[/LIST]

---

[SIZE=5][B]🤝 Credits & Upstream Acknowledgments[/B][/SIZE]

[LIST]
[*][B]crDroid Android Team & LineageOS:[/B] Base kernel source & A16 tree.
[*][B]rifsxd & tiann:[/B] KernelSU-Next & KernelSU architecture.
[*][B]Offensive Security Team:[/B] Kali NetHunter project.
[*][B]osm0sis:[/B] AnyKernel3 packaging engine.
[*][B]René Ortez:[/B] Lead Developer & Maintainer.
[*][B]Antigravity (Google DeepMind):[/B] Co-Developer (Architecture & Kernel Hooking).
[*][B]Miatoll Community:[/B] Continuous testing and development.
[/LIST]

[CENTER]
[SIZE=2][I]Licensed under GNU General Public License v2.0 (GPL-2.0).[/I][/SIZE]
[/CENTER]
```

---

## 💡 Recomendaciones para la publicación en XDA

1. **Sección en XDA:** Publica el hilo en el subforo de **Xiaomi Redmi Note 9 Pro (joyeuse) -> ROMs, Kernels, & Mods**.
2. **Adjuntos / Links:** Asegúrate de enlazar tu Release de GitHub (`https://github.com/r3n3o/KernelSU-Next_Actions-builder_Miatoll/releases`) para que los usuarios descarguen el ZIP directamente.
3. **Soporte:** Pide a los usuarios que publiquen los logs de recuperación (`anykernel_install.log` o `dmesg`) si reportan algún problema.
