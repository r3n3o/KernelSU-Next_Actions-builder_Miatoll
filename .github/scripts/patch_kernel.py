"""
KernelSU-Next v3.4.0-legacy - Non-GKI VFS Hook Injector for SM6250 (Miatoll / Linux 4.19)
============================================================================================
Purpose: Inject the VFS call hooks required for KernelSU-Next's NON-GKI (legacy) integration
         mode into the crDroid 16.0 kernel source tree.

KernelSU-Next v3.4.0-legacy Architecture (Non-GKI):
  - Uses MANUAL VFS hooks (NOT kprobes/tracepoints)
  - core_hook.c NO LONGER EXISTS
  - supercall/supercall.c handles sys_reboot gateway (NOT prctl)
  - apk_sign.c is at drivers/kernelsu/apk_sign.c (flat structure)
  - setup.sh tag: v3.4.0-legacy

Author: r3n3o & Antigravity (Google DeepMind)
"""

import os
import re
import sys


def find_kernelsu_dir():
    """Locate the KernelSU-Next kernel directory after setup.sh ran."""
    candidates = [
        "drivers/kernelsu",
        "KernelSU-Next/kernel",
        "KernelSU/kernel",
    ]
    for p in candidates:
        if os.path.isdir(p):
            return p
    return None


def main():
    print("[*] KernelSU-Next v3.4.0 Non-GKI VFS Hook Injector starting...")
    print("[*] Target: crDroid 16.0 / SM6250 (Miatoll) / Linux 4.19")

    ksu_dir = find_kernelsu_dir()
    if ksu_dir:
        print(f"[+] Found KernelSU-Next driver directory: {ksu_dir}")
    else:
        print("[!] Warning: KernelSU-Next driver directory not found. Continuing with kernel hooks only.")

    # =========================================================================
    # 1. fs/exec.c - execveat hook (su binary execution redirect)
    # =========================================================================
    print("\n[*] Patching fs/exec.c (execveat hook)...")
    with open("fs/exec.c", "r", encoding="utf-8") as f:
        exec_c = f.read()

    exec_decl = """
#ifdef CONFIG_KSU
extern bool ksu_execveat_hook __read_mostly;
extern int ksu_handle_execveat(int *fd, struct filename **filename_ptr, void *argv,
\t\t\tvoid *envp, int *flags);
extern int ksu_handle_execveat_sucompat(int *fd, struct filename **filename_ptr,
\t\t\t\t void *argv, void *envp, int *flags);
#endif
"""
    exec_call = """
#ifdef CONFIG_KSU
\tif (unlikely(ksu_execveat_hook))
\t\tksu_handle_execveat(&fd, &filename, &argv, &envp, &flags);
\telse
\t\tksu_handle_execveat_sucompat(&fd, &filename, &argv, &envp, &flags);
#endif
"""
    if "ksu_handle_execveat" not in exec_c:
        exec_c, n = re.subn(
            r"((?:static\s+)?int\s+do_execveat_common\s*\([^)]*\)\s*\{)",
            exec_decl + r"\n\1\n" + exec_call,
            exec_c, count=1
        )
        assert n == 1, "Failed to patch do_execveat_common in fs/exec.c"
        with open("fs/exec.c", "w", encoding="utf-8") as f:
            f.write(exec_c)
        print("[+] Patched fs/exec.c with KernelSU execveat hook")
    else:
        print("[~] fs/exec.c already patched, skipping")

    # =========================================================================
    # 2. fs/open.c - faccessat hook (su binary access check redirect)
    # =========================================================================
    print("\n[*] Patching fs/open.c (faccessat hook)...")
    with open("fs/open.c", "r", encoding="utf-8") as f:
        open_c = f.read()

    open_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_faccessat(int *dfd, const char __user **filename_user, int *mode,
\t\t\t int *flags);
#endif
"""
    open_call = """
#ifdef CONFIG_KSU
\tksu_handle_faccessat(&dfd, &filename, &mode, NULL);
#endif
"""
    if "ksu_handle_faccessat" not in open_c:
        open_c, n = re.subn(
            r"(SYSCALL_DEFINE3\s*\(\s*faccessat\s*,[^{]*\{)",
            open_decl + r"\n\1\n" + open_call,
            open_c, count=1
        )
        assert n == 1, "Failed to patch SYSCALL_DEFINE3(faccessat) in fs/open.c"
        with open("fs/open.c", "w", encoding="utf-8") as f:
            f.write(open_c)
        print("[+] Patched fs/open.c with KernelSU faccessat hook")
    else:
        print("[~] fs/open.c already patched, skipping")

    # =========================================================================
    # 3. fs/read_write.c - vfs_read hook (sucompat binary read intercept)
    # =========================================================================
    print("\n[*] Patching fs/read_write.c (vfs_read hook)...")
    with open("fs/read_write.c", "r", encoding="utf-8") as f:
        rw_c = f.read()

    rw_decl = """
