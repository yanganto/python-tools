#!/usr/bin/env python
""" TF(1)

NAME
	tf - tag finder

SYNOPSIS
	tf [OPTION]... [FILES]...

DESCRIPTION
	Finding tags wrapper by start wrapper and end wrapper

	-s, --start
		set start wrapper, '{{' is default

	-e, --end
		set end wrapper, '}}' is default

	-h, --help
		show usage

	-v, --version

EXAMPLES


COPYRIGHT
	BSD Licence

SOURCE
	https://github.com/yanganto/python-tools/blob/master/tag_finder.py
"""


def parser(content, tag_start="{{", tag_end="}}"):
	""" A parser, parsing tag btw `tag_start` & `tag_end` in `content`
	"""
	c = content
	while True:
		if tag_start in c:
			c = c[c.index(tag_start) + len(tag_start):]
			if tag_end not in c:
				continue
			yield c[:c.index(tag_end)].strip()
			c = c[c.index(tag_end):]
		else:
			return

if __name__ == '__main__':
	import os
	import sys
	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:], "he:s:v", ["help", "end", "start", "version"])
	except getopt.GetoptError as e:
		print(__doc__)
		sys.exit("invalid option")

	tag_start = '{{'
	tag_end = '}}'

	for o, a in opts:
		if o in ('-h', '--help'):
			print(__doc__)
			sys.exit(0)
		elif o in ('-v', '--version'):
			print(0.1)
			sys.exit(0)
		elif o in ('-s', '--start'):
			tag_start = a
		elif o in ('-e', '--end'):
			tag_end = a

	tags = dict()
	if args:
		for arg in args:
			if not os.path.isfile(arg):
				sys.exit("missing file: " + arg)
			with open(arg, 'r') as f:
				for line in f:
					p = parser(line, tag_start, tag_end)
					while True:
						try:
							tag = next(p)
							tags[tag] = tags.get(tag, 0) +1
						except StopIteration:
							break
	else:
		# TODO: work with pipe here
		sys.exit("missing argument")

	for k, v in tags.items():
		print(k, v, sep='\t')
