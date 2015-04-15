#!/usr/bin/env python
"""
cmongo2sql
Utility to convert a MongoDB JSON dump to a SQL dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Use -h switch for usage information.
"""
import sys
import os
import re
import json
import argparse

signature = 'cmongo2sql 1.0 (https://github.com/stpettersens/cmongo2sql)'

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def cmongo2sql(file, out, db, verbose, version, info):

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

	head, tail = os.path.split(file)
	table = re.sub('.json', '', tail)

	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	dtable = 'DROP TABLE IF EXISTS `{0}`;'.format(table)
	ctable = 'CREATE TABLE IF NOT EXISTS `{0}` (\n'.format(table)
	insert = 'INSERT INTO `{0}` VALUES (\n'.format(table)
	inserts = []
	headers = True
	id = False
	for line in lines:
		ii = ''
		inputJson = json.loads(line)
		for key, value in inputJson.iteritems():

			fvalue = re.sub('\{|\}|\'', '', str(value))

			pattern = re.compile('u\$oid')
			if pattern.match(str(fvalue)):
				if headers: ctable += '{0} VARCHAR(30) NOT NULL,\n'.format(key)
				v = re.split(':', str(fvalue), 1)
				v = re.sub('\u', '', v[1], 1)
				v = re.sub('\s', '', v, 1)
				ii += '\'{0}\',\n'.format(v)
				id = True

			pattern = re.compile('u\$date')
			if pattern.match(str(fvalue)):
				if headers: ctable += '{0} TIMESTAMP NOT NULL,\n'.format(key)
				v = re.split(':', str(fvalue), 1)
				v = re.split('\s', v[1], 1)
				v = ''.join(v)
				v = re.sub('\T', ' ', v)
				v = re.sub('\u', '', v)
				v = re.sub('\.\d{3}Z', '', v)
				v = re.sub('\.\d{3}\+\d{4}', '', v)
				ii += '\'{0}\',\n'.format(v)
				id = False

			elif(type(value).__name__ == 'unicode' or type(value).__name__ == 'dict'):
				if headers and id == False:
					length = 50
					if key == 'description': length = 100
					ctable += '{0} VARCHAR({1}) NOT NULL,\n'.format(key, length)
				if fvalue.startswith('u$oid') == False and fvalue.startswith('u$date') == False: 
					ii += '\'{0}\',\n'.format(fvalue)
				id = False

			elif type(value).__name__ == 'int' or type(value).__name__ == 'float':
				if headers: ctable += '{0} NUMERIC(15, 2) NOT NULL,\n'.format(key)
				ii += '{0},\n'.format(fvalue)
				id = False

		headers = False
		ii = ii[:-2]
		inserts.append(insert + ii + ');\n')
		ii = ''

	ctable = ctable[:-2]
	ctable += ')\nENGINE=InnoDB DEFAULT CHARSET=utf8;'

	if verbose: 
		print('\nGenerating SQL dump file: \'{0}\' from\nMongoDB JSON dump file: \'{1}\'\n'
		.format(out, file))

	f = open(out, 'w')
	f.write('-- SQL table dump from MongoDB collection: {0} ({1} -> {2})\n'
	.format(re.sub('.json', '', file), file, out))
	f.write('-- Generated by: {0}\n'.format(signature))
	if db != None: f.write('USE {0};\n'.format(db));
	f.write('{0}\n'.format(dtable))
	f.write('{0}\n\n'.format(ctable))

	for insert in inserts:
		f.write('{0}\n'.format(insert))

	f.close()

				
# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to convert a MongoDB JSON dump to a SQL dump.')
parser.add_argument('-f', '--file', action='store', dest='file', metavar="FILE")
parser.add_argument('-o', '--out', action='store', dest='out', metavar="OUT")
parser.add_argument('-d', '--db', action='store', dest='db', metavar="DB")
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

cmongo2sql(argv.file, argv.out, argv.db, argv.verbose, argv.version, argv.info)