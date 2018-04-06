# pwntrace
Use ltrace with pwnlib.tubes.process instances, useful for heap exploitation

## Install

pwntrace is on PyPI:

```
$ pip install pwntrace
```

I suggest you to use a vitualenv to work with pwntools.

## Api

ltrace:
+ `p = ltrace(argv, functions, ...)` create a modified instace of pwnlib.tubes.process for ltrace
+ `p.get_trace()` get trace output
+ `print_trace(trace)` pretty print p.get_trace or p.trace_now return value
+ `p.trace_now()` get_trace + print_trace

heap_ltrace:
+ `p = heap_ltrace(argv, ...)` create a modified instace of pwnlib.tubes.process for ltrace malloc and free
+ `p.get_trace()` get trace output
+ `print_heap_trace(heap_trace)`
+ `p.trace_now()`  get_trace + print_trace
+ `p.allocd` list of `{"addr": ret_val, "size": arg_val}` objects representing the memory allocated from the last get_trace|trace_now call
+ `p.freed` list of addresses (int) representing the memory freed from the last get_trace|trace_now call
+ `p.print_allocd()` pretty print allocd
+ `p.print_freed()` pretty print freed

## Examples

```python
>>> from pwntrace import *
>>> p = ltrace("/bin/ls", ["fflush", "fclose"])
[x] Starting local process '/usr/bin/ltrace'
[+] Starting local process '/usr/bin/ltrace': pid 8737
>>> p.recv()
[*] Process '/usr/bin/ltrace' stopped with exit code 0 (pid 8737)
'LICENSE  pwntrace  README.md\n'
>>> p.trace_now()
 <trace> ls->fflush(0x7efc8f6a0620) = 0
 <trace> ls->fclose(0x7efc8f6a0620) = 0
 <trace> ls->fflush(0x7efc8f6a0540) = 0
 <trace> ls->fclose(0x7efc8f6a0540) = 0
[{'ret': '0', 'fn': 'ls->fflush(0x7efc8f6a0620)'}, {'ret': '0', 'fn': 'ls->fclose(0x7efc8f6a0620)'}, {'ret': '0', 'fn': 'ls->fflush(0x7efc8f6a0540)'}, {'ret': '0', 'fn': 'ls->fclose(0x7efc8f6a0540)'}]
```

```python
>>> p = heap_ltrace(["/bin/ip", "address"])
[x] Starting local process '/usr/bin/ltrace'
[+] Starting local process '/usr/bin/ltrace': pid 9694
>>> p.trace_now()
 <trace> malloc(1276) = 0x12ec010
 <trace> malloc(64) = 0x12ec520
 <trace> malloc(1292) = 0x12ec570
 <trace> malloc(64) = 0x12eca90
 <trace> malloc(1284) = 0x12ecae0
 <trace> malloc(64) = 0x12ecff0
 <trace> malloc(1688) = 0x12ed040
 <trace> malloc(64) = 0x12ed6e0
 <trace> malloc(1696) = 0x12ed730
 <trace> malloc(64) = 0x12edde0
 <trace> malloc(1576) = 0x12ede30
 <trace> malloc(64) = 0x12ee460
 <trace> malloc(84) = 0x12ee4b0
 <trace> malloc(96) = 0x12ee510
 <trace> malloc(88) = 0x12ee580
 <trace> malloc(96) = 0x12ee5e0
 <trace> malloc(80) = 0x12ee650
 <trace> malloc(80) = 0x12ee6b0
 <trace> malloc(80) = 0x12ee710
 <trace> malloc(80) = 0x12ee770
 <trace> malloc(24) = 0x12efe20
 <trace> free(0x12ee4b0) = <void>
 <trace> free(0x12ee510) = <void>
 <trace> free(0x12ee580) = <void>
 <trace> free(0x12ee5e0) = <void>
 <trace> free(0x12ee650) = <void>
 <trace> free(0x12ee6b0) = <void>
 <trace> free(0x12ee710) = <void>
 <trace> free(0x12ee770) = <void>
 <trace> free(0x12ec010) = <void>
 <trace> free(0x12ec570) = <void>
 <trace> free(0x12ecae0) = <void>
 <trace> free(0x12ed040) = <void>
 <trace> free(0x12ed730) = <void>
 <trace> free(0x12ede30) = <void>
[{'ret': 19841040, 'fn': 'malloc', 'arg': 1276}, {'ret': 19842336, 'fn': 'malloc', 'arg': 64}, {'ret': 19842416, 'fn': 'malloc', 'arg': 1292}, {'ret': 19843728, 'fn': 'malloc', 'arg': 64}, {'ret': 19843808, 'fn': 'malloc', 'arg': 1284}, {'ret': 19845104, 'fn': 'malloc', 'arg': 64}, {'ret': 19845184, 'fn': 'malloc', 'arg': 1688}, {'ret': 19846880, 'fn': 'malloc', 'arg': 64}, {'ret': 19846960, 'fn': 'malloc', 'arg': 1696}, {'ret': 19848672, 'fn': 'malloc', 'arg': 64}, {'ret': 19848752, 'fn': 'malloc', 'arg': 1576}, {'ret': 19850336, 'fn': 'malloc', 'arg': 64}, {'ret': 19850416, 'fn': 'malloc', 'arg': 84}, {'ret': 19850512, 'fn': 'malloc', 'arg': 96}, {'ret': 19850624, 'fn': 'malloc', 'arg': 88}, {'ret': 19850720, 'fn': 'malloc', 'arg': 96}, {'ret': 19850832, 'fn': 'malloc', 'arg': 80}, {'ret': 19850928, 'fn': 'malloc', 'arg': 80}, {'ret': 19851024, 'fn': 'malloc', 'arg': 80}, {'ret': 19851120, 'fn': 'malloc', 'arg': 80}, {'ret': 19856928, 'fn': 'malloc', 'arg': 24}, {'ret': None, 'fn': 'free', 'arg': 19850416}, {'ret': None, 'fn': 'free', 'arg': 19850512}, {'ret': None, 'fn': 'free', 'arg': 19850624}, {'ret': None, 'fn': 'free', 'arg': 19850720}, {'ret': None, 'fn': 'free', 'arg': 19850832}, {'ret': None, 'fn': 'free', 'arg': 19850928}, {'ret': None, 'fn': 'free', 'arg': 19851024}, {'ret': None, 'fn': 'free', 'arg': 19851120}, {'ret': None, 'fn': 'free', 'arg': 19841040}, {'ret': None, 'fn': 'free', 'arg': 19842416}, {'ret': None, 'fn': 'free', 'arg': 19843808}, {'ret': None, 'fn': 'free', 'arg': 19845184}, {'ret': None, 'fn': 'free', 'arg': 19846960}, {'ret': None, 'fn': 'free', 'arg': 19848752}]
>>> p.print_allocd()
 >>> ALLOCD <<<
 addr: 0x12ec520	size:64
 addr: 0x12eca90	size:64
 addr: 0x12ecff0	size:64
 addr: 0x12ed6e0	size:64
 addr: 0x12edde0	size:64
 addr: 0x12ee460	size:64
 addr: 0x12efe20	size:24

```

### Dedication

In loving memory of malloc_hook
