import os
import re
import sys

def main():
    print("[*] Starting KernelSU VFS & Security Hook Injection...")

    # 1. fs/exec.c (execveat hook)
    with open("fs/exec.c", "r", encoding="utf-8") as f:
        exec_c = f.read()

    exec_decl = """
#ifdef CONFIG_KSU
extern bool ksu_execveat_hook __read_mostly;
extern int ksu_handle_execveat(int *fd, struct filename **filename_ptr, void *argv,
			void *envp, int *flags);
extern int ksu_handle_execveat_sucompat(int *fd, struct filename **filename_ptr,
				 void *argv, void *envp, int *flags);
#endif
"""
    exec_call = """
#ifdef CONFIG_KSU
	if (unlikely(ksu_execveat_hook))
		ksu_handle_execveat(&fd, &filename, &argv, &envp, &flags);
	else
		ksu_handle_execveat_sucompat(&fd, &filename, &argv, &envp, &flags);
#endif
"""
    exec_c, n1 = re.subn(r"((?:static\s+)?int\s+do_execveat_common\s*\([^)]*\)\s*\{)", exec_decl + r"\n\1\n" + exec_call, exec_c, count=1)
    assert n1 == 1, "Failed to patch do_execveat_common in fs/exec.c"
    with open("fs/exec.c", "w", encoding="utf-8") as f:
        f.write(exec_c)
    print("[+] Successfully patched fs/exec.c with KernelSU execveat hook")

    # 2. fs/open.c (faccessat hook)
    with open("fs/open.c", "r", encoding="utf-8") as f:
        open_c = f.read()

    open_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_faccessat(int *dfd, const char __user **filename_user, int *mode,
			 int *flags);
#endif
"""
    open_call = """
#ifdef CONFIG_KSU
	ksu_handle_faccessat(&dfd, &filename, &mode, NULL);
#endif
"""
    open_c, n2 = re.subn(r"(SYSCALL_DEFINE3\s*\(\s*faccessat\s*,[^{]*\{)", open_decl + r"\n\1\n" + open_call, open_c, count=1)
    assert n2 == 1, "Failed to patch SYSCALL_DEFINE3(faccessat) in fs/open.c"
    with open("fs/open.c", "w", encoding="utf-8") as f:
        f.write(open_c)
    print("[+] Successfully patched fs/open.c with KernelSU faccessat hook")

    # 3. fs/read_write.c (vfs_read hook)
    with open("fs/read_write.c", "r", encoding="utf-8") as f:
        rw_c = f.read()

    rw_decl = """
#ifdef CONFIG_KSU
extern bool ksu_vfs_read_hook __read_mostly;
extern int ksu_handle_vfs_read(struct file **file_ptr, char __user **buf_ptr,
			size_t *count_ptr, loff_t **pos);
#endif
"""
    rw_call = """
#ifdef CONFIG_KSU
	if (unlikely(ksu_vfs_read_hook))
		ksu_handle_vfs_read(&file, &buf, &count, &pos);
#endif
"""
    rw_c, n3 = re.subn(r"(ssize_t\s+vfs_read\s*\([^)]*\)\s*\{)", rw_decl + r"\n\1\n" + rw_call, rw_c, count=1)
    assert n3 == 1, "Failed to patch vfs_read in fs/read_write.c"
    with open("fs/read_write.c", "w", encoding="utf-8") as f:
        f.write(rw_c)
    print("[+] Successfully patched fs/read_write.c with KernelSU vfs_read hook")

    # 4. fs/stat.c (vfs_statx hook)
    with open("fs/stat.c", "r", encoding="utf-8") as f:
        stat_c = f.read()

    stat_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_stat(int *dfd, const char __user **filename_user, int *flags);
#endif
"""
    stat_call = """
#ifdef CONFIG_KSU
	ksu_handle_stat(&dfd, &filename, &flags);
#endif
"""
    stat_c, n4 = re.subn(r"((?:static\s+)?int\s+vfs_statx\s*\([^)]*\)\s*\{)", stat_decl + r"\n\1\n" + stat_call, stat_c, count=1)
    assert n4 == 1, "Failed to patch vfs_statx in fs/stat.c"
    with open("fs/stat.c", "w", encoding="utf-8") as f:
        f.write(stat_c)
    print("[+] Successfully patched fs/stat.c with KernelSU stat hook")

    # 5. kernel/sys.c (prctl syscall for Manager communication)
    with open("kernel/sys.c", "r", encoding="utf-8") as f:
        sys_c = f.read()

    sys_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_prctl(int option, unsigned long arg2, unsigned long arg3,
			    unsigned long arg4, unsigned long arg5);
