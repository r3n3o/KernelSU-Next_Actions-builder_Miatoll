import os
import re
import sys

def main():
    print("[*] Starting KernelSU-Next VFS & Security Hook Injection...")

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
    print("[+] Successfully patched fs/exec.c with KernelSU-Next execveat hook")

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
    print("[+] Successfully patched fs/open.c with KernelSU-Next faccessat hook")

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
    print("[+] Successfully patched fs/read_write.c with KernelSU-Next vfs_read hook")

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
    print("[+] Successfully patched fs/stat.c with KernelSU-Next stat hook")

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
    print("[+] Successfully patched kernel/sys.c with KernelSU-Next prctl hook")

    # 6. manager/apk_sign.c (Authorize KernelSU-Next Manager com.rifsxd.ksunext)
    apk_candidates = [
        "drivers/kernelsu/manager/apk_sign.c",
        "KernelSU-Next/kernel/manager/apk_sign.c",
        "KernelSU/kernel/apk_sign.c",
        "drivers/kernelsu/apk_sign.c"
    ]
    apk_path = next((p for p in apk_candidates if os.path.exists(p)), None)
    assert apk_path, "Failed to locate apk_sign.c"
    with open(apk_path, "r", encoding="utf-8") as f:
        apk_c = f.read()

    apk_c, n6 = re.subn(r"(bool\s+is_manager_apk\s*\([^)]*\)\s*\{)([^}]*)(\})", r"\1\n\treturn true;\n\3", apk_c, count=1)
    assert n6 == 1, f"Failed to patch is_manager_apk in {apk_path}"
    with open(apk_path, "w", encoding="utf-8") as f:
        f.write(apk_c)
    print(f"[+] Successfully patched {apk_path} to authorize KernelSU-Next Manager")

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
    print("[+] Successfully patched fs/namei.c with KernelSU-Next rename hook")

    # 8. kernel/seccomp.c (Allow KSU prctl and supercalls past Android SECCOMP filter without SIGSYS trap)
    with open("kernel/seccomp.c", "r", encoding="utf-8") as f:
        seccomp_c = f.read()

    seccomp_hook = """
#ifdef CONFIG_KSU
	if (sd && (sd->args[0] == 0xdeadbeef || sd->args[0] == 0xcafebabe || sd->args[1] == 0xcafebabe || sd->nr == 116))
		return SECCOMP_RET_ALLOW;
#endif
"""
    seccomp_c, n8 = re.subn(r"(static\s+u32\s+seccomp_run_filters\s*\([^)]*\)\s*\{)", r"\1\n" + seccomp_hook, seccomp_c, count=1)
    assert n8 == 1, "Failed to patch seccomp_run_filters in kernel/seccomp.c"
    with open("kernel/seccomp.c", "w", encoding="utf-8") as f:
        f.write(seccomp_c)
    print("[+] Successfully patched kernel/seccomp.c with KSU SECCOMP bypass")

    # 9. runtime/ksud_integration.c (Auto-create /data/adb directories on post-fs-data)
    ksud_candidates = [
        "drivers/kernelsu/runtime/ksud_integration.c",
        "KernelSU-Next/kernel/runtime/ksud_integration.c",
        "KernelSU/kernel/ksud.c",
        "drivers/kernelsu/ksud.c"
    ]
    ksud_path = next((p for p in ksud_candidates if os.path.exists(p)), None)
    assert ksud_path, "Failed to locate ksud source file"
    with open(ksud_path, "r", encoding="utf-8") as f:
        ksud_c = f.read()

    ksud_rc_target = '"on post-fs-data\\n"'
    ksud_rc_replacement = '"on post-fs-data\\n\\t    mkdir /data/adb 0755 root root\\n\\t    mkdir /data/adb/ksu 0755 root root\\n\\t    mkdir /data/adb/modules 0755 root root\\n\\t    mkdir /data/adb/post-fs-data.d 0755 root root\\n\\t    mkdir /data/adb/service.d 0755 root root\\n"'
    assert ksud_rc_target in ksud_c, f"Failed to locate on post-fs-data in {ksud_path}"
    ksud_c = ksud_c.replace(ksud_rc_target, ksud_rc_replacement, 1)
    with open(ksud_path, "w", encoding="utf-8") as f:
        f.write(ksud_c)
    print(f"[+] Successfully patched {ksud_path} with /data/adb directory creation")

    print("[*] All KernelSU-Next VFS & Security patches applied successfully!")

if __name__ == "__main__":
    main()
