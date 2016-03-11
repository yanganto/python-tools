"""
	Generate binary files for a softeare of python
	
	colony.py [-advrh] [-o optimize level] [-s source directory] [-t target directory]

	-a, --all
		including the hinded files
	
	-d, --dry
		dry run

	-s, --source
		specific the source directory, or use current directory

	-t, --target
		specific the target directory, or use ./output/
	/home/yanganto/Trend/EasyPhishing
	-v, --verbose
		verbose mode

	-r, --remove
		remove the py file from the source, while the pyc or pyo was generateed
	
	-o, --optimize
		optimize compile
		default value of -1 selects the optimization level of the interpreter as given by -O options. 
		Explicit levels are 0 (no optimization; __debug__ is true),
		1 (asserts are removed, __debug__ is false) or 2 (docstrings are removed too).

	-h, --help
		show ussage
"""
import os
import sys
import getopt
import py_compile
import re
import shutil

VERBOSE = False
REMOVE_MODE = False
IGNORE_HIDDEN = True
DRYRUN = False
SOURCE = "./"
TARGET = "./output/"
OPTIMIZE_LEVEL = -1


def main():
	try:
		for dir_path, dir_names, files in os.walk(SOURCE):
			for fullname in files:
				if IGNORE_HIDDEN and  is_hindden(dir_path) or fullname[0] == '.':
					if VERBOSE:
						print('Ignore: ' + os.path.join(dir_path, fullname))
					continue
				file_name, extension = os.path.splitext(fullname)
				source_file = os.path.join(dir_path, fullname)
				if extension == '.py': 
					target_file = re.sub( r'^' + SOURCE + r'(.+)' + r'.py$', TARGET + r'\1'+ '.pyc' , source_file)
					if VERBOSE:
						print('Compile: ' + source_file + ' -> ' + target_file)
					if not DRYRUN:
						py_compile.compile(source_file, target_file, doraise=True, optimize=OPTIMIZE_LEVEL)
				elif extension in ('.pyc', '.pyo'):
					if VERBOSE:
						print('Ignore: ' + os.path.join(dir_path, fullname))
				else:
					target_file = re.sub( r'^' + SOURCE, TARGET, source_file)
					if VERBOSE:
						print('Copy: ' + source_file + ' -> ' + target_file)
					if not DRYRUN:
						shutil.copyfile(source_file, target_file)
			for dir_name in dir_names:
				source_dir = os.path.join(dir_path, dir_name)
				target_dir = re.sub( r'^' + SOURCE, TARGET, source_dir)
				if VERBOSE:
					print('Create: ' + target_dir)
				if not DRYRUN:
					os.mkdir(target_dir)

		else:
			if REMOVE_MODE:
				if VERBOSE:
					print("Removing source")
				shutil.rmtree(SOURCE)
	except:
		print(sys.exc_info())
		print("Roll Back")
		shutil.rmtree(TARGET)


def is_hindden(path): 
	"""
		detect the path has any hindden folder
	"""
	while True:
		heads, tail = os.path.split(path)
		if heads == path: # The root 
			return False
		if tail == path: # the '.'
			return False
		elif tail and  tail[0] == '.':  # hidden folder detected
			return True
		else: # recursive
			path = heads

if __name__ == '__main__':
	assert is_hindden('/sdf/sdf/sdf.xx') == False, "absolute normal path fail"
	assert is_hindden('/sdf/.sdf/sfd.xx') == True, "absolute hiddend path fail"
	assert is_hindden('./sdf/sdf/sfd.xx') == False, "relative normal `path fail"
	assert is_hindden('./sdf/.sdf/sfd.xx') == True, "relative hiddend path fail"
	assert is_hindden('./') == False, "relative current folder fail"
	assert is_hindden('.') == False, "relative current path fail"
	assert is_hindden('/') == False, "root path fail"
	try:
		opts, args = getopt.getopt(sys.argv[1:], "advrho:s:t:", ["all", "dry", "verbose", "remove", 'help', 'optimize',
																 "source", "target"])
	except getopt.GetoptError as e:
		print(e)
		print(__doc__)
		sys.exit(-1)

	for o, a in opts:
		if o in ('-h', '--help'):
			print(__doc__)
			sys.exit(0)
		elif o in ('-a', '--all'):
			IGNORE_HIDDEN = False
		elif o in ('-d', '--dry'):
			VERBOSE = True
			DRYRUN = True
		elif o in ('-v', '--verbose'):
			VERBOSE = True
		elif o in ('-o', '--optimize'):
			OPTIMIZE_LEVEL = int(a)
		elif o in ('-s', '--source'):
			SOURCE = a
		elif o in ('-t', '--target'):
			TARGET = a
		elif o in ('-r', '--remove'):
			REMOVE_MODE = True
			pattern = re.compile("^" + os.path.abspath(SOURCE))
			if pattern.match(os.path.abspath(TARGET)):
				print('Target cant not under the source in remove mode')
				sys.exit(-1)
		else:
			print("Unkown options: " + o)
			print(__doc__)
			sys.exit(-1)
	main()