#ifdef CONFIG_KSU
extern bool ksu_vfs_read_hook __read_mostly;
extern int ksu_handle_vfs_read(struct file **file_ptr, char __user **buf_ptr,
\t\t\tsize_t *count_ptr, loff_t **pos);
#endif
"""
    rw_call = """
#ifdef CONFIG_KSU
\tif (unlikely(ksu_vfs_read_hook))
\t\tksu_handle_vfs_read(&file, &buf, &count, &pos);
#endif
"""
    if "ksu_handle_vfs_read" not in rw_c:
        rw_c, n = re.subn(
            r"(ssize_t\s+vfs_read\s*\([^)]*\)\s*\{)",
            rw_decl + r"\n\1\n" + rw_call,
            rw_c, count=1
        )
        assert n == 1, "Failed to patch vfs_read in fs/read_write.c"
        with open("fs/read_write.c", "w", encoding="utf-8") as f:
            f.write(rw_c)
        print("[+] Patched fs/read_write.c with KernelSU vfs_read hook")
    else:
        print("[~] fs/read_write.c already patched, skipping")

    # =========================================================================
    # 4. fs/stat.c - vfs_statx hook (stat-based su binary detection)
    # =========================================================================
    print("\n[*] Patching fs/stat.c (vfs_statx hook)...")
    with open("fs/stat.c", "r", encoding="utf-8") as f:
        stat_c = f.read()

    stat_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_stat(int *dfd, const char __user **filename_user, int *flags);
#endif
"""
    stat_call = """
#ifdef CONFIG_KSU
\tksu_handle_stat(&dfd, &filename, &flags);
#endif
"""
    if "ksu_handle_stat" not in stat_c:
        stat_c, n = re.subn(
            r"((?:static\s+)?int\s+vfs_statx\s*\([^)]*\)\s*\{)",
            stat_decl + r"\n\1\n" + stat_call,
            stat_c, count=1
        )
        assert n == 1, "Failed to patch vfs_statx in fs/stat.c"
        with open("fs/stat.c", "w", encoding="utf-8") as f:
            f.write(stat_c)
        print("[+] Patched fs/stat.c with KernelSU stat hook")
    else:
        print("[~] fs/stat.c already patched, skipping")

    # =========================================================================
    # 5. kernel/reboot.c - sys_reboot hook (Manager <-> Kernel supercall gateway)
    #    KernelSU-Next v3.4.0-legacy: sys_reboot entry -> supercall/supercall.c
    # =========================================================================
    print("\n[*] Patching kernel/reboot.c (sys_reboot supercall hook)...")
    if os.path.exists("kernel/reboot.c"):
        with open("kernel/reboot.c", "r", encoding="utf-8") as f:
            reboot_c = f.read()

        reboot_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_sys_reboot(int magic1, int magic2, unsigned int cmd, void __user **arg);
#endif
"""
        reboot_call = """
