""" Parsing tag from

	parse.py [-h] [-se][tag_wrapper] content

	-s, --start
		set start wrapper, '{{' is default

	-e, --end
		set end wrapper, '}}' is default

	-h, --help
		show usage

"""


def parse(content, tag_start="{{", tag_end="}}"):
	""" A parser, parsing tag btw `tag_start` & `tag_end` in `content`
	"""
	c = content
	while True:
		if tag_start in c:
			c = c[c.index(tag_start) + len(tag_start):]
			if tag_end not in c:
				continue
			yield c[:c.index(tag_end)]
			c = c[c.index(tag_end):]
		else:
			return

if __name__ == '__main__':
	import os
	import sys
	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:], "he:s:", ["help", "end", "start"])
	except getopt.GetoptError as e:
		pass
	print('using in command line still not implement.')
	#     print(e)
	#     print(__doc__)
	#     sys.exit(-1)
	#
	# for o, a in opts:
	#     if o in ('-h', '--help'):
	#         print(__doc__)
	#         sys.exit(0)
	#     elif o in ('-a', '--all'):
	#         IGNORE_HIDDEN = False
	#     elif o in ('-d', '--dry'):
	#         VERBOSE = True
	#         DRYRUN = True
	#     elif o in ('-v', '--verbose'):
	#         VERBOSE = True
	#     elif o in ('-o', '--optimize'):
	#         OPTIMIZE_LEVEL = int(a)
	#     elif o in ('-s', '--source'):
	#         SOURCE = a
	#     elif o in ('-t', '--target'):
	#         TARGET = a
	#     elif o in ('-r', '--remove'):
	#         REMOVE_MODE = True
	#         pattern = re.compile("^" + os.path.abspath(SOURCE))
	#         if pattern.match(os.path.abspath(TARGET)):
	#             print('Target cant not under the source in remove mode')
	#             sys.exit(-1)
	#     else:
	#         print("Unkown options: " + o)
	#         print(__doc__)
	#         sys.exit(-1)
	# main()
