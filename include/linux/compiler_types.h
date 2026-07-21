/* Backport shim: compiler_types.h was split out in kernel 4.15.
 * On 4.9 the macros KSU-Next needs live in <linux/compiler.h>.
 * Redirect so drivers/kernelsu/*.c that #include <linux/compiler_types.h> build. */
#ifndef __LINUX_COMPILER_TYPES_H
#define __LINUX_COMPILER_TYPES_H
#include <linux/compiler.h>
#endif /* __LINUX_COMPILER_TYPES_H */
