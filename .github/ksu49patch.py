# 4.9 compat patch for KernelSU-Next v3.0.1 driver (post-setup.sh, pre-build)
import os
d = "drivers/kernelsu"

# --- allowlist.c: kernel_write/read 4.9 signatures + TWA_RESUME ---
aw = os.path.join(d, "allowlist.c")
s = open(aw, encoding="utf-8", errors="replace").read()
s = s.replace("TWA_RESUME", "true")
s = s.replace("kernel_write(", "ksu49_kw(").replace("kernel_read(", "ksu49_kr(")
lines = s.splitlines(keepends=True)
last_inc = 0
for i, l in enumerate(lines[:120]):
    if l.lstrip().startswith("#include"):
        last_inc = i
wrap = ("\n/* 4.9 compat: kernel_write pos-by-value; kernel_read(file,offset,buf,count) */\n"
        "static inline ssize_t ksu49_kw(struct file *f,const void *b,size_t c,loff_t *o){ssize_t n=kernel_write(f,(const char*)b,c,*o);if(n>0)*o+=n;return n;}\n"
        "static inline ssize_t ksu49_kr(struct file *f,void *b,size_t c,loff_t *o){int n=kernel_read(f,*o,(char*)b,c);if(n>0)*o+=n;return n;}\n")
lines.insert(last_inc + 1, wrap)
open(aw, "w", encoding="utf-8").write("".join(lines))

# --- ksud.c: TWA_RESUME ---
kd = os.path.join(d, "ksud.c")
open(kd, "w", encoding="utf-8").write(open(kd, encoding="utf-8", errors="replace").read().replace("TWA_RESUME", "true"))

# --- app_profile.c: seccomp.filter_count + seccomp_filter_release are 5.9+ ---
ap = os.path.join(d, "app_profile.c")
s = open(ap, encoding="utf-8", errors="replace").read()
s = s.replace("atomic_set(&current->seccomp.filter_count, 0);",
              "#if LINUX_VERSION_CODE >= KERNEL_VERSION(5,9,0)\n\tatomic_set(&current->seccomp.filter_count, 0);\n#endif")
s = s.replace("seccomp_filter_release(fake);",
              "#if LINUX_VERSION_CODE >= KERNEL_VERSION(5,9,0)\n\tseccomp_filter_release(fake);\n#endif")
open(ap, "w", encoding="utf-8").write(s)

print("[ksu49patch] applied: allowlist(kw/kr,TWA), ksud(TWA), app_profile(seccomp 5.9 guards)")