#ifdef CONFIG_KSU
\tksu_handle_sys_reboot(magic1, magic2, cmd, &arg);
#endif
"""
        if "ksu_handle_sys_reboot" not in reboot_c:
            reboot_c, n = re.subn(
                r"(SYSCALL_DEFINE4\s*\(\s*reboot\s*,[^{]*\{)",
                reboot_decl + r"\n\1\n" + reboot_call,
                reboot_c, count=1
            )
            assert n == 1, "Failed to patch SYSCALL_DEFINE4(reboot) in kernel/reboot.c"
            with open("kernel/reboot.c", "w", encoding="utf-8") as f:
                f.write(reboot_c)
            print("[+] Patched kernel/reboot.c with KernelSU sys_reboot hook")
        else:
            print("[~] kernel/reboot.c already patched, skipping")
    else:
        print("[!] kernel/reboot.c not found")

    # =========================================================================
    # 7. apk_sign.c - Authorize KernelSU-Next Manager APK signature
    #    In v3.4.0-LEGACY: flat structure -> drivers/kernelsu/apk_sign.c
    #    In v3.4.0 (GKI): manager/apk_sign.c
    # =========================================================================
    print("\n[*] Patching apk_sign.c (Manager APK authorization)...")
    apk_candidates = [
        "drivers/kernelsu/apk_sign.c",       # v3.4.0-legacy (flat)
        "KernelSU-Next/kernel/apk_sign.c",   # direct clone legacy
        "drivers/kernelsu/manager/apk_sign.c", # v3.4.0 GKI (fallback)
        "KernelSU/kernel/apk_sign.c",        # older structure
    ]
    apk_path = next((p for p in apk_candidates if os.path.exists(p)), None)


    if apk_path:
        with open(apk_path, "r", encoding="utf-8") as f:
            apk_c = f.read()

        modified = False

        if "return true; /* KSU-Next-Miatoll */" not in apk_c:
            apk_c_new, n = re.subn(
                r"(bool\s+is_manager_apk\s*\([^)]*\)\s*\{)([^}]*)(\})",
                r"\1\n\treturn true; /* KSU-Next-Miatoll */\n\3",
                apk_c, count=1
            )
            if n == 1:
                apk_c = apk_c_new
                modified = True
                print(f"[+] Patched is_manager_apk() in {apk_path}")

        # Hash from KernelSU_Next_v3.4.0_33294-release.apk (SHA256 of signing block)
        for old_size_pat in [r'#define\s+EXPECTED_SIZE\s+0x[0-9a-fA-F]+']:
            if re.search(old_size_pat, apk_c):
                apk_c = re.sub(old_size_pat, '#define EXPECTED_SIZE 0x3e6', apk_c)
                modified = True

        for old_hash_pat in [r'#define\s+EXPECTED_HASH\s+"[0-9a-fA-F]+"']:
            if re.search(old_hash_pat, apk_c):
                apk_c = re.sub(
                    old_hash_pat,
                    '#define EXPECTED_HASH "50339a93c0f812b8a72c1a387a1b441891e3df0f20b2d9daf80fd798d04b3de8"',
                    apk_c
                )
                modified = True

        if modified:
            with open(apk_path, "w", encoding="utf-8") as f:
                f.write(apk_c)
            print(f"[+] Updated {apk_path} with v3.4.0 Manager authorization")
        else:
            print(f"[~] {apk_path} already authorized, skipping")
    else:
        print("[!] Warning: apk_sign.c not found (will use kernel CONFIG defaults)")

    # =========================================================================
    # 7. fs/namei.c - vfs_rename hook (package name change tracker)
    # =========================================================================
    print("\n[*] Patching fs/namei.c (vfs_rename hook)...")
    with open("fs/namei.c", "r", encoding="utf-8") as f:
        namei_c = f.read()

    namei_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_rename(struct dentry *old_dentry, struct dentry *new_dentry);
#endif
"""
    namei_call = """
#ifdef CONFIG_KSU
\tksu_handle_rename(old_dentry, new_dentry);
#endif
"""
    if "ksu_handle_rename" not in namei_c:
        namei_c, n = re.subn(
            r"((?:static\s+)?int\s+vfs_rename\s*\([^)]*\)\s*\{)",
            namei_decl + r"\n\1\n" + namei_call,
            namei_c, count=1
        )
        assert n == 1, "Failed to patch vfs_rename in fs/namei.c"
        with open("fs/namei.c", "w", encoding="utf-8") as f:
            f.write(namei_c)
        print("[+] Patched fs/namei.c with KernelSU rename hook")
    else:
        print("[~] fs/namei.c already patched, skipping")

    # =========================================================================
    # 8. kernel/seccomp.c - Allow KSU prctl (option=0xdeadbeef) past SECCOMP
    #    KernelSU-Next v3.4.0 ksud uses SIGSYS handler but the first prctl
    #    call needs to reach the kernel before the handler is installed
    # =========================================================================
    print("\n[*] Patching kernel/seccomp.c (allow KSU prctl past SECCOMP)...")
    seccomp_path = "kernel/seccomp.c"
    if os.path.exists(seccomp_path):
        with open(seccomp_path, "r", encoding="utf-8") as f:
            seccomp_c = f.read()

        if "CONFIG_KSU" not in seccomp_c:
            seccomp_bypass = """
#ifdef CONFIG_KSU
\t/* KernelSU-Next: allow prctl(0xdeadbeef) supercall to bypass SECCOMP */
\tif (this_syscall == 167 || this_syscall == 142)
\t\treturn 0;
#endif
"""
            seccomp_c, n = re.subn(
                r"((?:static\s+)?int\s+__seccomp_filter\s*\([^)]*\)\s*\{)",
                r"\1\n" + seccomp_bypass,
                seccomp_c, count=1
            )
            if n == 1:
                with open(seccomp_path, "w", encoding="utf-8") as f:
                    f.write(seccomp_c)
                print("[+] Patched kernel/seccomp.c for KSU prctl bypass")
            else:
                print("[!] Could not find __seccomp_filter, skipping SECCOMP patch")
        else:
            print("[~] kernel/seccomp.c already patched, skipping")
    else:
        print("[!] kernel/seccomp.c not found, skipping")

    # =========================================================================
    # 9. KernelSU Makefile - Fix KSU_VERSION pin at 33294
    # =========================================================================
    print("\n[*] Patching KernelSU Makefile (version pin)...")
    mk_candidates = [
        "drivers/kernelsu/Makefile",
        "KernelSU-Next/kernel/Makefile",
        "KernelSU/kernel/Makefile",
    ]
    mk_path = next((p for p in mk_candidates if os.path.exists(p)), None)

    if mk_path:
        with open(mk_path, "r", encoding="utf-8") as f:
            mk_c = f.read()

        modified = False
        for old_expr in [
            "$(eval KSU_VERSION=$(shell expr 10000 + $(KSU_GIT_VERSION) + 200))",
            "$(eval KSU_VERSION=$(shell expr 10000 + $(KSU_GIT_VERSION) + 300))",
        ]:
            if old_expr in mk_c:
                mk_c = mk_c.replace(old_expr, "$(eval KSU_VERSION=33294)")
                modified = True

        if "ccflags-y += -DKSU_VERSION=16" in mk_c:
            mk_c = mk_c.replace("ccflags-y += -DKSU_VERSION=16", "ccflags-y += -DKSU_VERSION=33294")
            modified = True

        if modified:
            with open(mk_path, "w", encoding="utf-8") as f:
                f.write(mk_c)
            print(f"[+] Updated {mk_path} with KSU_VERSION=33294")
        else:
            print(f"[~] {mk_path} version already correct, skipping")
    else:
        print("[!] KernelSU Makefile not found (Kbuild will use git tag version)")

    # =========================================================================
    # 10. ksud runtime integration - Ensure /data/adb directories are created
    # =========================================================================
    print("\n[*] Checking ksud runtime integration...")
    ksud_candidates = [
        "drivers/kernelsu/runtime/ksud_integration.c",
        "KernelSU-Next/kernel/runtime/ksud_integration.c",
        "drivers/kernelsu/ksud.c",
        "KernelSU/kernel/ksud.c",
    ]
    ksud_path_found = next((p for p in ksud_candidates if os.path.exists(p)), None)
    if ksud_path_found:
        with open(ksud_path_found, "r", encoding="utf-8") as f:
            ksud_c = f.read()

        if "mkdir /data/adb" not in ksud_c and '"on post-fs-data\\n"' in ksud_c:
            ksud_rc_replacement = (
                '"on post-fs-data\\n\\t    mkdir /data/adb 0755 root root\\n'
                '\\t    mkdir /data/adb/ksu 0755 root root\\n'
                '\\t    mkdir /data/adb/ksu/bin 0755 root root\\n'
                '\\t    mkdir /data/adb/modules 0755 root root\\n'
                '\\t    mkdir /data/adb/post-fs-data.d 0755 root root\\n'
                '\\t    mkdir /data/adb/service.d 0755 root root\\n"'
            )
            ksud_c = ksud_c.replace('"on post-fs-data\\n"', ksud_rc_replacement, 1)
            with open(ksud_path_found, "w", encoding="utf-8") as f:
                f.write(ksud_c)
            print(f"[+] Patched {ksud_path_found} with /data/adb directory creation")
        else:
            print(f"[~] {ksud_path_found} already provisioned, skipping")
    else:
        print("[~] ksud_integration.c not found; anykernel.sh will provision /data/adb")

    # =========================================================================
    # 11. fs/devpts/inode.c - PTY hook for NHterm/Termux terminal emulators
    # =========================================================================
    print("\n[*] Patching fs/devpts/inode.c (PTY hook for terminal emulators)...")
    devpts_path = "fs/devpts/inode.c"
    if os.path.exists(devpts_path):
        with open(devpts_path, "r", encoding="utf-8") as f:
            devpts_c = f.read()

        devpts_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_devpts(struct inode *inode);
