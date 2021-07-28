import numpy as np
import math


def pi_digits(x=1000):
	"""Generate x digits of Pi.

	Shamelessly usurped from StackOverflow
	https://stackoverflow.com/a/54967370/11895567

	:param x: Number of digits of pi. Default is 1,000
	:type x: int
	"""
	k, a, b, a1, b1 = 2, 4, 1, 12, 4
	while x > 0:
		p, q, k = k * k, 2 * k + 1, k + 1
		a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
		d, d1 = a / b, a1 / b1
		while d == d1 and x > 0:
			yield int(d)
			x -= 1
			a, a1 = 10 * (a % b), 10 * (a1 % b1)
			d, d1 = a / b, a1 / b1


def print_digits(col_width=12, x_digits=1000, fn=None, chunk_size=None, cp=None,
                 **kwargs):
	"""Print out the digits of pi

	This one I wrote.

	:param col_width: Number of digits/characters
		in a column. Default is 12. Must be a number
		greater than or equal to 2.
	:type col_width: int
	:param x_digits: The number of digits of pi to
		calculate. Default is 1000.
	:type x_digits: int
	:param fn: The name of the output file.
		Default is None.
	:type fn: str, PathLike, None
	:param chunk_size: Number of lines to write at a time. Default is 100.
	:type chunk_size: int, None
	:param cp: Check point. If not none, stop the program and wait for user
		input when the program is ready to begin writing to file.
	:type cp: None, int, str, float, bool
	"""

	if 'nmax' in kwargs.keys():
		nmax = kwargs['nmax']
	else:
		nmax = 1100000

	if 'block_size' in kwargs.keys():
		block_size = kwargs['block_size']
	else:
		block_size = 10

	print("\tRunning...")
	print(f'\tCalculating {x_digits} digits of pi...')

	assert(col_width >= 2), 'col_width must be an integer greater than ' \
	                        'or equal to 2'

	if x_digits > nmax:
		# don't let user print more than nmax digits
		raise RuntimeError(f"\n\n\n{x_digits} digits... No. "
		                   f"No you're not doing that...")

	if chunk_size is None:
		chunk_size = 100
	elif np.mod(chunk_size, block_size) != 0:
		print(f'chunk_size must be a positive multiple of {block_size}')
		chunk_size = int(math.ceil(abs(chunk_size) / block_size)) * block_size
	else:
		pass

	while np.mod(x_digits, col_width) != 0:
		# Ensure the array will be rectangular and contain
		# at least the number of digits specified
		x_digits += 1
	x_digits -= 1  # compensate for decimal place

	digits = [int(n) for n in list(pi_digits(x=x_digits))]
	left_side = np.array([3, np.nan])
	right_side = np.array([int(x) for x in digits[1:]])

	# combine left_side and right_side
	all_pi = np.append(left_side, right_side)
	number_elements = all_pi.shape
	number_rows = np.floor_divide(number_elements, col_width)
	all_pi = all_pi.reshape((number_rows[0], col_width))

	# add the first line "3.1415926535..." to list
	lines = [
		str(int(all_pi[0][0])) + "." + "".join(
			str(int(_)) for _ in all_pi[0][2:]
		)]

	for row in range(1, int(number_rows)):
		# Add the remaining lines to list
		lines.append("".join(str(int(_)) for _ in all_pi[row]))

	print(f'\tReady to write to file...')

	if cp is not (None or False):
		# if anything is passed to the checkpoint variable (``cp``)
		# wait for user to press ENTER before writing to the output file.
		input('Press ENTER to continue. ')

	if fn is None:
		# set default output filename
		fn = "pi_printer_" + str(col_width) + \
		     "x" + str(number_elements[0]) + ".txt"

	num_iters, num_lines = _writer_thing(
		list_lines=lines,
		filename=fn,
		chunk_size=chunk_size,
		**kwargs)

	print(f'Iterations: {num_iters+1}')
	print(f'Number lines: {num_lines+1}')
	return num_iters, num_lines


def _writer_thing(list_lines, filename, chunk_size, iteration=0, lines_printed=0,
                  **kwargs):
	"""Write the digits of pi to an output file

	:param list_lines: A list of the lines to write. The lines are the digits of
		pi broken up into n-character long lines, where n is a parameter passed
		to print_digits(...) as `col_width`; default is 12 characters long.
	:type list_lines: list, tuple
	:param filename: the name of the output file to write the lines to.
	:type filename: str, PathLike
	:param chunk_size: The number of lines to write at a time.
	:type chunk_size: int
	:param iteration: An integer that keeps track of the recursion of this
		function. Default is 0.
	:type iteration: int
	"""
	if 'block_size' in kwargs.keys():
		block_size = kwargs['block_size']
	else:
		block_size = 10

	if len(list_lines) >= chunk_size:
		_chunk_size = chunk_size
	else:
		_chunk_size = len(list_lines)

	pi_out = open(file=filename, mode='a')
	for i, _ in enumerate(list_lines[:_chunk_size]):
		pi_out.write(list_lines.pop(0))
		pi_out.write("\n")
		if np.mod(i+1, block_size) == 0 and len(list_lines)+1 > block_size:
			lines_printed += 1
			pi_out.write("\n")
		lines_printed += 1
	pi_out.close()
	print(f'Wrote {_chunk_size} lines to file. Saving file...')

	if len(list_lines) > 0:
		# recursion case
		iteration, lines_printed = _writer_thing(
			list_lines=list_lines,
			filename=filename,
			chunk_size=chunk_size,
			iteration=iteration+1,
			lines_printed=lines_printed,
			**kwargs)
	return iteration, lines_printed


def main(**kwargs):
	"""Wrapper for print_digits(...)

	:param kwargs: Key-word arguments.

		* col_width = width of columns printed or the number of elements printed per line
		* chunk_size = number of lines to print before saving the file
		* fn = output filename
		* cp = check point, pause program execution and wait for user input before continuing.
		* x_digits = number of digits of pi to print
		* nmax = max number of digits to calculate. Default is 1.1 million
		* block_size = add a blank line every block_size+1 line
	"""
	print_digits(**kwargs)
	return True


if __name__ == "__main__":
	# 1,000,000 digits = 44268.841465473175 seconds (old code)
	my_kwargs = {
		'col_width': 12,
		'chunk_size': 1500,
		'fn': None,
		'cp': False,
		'x_digits': 1000000,
	}
	main(**my_kwargs)
