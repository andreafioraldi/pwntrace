from pwn import *
import random
import string
import atexit
import sys
import os

def print_trace(trace):
	if trace == None:
		print '\033[0;96m' + " <trace> NO TRACE" + '\033[0m'
	else:
		for e in trace:
			print '\033[0;96m' + " <trace> " + e["fn"] + " = " + e["ret"] + '\033[0m'

def ltrace(argv, functions, env=None, shell=False, **kwargs):
	assert type(functions) == list
	func_list = ""
	for f in functions:
		func_list += f + "+"
	func_list = func_list[:-1]

	rand_str = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
	fifo_name = "/tmp/ltrace-fifo-" + rand_str
	os.mkfifo(fifo_name)
	
	ll = context.log_level
	context.log_level = "warning"
	t = process(["cat", fifo_name])
	context.log_level = ll
	
	if shell:
		p = process("ltrace -e '" + func_list + "' -o '" + fifo_name + "' " + argv, env=env, shell=shell, **kwargs)
	else:
		if type(argv) == str:
			argv = [argv]
		p = process(["ltrace", "-e", func_list, "-o", fifo_name] + argv, env=env, shell=shell, **kwargs)
	
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
		ret = []
		for l in lines:
			if "=" not in l:
				continue
			s = l.split("=")
			ret += [{"fn":s[0].strip(), "ret":s[1].strip()}]
		return ret
	
	def trace_now():
		trace = p.get_trace()
		print_trace(trace)
		return trace
	
	setattr(p, "tracer_output", t)
	setattr(p, "get_trace", get_trace)
	setattr(p, "trace_now", trace_now)
	return p


