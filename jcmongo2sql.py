#!/usr/bin/env jython
# Wrapper for cmongo2sql in Jython
import sys
from os import path
from subprocess import Popen, call, PIPE, STDOUT

jyson = 'jyson.jar'
if path.isfile(jyson) == False:
	print('Dependency \'%s\' is missing.\nPlease download it from:' % jyson)
	print('http://opensource.xhaus.com/projects/jyson') 
	sys.exit(1)

cmd = ['jython', '-Dpython.path=jyson.jar', 'cmongo2sql.jy.py']

try:
	p = Popen('uname', stdout=PIPE, stderr=STDOUT)
	uname = p.stdout.read()
except:
	uname = 'MINGW32'

if uname.startswith('MINGW32'): cmd[0] = 'jython.bat'
for arg in sys.argv: cmd.append(arg)
del cmd[3] 
call(cmd)
