# AnyKernel3 Config para Miatoll (Qualcomm SM6250)
properties() { '
kernel.string=Miatoll NetHunter Kernel
do.devicecheck=0
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuntil=500
device.name1=miatoll
device.name2=curtana
device.name3=joyeuse
device.name4=gram
device.name5=excalibur
supported.versions=
supported.patchlevels=
'; }

# Ruta explicita al bloque UFS /boot detectado por TWRP
block=/dev/block/sde51;
is_slot_device=0;
ramdisk_build_dts=0;

. tools/ak3-core.sh;

dump_boot;
write_boot;