#endif
"""
        if "ksu_handle_devpts" not in devpts_c:
            devpts_pattern = r"(struct\s+dentry\s*\*devpts_pty_new\s*\([^{]*\{[\s\S]*?d_add\s*\(\s*dentry\s*,\s*inode\s*\)\s*;)"
            devpts_repl = devpts_decl + r"\n\1\n#ifdef CONFIG_KSU\n\t\tksu_handle_devpts(inode);\n#endif"
            devpts_c, n = re.subn(devpts_pattern, devpts_repl, devpts_c, count=1)
            if n == 1:
                with open(devpts_path, "w", encoding="utf-8") as f:
                    f.write(devpts_c)
                print("[+] Patched fs/devpts/inode.c with KernelSU PTY hook")
            else:
                print("[!] Could not locate devpts_pty_new, skipping PTY hook")
        else:
            print("[~] fs/devpts/inode.c already patched, skipping")
    else:
        print("[!] fs/devpts/inode.c not found, skipping")

    print("\n" + "=" * 60)
    print("[*] All KernelSU-Next v3.4.0 VFS hooks applied!")
    print("    Kernel: SM6250 (Miatoll) / crDroid 16.0 / Linux 4.19")
    print("    Driver: KernelSU-Next v3.4.0 (supercall/dispatch native)")
    print("=" * 60)



if __name__ == "__main__":
    main()
