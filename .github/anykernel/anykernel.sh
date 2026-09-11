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

# boot install (preserve original crDroid 16.0 ramdisk bit-for-bit without unpack/repack corruption)
split_boot;

# Eliminate any extracted AVB metadata before repacking
rm -f $SPLITIMG/avb* $SPLITIMG/*.avb 2>/dev/null;

flash_boot;
## end boot install