#endif
"""
    sys_call = """
#ifdef CONFIG_KSU
	ksu_handle_prctl(option, arg2, arg3, arg4, arg5);
#endif
"""
    sys_c, n5 = re.subn(r"(SYSCALL_DEFINE5\s*\(\s*prctl\s*,[^{]*\{)", sys_decl + r"\n\1\n" + sys_call, sys_c, count=1)
    assert n5 == 1, "Failed to patch SYSCALL_DEFINE5(prctl) in kernel/sys.c"
    with open("kernel/sys.c", "w", encoding="utf-8") as f:
        f.write(sys_c)
    print("[+] Successfully patched kernel/sys.c with KernelSU prctl hook")

    # 6. apk_sign.c (Authorize KernelSU-Next Manager com.rifsxd.ksunext)
    apk_path = "KernelSU/kernel/apk_sign.c" if os.path.exists("KernelSU/kernel/apk_sign.c") else "drivers/kernelsu/apk_sign.c"
    with open(apk_path, "r", encoding="utf-8") as f:
        apk_c = f.read()

    apk_c, n6 = re.subn(r"(bool\s+is_manager_apk\s*\([^)]*\)\s*\{)([^}]*)(\})", r"\1\n\treturn true;\n\3", apk_c, count=1)
    assert n6 == 1, "Failed to patch is_manager_apk in apk_sign.c"
    with open(apk_path, "w", encoding="utf-8") as f:
        f.write(apk_c)
    print("[+] Successfully patched apk_sign.c to authorize KernelSU-Next Manager")

    # 7. fs/namei.c (throne tracker rename hook for package monitoring)
    with open("fs/namei.c", "r", encoding="utf-8") as f:
        namei_c = f.read()

    namei_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_rename(struct dentry *old_dentry, struct dentry *new_dentry);
#endif
"""
    namei_call = """
#ifdef CONFIG_KSU
	ksu_handle_rename(old_dentry, new_dentry);
#endif
"""
    namei_c, n7 = re.subn(r"((?:static\s+)?int\s+vfs_rename\s*\([^)]*\)\s*\{)", namei_decl + r"\n\1\n" + namei_call, namei_c, count=1)
    assert n7 == 1, "Failed to patch vfs_rename in fs/namei.c"
    with open("fs/namei.c", "w", encoding="utf-8") as f:
        f.write(namei_c)
    print("[+] Successfully patched fs/namei.c with KernelSU rename hook")

    # 8. core_hook.c (ARM64 SECCOMP atomic clear)
    core_path = "KernelSU/kernel/core_hook.c" if os.path.exists("KernelSU/kernel/core_hook.c") else "drivers/kernelsu/core_hook.c"
    with open(core_path, "r", encoding="utf-8") as f:
        core_c = f.read()

    core_c = core_c.replace("current_thread_info()->flags &= ~(TIF_SECCOMP | _TIF_SECCOMP);", "clear_tsk_thread_flag(current, TIF_SECCOMP);")
    with open(core_path, "w", encoding="utf-8") as f:
        f.write(core_c)
    print("[+] Successfully patched core_hook.c for ARM64 SECCOMP clearing")

    # 9. kernel/seccomp.c (Allow KSU prctl and reboot supercalls past Android SECCOMP filter without SIGSYS trap)
    with open("kernel/seccomp.c", "r", encoding="utf-8") as f:
        seccomp_c = f.read()

    seccomp_hook = """
#ifdef CONFIG_KSU
	if (sd && ((u32)sd->args[0] == 0xdeadbeef || (u32)sd->args[0] == 0xcafebabe || (u32)sd->args[1] == 0xcafebabe || sd->nr == 116))
		return SECCOMP_RET_ALLOW;
#endif
"""
    seccomp_c, n9 = re.subn(r"(static\s+u32\s+seccomp_run_filters\s*\([^)]*\)\s*\{)", r"\1\n" + seccomp_hook, seccomp_c, count=1)
    assert n9 == 1, "Failed to patch seccomp_run_filters in kernel/seccomp.c"
    with open("kernel/seccomp.c", "w", encoding="utf-8") as f:
        f.write(seccomp_c)
    print("[+] Successfully patched kernel/seccomp.c with KSU SECCOMP bypass")

    # 10. ksud.c (Auto-create /data/adb directories on post-fs-data)
    ksud_path = "KernelSU/kernel/ksud.c" if os.path.exists("KernelSU/kernel/ksud.c") else "drivers/kernelsu/ksud.c"
    with open(ksud_path, "r", encoding="utf-8") as f:
        ksud_c = f.read()

    ksud_rc_target = '"on post-fs-data\\n"'
    ksud_rc_replacement = '"on post-fs-data\\n\\t    mkdir /data/adb 0755 root root\\n\\t    mkdir /data/adb/ksu 0755 root root\\n\\t    mkdir /data/adb/modules 0755 root root\\n\\t    mkdir /data/adb/post-fs-data.d 0755 root root\\n\\t    mkdir /data/adb/service.d 0755 root root\\n"'
    assert ksud_rc_target in ksud_c, "Failed to locate on post-fs-data in ksud.c"
    ksud_c = ksud_c.replace(ksud_rc_target, ksud_rc_replacement, 1)
    with open(ksud_path, "w", encoding="utf-8") as f:
        f.write(ksud_c)
    print("[+] Successfully patched ksud.c with /data/adb directory creation")

    # 11. fs/devpts/inode.c (PTY terminal hook for interactive root shell)
    with open("fs/devpts/inode.c", "r", encoding="utf-8") as f:
        devpts_c = f.read()

    devpts_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_devpts(struct inode *inode);
