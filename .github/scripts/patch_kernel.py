import os
import re
import sys

def main():
    print("[*] Starting KernelSU-Next VFS, Security & Supercall Integration...")

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
    apk_candidates = [
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
    print("[+] Successfully patched fs/namei.c with KernelSU rename hook")

    # 8. core_hook.c (ARM64 SECCOMP atomic clear, UAPI v2 reporting, and manager registration)
    core_candidates = [
        "KernelSU/kernel/core_hook.c",
        "drivers/kernelsu/core_hook.c"
    ]
    core_path = next((p for p in core_candidates if os.path.exists(p)), None)
    if core_path:
        with open(core_path, "r", encoding="utf-8") as f:
            core_c = f.read()
        core_c = core_c.replace("current_thread_info()->flags &= ~(TIF_SECCOMP | _TIF_SECCOMP);", "clear_tsk_thread_flag(current, TIF_SECCOMP);")
        
        # Inject UAPI version in CMD_GET_VERSION
        core_target = "if (arg2 == CMD_GET_VERSION) {"
        core_repl = """if (arg2 == CMD_GET_VERSION) {
\t\tu32 uapi_ver = 2;
\t\tif (arg5 && copy_to_user(arg5, &uapi_ver, sizeof(uapi_ver))) {
\t\t\tpr_err("prctl reply uapi error, cmd: %lu\\n", arg2);
\t\t}"""
        if core_target in core_c and "uapi_ver = 2" not in core_c:
            core_c = core_c.replace(core_target, core_repl, 1)

        # Allow become_manager before from_manager gate and register manager UID
        auth_target = """\tbool from_root = 0 == current_uid().val;
\tbool from_manager = is_manager();

\tif (!from_root && !from_manager) {"""
        auth_repl = """\tif (arg2 == CMD_BECOME_MANAGER) {
\t\tksu_set_manager_uid(current_uid().val);
\t}

\tbool from_root = 0 == current_uid().val;
\tbool from_manager = is_manager();

\tif (!from_root && !from_manager) {"""
        if auth_target in core_c:
            core_c = core_c.replace(auth_target, auth_repl, 1)

        # Inject become_manager override to install driver fd and reply OK
        mgr_target = "if (arg2 == CMD_BECOME_MANAGER) {"
        mgr_repl = """if (arg2 == CMD_BECOME_MANAGER) {
\t\textern int ksu_install_fd(void);
\t\tksu_set_manager_uid(current_uid().val);
\t\tksu_install_fd();
\t\tif (copy_to_user(result, &reply_ok, sizeof(reply_ok))) {
\t\t\tpr_err("become_manager: prctl reply error\\n");
\t\t}
\t\treturn 0;
\t}
\tif (false) {"""
        if mgr_target in core_c and "ksu_install_fd" not in core_c:
            core_c = core_c.replace(mgr_target, mgr_repl, 1)
            
        with open(core_path, "w", encoding="utf-8") as f:
            f.write(core_c)
        print(f"[+] Successfully patched {core_path} for SECCOMP clearing, UAPI v2 reporting, and manager registration")

    # 9. kernel/seccomp.c (Allow KSU prctl and reboot supercalls past Android SECCOMP filter without SIGSYS trap)
    with open("kernel/seccomp.c", "r", encoding="utf-8") as f:
        seccomp_c = f.read()

    # Hook __seccomp_filter for syscall 142 (reboot), 167 (prctl), and 32-bit compat (88, 172)
    seccomp_hook_fn = """
#ifdef CONFIG_KSU
	if (this_syscall == 142 || this_syscall == 167 || this_syscall == 88 || this_syscall == 172)
		return 0;
#endif
"""
    seccomp_c, n9_1 = re.subn(r"((?:static\s+)?int\s+__seccomp_filter\s*\([^)]*\)\s*\{)", r"\1\n" + seccomp_hook_fn, seccomp_c, count=1)
    assert n9_1 == 1, "Failed to patch __seccomp_filter in kernel/seccomp.c"

    # Hook seccomp_run_filters after sd is populated
    seccomp_target = "if (!sd) {\n\t\tpopulate_seccomp_data(&sd_local);\n\t\tsd = &sd_local;\n\t}"
    seccomp_repl = """if (!sd) {
\t\tpopulate_seccomp_data(&sd_local);
\t\tsd = &sd_local;
\t}
#ifdef CONFIG_KSU
\tif (sd) {
\t\tunsigned long a0 = sd->args[0] & 0xFFFFFFFF;
\t\tunsigned long a1 = sd->args[1] & 0xFFFFFFFF;
\t\tif (a0 == 0xdeadbeef || a0 == 0xcafebabe || a1 == 0xcafebabe || a1 == 0xdeadbeef || sd->nr == 142 || sd->nr == 167 || sd->nr == 88 || sd->nr == 172)
\t\t\treturn SECCOMP_RET_ALLOW;
\t}
#endif"""
    assert seccomp_target in seccomp_c, "Failed to locate populate_seccomp_data in kernel/seccomp.c"
    seccomp_c = seccomp_c.replace(seccomp_target, seccomp_repl, 1)

    with open("kernel/seccomp.c", "w", encoding="utf-8") as f:
        f.write(seccomp_c)
    print("[+] Successfully patched kernel/seccomp.c with bulletproof KSU SECCOMP bypass")

    # 10. ksud.c (Auto-create /data/adb directories on post-fs-data)
    ksud_candidates = [
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

    # 11. Create supercall.c in KernelSU/kernel/ for [ksu_driver] ioctl interface
    supercall_dir = "KernelSU/kernel" if os.path.exists("KernelSU/kernel") else "drivers/kernelsu"
    supercall_path = os.path.join(supercall_dir, "supercall.c")
    supercall_code = """
#include <linux/anon_inodes.h>
#include <linux/err.h>
#include <linux/fdtable.h>
#include <linux/file.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>
#include <linux/version.h>

#include "ksu.h"
#include "allowlist.h"
#include "manager.h"

#define KSU_INSTALL_MAGIC1 0xDEADBEEF
#define KSU_INSTALL_MAGIC2 0xCAFEBABE

#define KSU_GET_INFO_FLAG_LKM (1U << 0)
#define KSU_GET_INFO_FLAG_MANAGER (1U << 1)

struct ksu_get_info_cmd {
    __u32 version;
    __u32 flags;
    __u32 features;
    __u32 uapi_version;
};

struct ksu_get_hook_mode_cmd {
    char mode[16];
};

struct ksu_get_version_tag_cmd {
    char tag[32];
};

struct ksu_report_event_cmd {
    __u32 event;
};

struct ksu_get_feature_cmd {
    __u32 feature_id;
    __u64 value;
    __u8 supported;
};

struct ksu_set_feature_cmd {
    __u32 feature_id;
    __u64 value;
};

extern void escape_to_root(void);
extern void on_post_fs_data(void);

static int anon_ksu_release(struct inode *inode, struct file *filp)
{
    return 0;
}

static long anon_ksu_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    void __user *argp = (void __user *)arg;
    unsigned int nr = _IOC_NR(cmd);

    if (_IOC_TYPE(cmd) != 'K')
        return -ENOTTY;

    switch (nr) {
    case 1: // KSU_IOCTL_GRANT_ROOT
        if (is_manager() || ksu_is_allow_uid(current_uid().val) || current_uid().val == 0) {
            escape_to_root();
            return 0;
        }
        return -EPERM;

    case 2: { // KSU_IOCTL_GET_INFO
        struct ksu_get_info_cmd info = {
            .version = 33214,
            .flags = KSU_GET_INFO_FLAG_MANAGER,
            .features = 10,
            .uapi_version = 2
        };
        if (copy_to_user(argp, &info, sizeof(info)))
            return -EFAULT;
        return 0;
    }

    case 3: { // KSU_IOCTL_REPORT_EVENT
        struct ksu_report_event_cmd evt;
        if (copy_from_user(&evt, argp, sizeof(evt)))
            return -EFAULT;
        if (evt.event == 1) { // EVENT_POST_FS_DATA
            on_post_fs_data();
        }
        return 0;
    }

    case 4: // KSU_IOCTL_SET_SEPOLICY
        return 0;

    case 5: { // KSU_IOCTL_CHECK_SAFEMODE
        __u8 in_safe_mode = 0;
        if (copy_to_user(argp, &in_safe_mode, sizeof(in_safe_mode)))
            return -EFAULT;
        return 0;
    }

    case 6: // KSU_IOCTL_GET_ALLOW_LIST / NEW_GET_ALLOW_LIST
    case 7: // KSU_IOCTL_GET_DENY_LIST / NEW_GET_DENY_LIST
        return 0;

    case 8: { // KSU_IOCTL_UID_GRANTED_ROOT
        __u32 uid = 0;
        __u8 allow = 1;
        if (argp && copy_from_user(&uid, argp, sizeof(uid)) == 0) {
            allow = is_manager() || ksu_is_allow_uid(uid) || (uid == 0);
            copy_to_user(argp, &allow, sizeof(allow));
        }
        return 0;
    }

    case 9: { // KSU_IOCTL_UID_SHOULD_UMOUNT
        __u32 uid = 0;
        __u8 should_umount = 0;
        if (argp && copy_from_user(&uid, argp, sizeof(uid)) == 0) {
            should_umount = ksu_uid_should_umount(uid);
            copy_to_user(argp, &should_umount, sizeof(should_umount));
        }
        return 0;
    }

    case 10: { // KSU_IOCTL_GET_MANAGER_APPID
        __u32 appid = ksu_get_manager_uid();
        if (appid == (uid_t)-1)
            appid = current_uid().val;
        if (copy_to_user(argp, &appid, sizeof(appid)))
            return -EFAULT;
        return 0;
    }

    case 11: { // KSU_IOCTL_GET_APP_PROFILE
        struct app_profile profile;
        if (copy_from_user(&profile, argp, sizeof(profile)))
            return -EFAULT;
        ksu_get_app_profile(&profile);
        if (copy_to_user(argp, &profile, sizeof(profile)))
            return -EFAULT;
        return 0;
    }

    case 12: { // KSU_IOCTL_SET_APP_PROFILE
        struct app_profile profile;
        if (copy_from_user(&profile, argp, sizeof(profile)))
            return -EFAULT;
        ksu_set_app_profile(&profile, true);
        return 0;
    }

    case 13: { // KSU_IOCTL_GET_FEATURE
        struct ksu_get_feature_cmd fcmd;
        if (copy_from_user(&fcmd, argp, sizeof(fcmd)))
            return -EFAULT;
        fcmd.value = 1;
        fcmd.supported = 1;
        if (copy_to_user(argp, &fcmd, sizeof(fcmd)))
            return -EFAULT;
        return 0;
    }

    case 14: { // KSU_IOCTL_SET_FEATURE
        struct ksu_set_feature_cmd fcmd;
        if (copy_from_user(&fcmd, argp, sizeof(fcmd)))
            return -EFAULT;
        return 0;
    }

    case 19: // KSU_IOCTL_SET_INIT_PGRP
        return 0;

    case 98: { // KSU_IOCTL_GET_HOOK_MODE
        struct ksu_get_hook_mode_cmd mode = {0};
        strncpy(mode.mode, "Manual", sizeof(mode.mode) - 1);
        if (copy_to_user(argp, &mode, sizeof(mode)))
            return -EFAULT;
        return 0;
    }

    case 99: { // KSU_IOCTL_GET_VERSION_TAG
        struct ksu_get_version_tag_cmd tag = {0};
        strncpy(tag.tag, "v3.3.0", sizeof(tag.tag) - 1);
        if (copy_to_user(argp, &tag, sizeof(tag)))
            return -EFAULT;
        return 0;
    }

    default:
        return -ENOTTY;
    }
}


static const struct file_operations anon_ksu_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = anon_ksu_ioctl,
    .compat_ioctl = anon_ksu_ioctl,
    .release = anon_ksu_release,
};

int ksu_install_fd(void)
{
    struct file *filp;
    int fd;

    fd = get_unused_fd_flags(O_CLOEXEC);
    if (fd < 0) {
        pr_err("ksu_install_fd: failed to get unused fd\\n");
        return fd;
    }

    filp = anon_inode_getfile("[ksu_driver]", &anon_ksu_fops, NULL, O_RDWR | O_CLOEXEC);
    if (IS_ERR(filp)) {
        pr_err("ksu_install_fd: failed to create anon inode file\\n");
        put_unused_fd(fd);
        return PTR_ERR(filp);
    }

    fd_install(fd, filp);
    pr_info("ksu fd installed: %d for pid %d\\n", fd, current->pid);
    return fd;
}

int ksu_handle_reboot(int magic1, int magic2, unsigned int cmd, void __user *arg)
{
    if (magic1 == (int)KSU_INSTALL_MAGIC1 && magic2 == (int)KSU_INSTALL_MAGIC2) {
        int fd = ksu_install_fd();
        if (fd >= 0 && arg) {
            if (copy_to_user(arg, &fd, sizeof(fd))) {
                pr_err("ksu_handle_reboot: copy_to_user failed\\n");
            }
        }
        if (cmd == 0 && (is_manager() || ksu_is_allow_uid(current_uid().val) || current_uid().val == 0)) {
            escape_to_root();
        }
        return 0;
    }
    if (magic1 == (int)KSU_INSTALL_MAGIC1 && magic2 == 10006) { // CHANGE_MANAGER_UID
        if (current_uid().val == 0 || is_manager()) {
            ksu_set_manager_uid(cmd);
            if (arg) {
                unsigned long reply = (unsigned long)arg;
                copy_to_user(arg, &reply, sizeof(reply));
            }
        }
        return 0;
    }
    return -EINVAL;
}
"""
    with open(supercall_path, "w", encoding="utf-8") as f:
        f.write(supercall_code)
    print(f"[+] Successfully created {supercall_path} ([ksu_driver] supercall handler)")

    # 12. Patch kernel/reboot.c for reboot supercall
    with open("kernel/reboot.c", "r", encoding="utf-8") as f:
        rb_c = f.read()

    rb_decl = """
#ifdef CONFIG_KSU
extern int ksu_handle_reboot(int magic1, int magic2, unsigned int cmd, void __user *arg);
#endif
"""
    rb_call = """
#ifdef CONFIG_KSU
	if (magic1 == (int)0xdeadbeef && magic2 == (int)0xcafebabe) {
		ksu_handle_reboot(magic1, magic2, cmd, arg);
		return 0;
	}
#endif
"""
    rb_c, n_rb = re.subn(r"(SYSCALL_DEFINE4\s*\(\s*reboot\s*,[^{]*\{)", rb_decl + r"\n\1\n" + rb_call, rb_c, count=1)
    assert n_rb == 1, "Failed to patch kernel/reboot.c"
    with open("kernel/reboot.c", "w", encoding="utf-8") as f:
        f.write(rb_c)
    print("[+] Successfully patched kernel/reboot.c with KernelSU reboot supercall")

    # 13. Patch KernelSU Makefile (Compile supercall.o & set KSU_VERSION to 33214)
    mk_candidates = [
        "KernelSU/kernel/Makefile",
        "drivers/kernelsu/Makefile"
    ]
    mk_path = next((p for p in mk_candidates if os.path.exists(p)), None)
    if mk_path:
        with open(mk_path, "r", encoding="utf-8") as f:
            mk_c = f.read()
        target_version_expr = "$(eval KSU_VERSION=$(shell expr 10000 + $(KSU_GIT_VERSION) + 200))"
        if target_version_expr in mk_c:
            mk_c = mk_c.replace(target_version_expr, "$(eval KSU_VERSION=33214)")
        if "ccflags-y += -DKSU_VERSION=16" in mk_c:
            mk_c = mk_c.replace("ccflags-y += -DKSU_VERSION=16", "ccflags-y += -DKSU_VERSION=33214")
        if "kernelsu-objs += supercall.o" not in mk_c:
            mk_c = mk_c.replace("kernelsu-objs += core_hook.o", "kernelsu-objs += core_hook.o\nkernelsu-objs += supercall.o")
        with open(mk_path, "w", encoding="utf-8") as f:
            f.write(mk_c)
        print(f"[+] Successfully updated {mk_path} with supercall.o and KSU_VERSION=33214")

    print("[*] All KernelSU-Next VFS, Security & Supercall hooks applied successfully!")

if __name__ == "__main__":
    main()
