### AnyKernel3 Ramdisk Mod Script
## osm0sis @ xda-developers

### AnyKernel setup
# global properties
properties() { '
kernel.string=Miatoll NetHunter Kernel
do.devicecheck=0
do.modules=0
do.systemless=0
do.cleanup=1
do.cleanuponabort=0
device.name1=miatoll
device.name2=curtana
device.name3=joyeuse
device.name4=gram
device.name5=excalibur
supported.versions=
supported.patchlevels=
supported.vendorpatchlevels=
'; } # end properties

### AnyKernel install
# boot shell variables
BLOCK=boot;
block=boot;
IS_SLOT_DEVICE=0;
is_slot_device=0;
RAMDISK_COMPRESSION=auto;
ramdisk_compression=auto;
PATCH_VBMETA_FLAG=0;
patch_vbmeta_flag=0;
NO_VBMETA_PARTITION_PATCH=1;
no_vbmeta_partition_patch=1;

# import functions/variables and setup patching (DO NOT REMOVE)
. tools/ak3-core.sh;

ui_print " ";
ui_print "  ╔═══════════════════════════════════════════════════╗";
ui_print "  ║   ⚡  NETHUNTER & KERNELSU-NEXT FOR MIATOLL  ⚡   ║";
ui_print "  ╠═══════════════════════════════════════════════════╣";
ui_print "  ║                                                   ║";
ui_print "  ║     ██████╗ ██████╗ ███╗   ██╗██████╗  ██████╗    ║";
ui_print "  ║     ██╔══██╗╚════██╗████╗  ██║╚════██╗██╔═══██╗   ║";
ui_print "  ║     ██████╔╝ █████╔╝██╔██╗ ██║ █████╔╝██║   ██║   ║";
ui_print "  ║     ██╔══██╗ ╚═══██╗██║╚██╗██║ ╚═══██╗██║   ██║   ║";
ui_print "  ║     ██║  ██║██████╔╝██║ ╚████║██████╔╝╚██████╔╝   ║";
ui_print "  ║     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝    ║";
ui_print "  ║                                                   ║";
ui_print "  ║  ⚡ Kernel Engine : v3.4.0-A16-STABLE (UAPI v4)   ║";
ui_print "  ║  📱 Target Device : Xiaomi Redmi Note 9 Pro       ║";
ui_print "  ║  🛡️ Security Stack: Kali NetHunter + BadUSB HID   ║";
ui_print "  ║                                                   ║";
ui_print "  ║  👑 Lead Developer: r3n3o                         ║";
ui_print "  ║  🤖 Co-Developer  : Antigravity (Google DeepMind) ║";
ui_print "  ╚═══════════════════════════════════════════════════╝";
ui_print " ";

# boot install (preserve original crDroid 16.0 ramdisk bit-for-bit without unpack/repack corruption)
split_boot;

# Eliminate any extracted AVB metadata before repacking
rm -f $SPLITIMG/avb* $SPLITIMG/*.avb 2>/dev/null;

flash_boot;
## end boot install

# Ensure /data/adb exists for KernelSU daemon and modules
mount /data 2>/dev/null;
if [ -d /data ]; then
  ui_print "[+] Provisioning KernelSU-Next v3.4.0 daemon environment...";
  mkdir -p /data/adb /data/adb/modules /data/adb/ksu /data/adb/ksu/bin /data/adb/post-fs-data.d /data/adb/service.d 2>/dev/null;
  chmod 755 /data/adb /data/adb/modules /data/adb/ksu /data/adb/ksu/bin /data/adb/post-fs-data.d /data/adb/service.d 2>/dev/null;
  chmod -R 755 /data/adb/ksu 2>/dev/null;
  if [ -f $AKHOME/tools/ksud ]; then
    cp -f $AKHOME/tools/ksud /data/adb/ksud 2>/dev/null;
    cp -f $AKHOME/tools/ksud /data/adb/ksu/bin/ksud 2>/dev/null;
    chmod 755 /data/adb/ksud /data/adb/ksu/bin/ksud 2>/dev/null;
  fi;
  # Fix Android 16 ART SecurityException for Manager dex cache if present
  find /data/user_de/0/com.rifsxd.ksunext/cache/ -name "*.jar" -exec chmod 444 {} + 2>/dev/null;
  find /data/data/com.rifsxd.ksunext/cache/ -name "*.jar" -exec chmod 444 {} + 2>/dev/null;
  ui_print "[✓] KernelSU-Next & NetHunter installation completed successfully!";
fi;