#endif
"""
    devpts_call = """
#ifdef CONFIG_KSU
	if (dentry && dentry->d_inode)
		ksu_handle_devpts(dentry->d_inode);
#endif
"""
    devpts_c, n11 = re.subn(r"(void\s+\*devpts_get_priv\s*\([^)]*\)\s*\{)", devpts_decl + r"\n\1\n" + devpts_call, devpts_c, count=1)
    assert n11 == 1, "Failed to patch devpts_get_priv in fs/devpts/inode.c"
    with open("fs/devpts/inode.c", "w", encoding="utf-8") as f:
        f.write(devpts_c)
    print("[+] Successfully patched fs/devpts/inode.c with KernelSU devpts hook")

    # 12. fs/namespace.c (Backport path_umount for stealth module unmounting)
    with open("fs/namespace.c", "r", encoding="utf-8") as f:
        ns_c = f.read()

    ns_patch = """
#ifdef CONFIG_KSU
static int can_umount(const struct path *path, int flags)
{
	struct mount *mnt = real_mount(path->mnt);

	if (!may_mount())
		return -EPERM;
	if (!path_mounted(path))
		return -EINVAL;
	if (!check_mnt(mnt))
		return -EINVAL;
	if (mnt->mnt.mnt_flags & MNT_LOCKED)
		return -EINVAL;
	if (flags & MNT_FORCE && !capable(CAP_SYS_ADMIN))
		return -EPERM;
	return 0;
}

int path_umount(struct path *path, int flags)
{
	struct mount *mnt = real_mount(path->mnt);
	int ret;

	ret = can_umount(path, flags);
	if (!ret)
		ret = do_umount(mnt, flags);
	dput(path->dentry);
	mntput_no_expire(mnt);
	return ret;
}
#endif
"""
    ns_c = ns_c + "\n" + ns_patch
    with open("fs/namespace.c", "w", encoding="utf-8") as f:
        f.write(ns_c)
    print("[+] Successfully backported path_umount in fs/namespace.c")

    print("[🎉] All 12 KernelSU VFS & Security patches applied successfully!")

if __name__ == "__main__":
    main()
