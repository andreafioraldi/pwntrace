# pwntrace
Use ltrace with pwnlib.tubes.process instances, useful for heap exploitation

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
[*] Process '/bin/cat' stopped with exit code 0 (pid 8736)
 <trace> ls->fflush(0x7efc8f6a0620) = 0
 <trace> ls->fclose(0x7efc8f6a0620) = 0
 <trace> ls->fflush(0x7efc8f6a0540) = 0
 <trace> ls->fclose(0x7efc8f6a0540) = 0
[{'ret': '0', 'fn': 'ls->fflush(0x7efc8f6a0620)'}, {'ret': '0', 'fn': 'ls->fclose(0x7efc8f6a0620)'}, {'ret': '0', 'fn': 'ls->fflush(0x7efc8f6a0540)'}, {'ret': '0', 'fn': 'ls->fclose(0x7efc8f6a0540)'}]
```

