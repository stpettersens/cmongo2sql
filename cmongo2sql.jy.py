#!/usr/bin/env jython
"""
cmongo2sql
Utility to convert a MongoDB JSON dump to a SQL dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Tweaked for Jython compatibility.
Uses Java implemented JSON module
and getopt instead of argparse.

"""
import sys
import os
import re
import com.xhaus.jyson.JysonCodec as json
import datetime
import getopt

signature = 'cmongo2sql 1.0.4 [Jython] (https://github.com/stpettersens/cmongo2sql)'

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def cmongo2sql(file, out, db, comments, verbose, version, info):

	if len(sys.argv) == 1:
		displayInfo()
		sys.exit(0)

	if file == None and out == None:
		if verbose ==  False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayInfo()

		sys.exit(0)

	if out == None: out = re.sub('.json', '.sql', file)

	if file.endswith('.json') == False:
		print('Input file is not a MongoDB dump.')
		sys.exit(1)

	if out.endswith('.sql') == False:
		print('Output file is not a SQL file.')
		sys.exit(1)

	if comments == None: comments = True

	head, tail = os.path.split(file)
	table = re.sub('.json', '', tail)

	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	dtable = 'DROP TABLE IF EXISTS `%s`;' % table
	ctable = 'CREATE TABLE IF NOT EXISTS `%s` (\n' % table
	insert = 'INSERT INTO `%s` VALUES (\n' % table
	inserts = []
	headers = True
	id = False
	for line in lines:
		ii = ''
		inputJson = json.loads(line)
		for key, value in inputJson.iteritems():

			fvalue = re.sub('\{|\}|\'', '', str(value))

			pattern = re.compile('\$oid')
			if pattern.match(str(fvalue)):
				if headers: ctable += '`%s` VARCHAR(24),\n' % key
				v = re.split(':', str(fvalue), 1)
				v = re.sub('\s', '', v[1], 1)
				v = re.sub('\u', '', v)
				ii += '\'%s\',\n' % v
				id = True

			pattern = re.compile('\$date')
			if pattern.match(str(fvalue)):
				if headers: ctable += '`%s` TIMESTAMP,\n' % key
				v = re.split(':', str(fvalue), 1)
				v = re.split('\s', v[1], 1)
				v = ''.join(v)
				v = re.sub('\T', ' ', v)
				v = re.sub('\u', '', v)
				v = re.sub('\.\d{3}Z', '', v)
				v = re.sub('\.\d{3}\+\d{4}', '', v)
				ii += '\'%s\',\n' % v
				id = False

			elif type(value).__name__ == 'unicode' or type(value).__name__ == 'dict':
				if headers and id == False:
					length = 50
					if key == 'description': length = 100
					ctable += '`%s` VARCHAR(%d),\n' % (key, length)
				if fvalue.startswith('$oid') == False and fvalue.startswith('$date') == False:
					ii += '\'%s\',\n' % fvalue
				id = False

			elif type(value).__name__ == 'int' or type(value).__name__ == 'float':
				if headers: ctable += '`%s` NUMERIC(15, 2),\n' % key
				ii += '%s,\n' % fvalue
				id = False

			elif type(value).__name__ == 'bool':
				if headers: ctable += '`%s` BOOLEAN,\n' % key
				ii += '%s,\n' % fvalue.upper()
				id = False

		headers = False
		ii = ii[:-2]
		inserts.append(insert + ii + ');\n\n')
		ii = ''

	ctable = ctable[:-2]
	ctable += ');'

	if verbose:
		print('\nGenerating SQL dump file: \'%s\' from\nMongoDB JSON dump file: \'%s\'\n' % (out, file))

	collection = re.sub('.json', '', file)

	f = open(out, 'w')
	f.write('--!\n')
	if comments:
		f.write('-- SQL table dump from MongoDB collection: %s (%s -> %s)\n' % (collection, file, out))
		f.write('-- Generated by: %s\n' % signature)
		f.write('-- Generated at: %s\n\n' % datetime.datetime.now())
	if db != None: f.write('USE %s;\n' % db);
	f.write('%s\n' % dtable)
	f.write('%s\n\n' % ctable)

	for insert in inserts:
		f.write(insert)

	f.close()


# Handle any command line arguments.
try:
	opts, args = getopt.getopt(sys.argv[1:], "f:o:d:nlvi")
except:
	print('Invalid option or argument.')
	displayInfo()
	sys.exit(2)

file = None
out = None
db = None
comments = None
verbose = False
version = False
info = False
for o, a in opts:
	if o == '-f':
		file = a
	elif o == '-o':
		out = a
	elif o == '-d':
		db = a
	elif o == '-n':
		comments = False
	elif o == '-l':
		verbose = True
	elif o == '-v':
		version = True
	elif o == '-i':
		info = True
	else:
		assert False, 'unhandled option'

cmongo2sql(file, out, db, comments, verbose, version, info)
