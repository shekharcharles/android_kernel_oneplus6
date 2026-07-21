# 4.9 compat patch for KernelSU-Next v3.0.1 driver (applied post-setup.sh, pre-build)
import os
d = "drivers/kernelsu"
aw = os.path.join(d, "allowlist.c")
s = open(aw, encoding="utf-8", errors="replace").read()
s = s.replace("TWA_RESUME", "true")                       # 4.9 task_work notify=true
s = s.replace("kernel_write(", "ksu49_kw(").replace("kernel_read(", "ksu49_kr(")  # rewrite CALLS first
lines = s.splitlines(keepends=True)
last_inc = 0
for i, l in enumerate(lines[:120]):
    if l.lstrip().startswith("#include"):
        last_inc = i
wrap = ("\n/* 4.9 compat: kernel_write pos-by-value; kernel_read(file,offset,buf,count) */\n"
        "static inline ssize_t ksu49_kw(struct file *f,const void *b,size_t c,loff_t *o){ssize_t n=kernel_write(f,(const char*)b,c,*o);if(n>0)*o+=n;return n;}\n"
        "static inline ssize_t ksu49_kr(struct file *f,void *b,size_t c,loff_t *o){int n=kernel_read(f,*o,(char*)b,c);if(n>0)*o+=n;return n;}\n")
lines.insert(last_inc + 1, wrap)                          # wrappers use REAL kernel_write/read (added AFTER call-rewrite)
open(aw, "w", encoding="utf-8").write("".join(lines))
kd = os.path.join(d, "ksud.c")
open(kd, "w", encoding="utf-8").write(open(kd, encoding="utf-8", errors="replace").read().replace("TWA_RESUME", "true"))
print("[ksu49patch] applied: TWA_RESUME->true, kernel_write/read 4.9 wrappers")
