from pwn import *
import random
import string
import atexit
import sys
import os

def print_heap_trace(trace):
	if trace == None:
		print '\033[0;96m' + " <trace> NO TRACE" + '\033[0m'
	else:
		for e in trace:
			if e["fn"] == "malloc":
				print '\033[0;32m' + " <trace> malloc(" + str(e["arg"]) + ") = " + hex(e["ret"]) + '\033[0m'
			elif e["fn"] == "free":
				print '\033[0;31m' + " <trace> free(" + hex(e["arg"]) + ") = <void>" + '\033[0m'

def heap_ltrace(argv, env=None, shell=False, **kwargs):
	rand_str = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
	fifo_name = "/tmp/ltrace-fifo-" + rand_str
	os.mkfifo(fifo_name)
	
	ll = context.log_level
	context.log_level = "warning"
	t = process(["cat", fifo_name])
	context.log_level = ll
	
	if shell:
		p = process("ltrace -e 'malloc+free' -o '" + fifo_name + "' " + argv, env=env, shell=shell, **kwargs)
	else:
		if type(argv) == str:
			argv = [argv]
		p = process(["ltrace", "-e", "malloc+free", "-o", fifo_name] + argv, env=env, shell=shell, **kwargs)

	def get_trace():
		ll = context.log_level
		context.log_level = "warning"
		try:
			r = p.tracer_output.recv()
		except EOFError:
			context.log_level = ll
			return None
		context.log_level = ll
		
		lines = r.split("\n")
		trace = []
		for line in lines:
			if "=" not in line:
				continue
			fn, ret = line.split("=")
			fn = fn.strip()
			ret = ret.strip()
			arg = fn[fn.rfind("(") +1: fn.rfind(")")]
		
			if "malloc" in fn:
				fn = "malloc"
				try: ret_val = int(ret, 16)
				except: ret_val = int(ret, 10)
				try: arg_val = int(arg)
				except: arg_val = int(arg, 16)
			
				if ret_val in p.freed:
					p.freed.remove(ret_val)
			
				p.allocd.append({"addr": ret_val, "size": arg_val})
			elif "free" in fn:
				fn = "free"
				ret_val = None
				try: arg_val = int(arg)
				except: arg_val = int(arg, 16)
			
				for d in p.allocd:
					if d["addr"] == arg_val:
						p.allocd.remove(d)
						break
				p.freed.append(arg_val)
		
			trace += [{"fn":fn, "arg":arg_val, "ret":ret_val}]
		return trace
	
	def trace_now():
		trace = p.get_trace()
		print_heap_trace(trace)
		return trace
	
	def print_allocd():
		print '\033[0;96m' + " >>> ALLOCD <<<"
		for d in p.allocd:
			print " addr: 0x%x\tsize:%d" % (d["addr"], d["size"])
		print '\033[0m'

	def print_freed():
		print '\033[0;96m' + " >>> FREED <<<"
		for a in p.freed:
			print " addr: 0x%x" % a
		print '\033[0m'

	
	setattr(p, "tracer_output", t)
	setattr(p, "get_trace", get_trace)
	setattr(p, "trace_now", trace_now)
	setattr(p, "allocd", [])
	setattr(p, "freed", [])
	setattr(p, "print_allocd", print_allocd)
	setattr(p, "print_freed", print_freed)
	return p


