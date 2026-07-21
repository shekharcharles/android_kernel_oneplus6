/* Backport shim: linux/set_memory.h split out in kernel 4.12.
 * On arm64 4.9 the set_memory_* helpers live in <asm/cacheflush.h>.
 * Redirect so SukiSU-Ultra KPM (drivers/kernelsu/kpm/*) builds. */
#ifndef _LINUX_SET_MEMORY_H
#define _LINUX_SET_MEMORY_H
#include <asm/cacheflush.h>
#endif /* _LINUX_SET_MEMORY_H */
