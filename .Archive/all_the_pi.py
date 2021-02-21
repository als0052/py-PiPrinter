#!/usr/bin/env python
# Filename: all_the_pi.py

"""
Format a string containing an arbitrary number of digits of Pi for output to
a text file.

Created by als0052
Created on Unknown
Updated on 02-16-2021
"""

from datetime import datetime as dt
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
		p, q, k = k*k, 2*k + 1, k + 1
		a, b, a1, b1 = a1, b1, p*a + q*a1, p*b + q*b1
		d, d1 = a/b, a1/b1
		while d == d1 and x > 0:
			yield int(d)
			x -= 1
			a, a1 = 10*(a % b), 10*(a1 % b1)
			d, d1 = a/b, a1/b1


def print_digits(col_width=12, x_digits=1000, fn=None, chunk_size=100,
                 cp=None):
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

	# Error Handling
	if col_width < 2:
		msg = 'col_width must be an integer greater than or equal to 2'
		raise ValueError(msg)

	if x_digits > 1100000:
		# Don't let user print more than 1,100,000 digits
		msg = f"Cannot operate with {x_digits} digits. That is too much."
		raise RuntimeError(msg)

	# Default output filename
	if fn is None:
		date = dt.now().strftime("%m-%d-%Y_%H%M%S")
		fn = f'pi_printer_{col_width}x{x_digits}_{date}.txt'

	if np.mod(chunk_size, 10) != 0:
		print('chunk_size must be a positive multiple of 10')
		chunk_size = int(math.ceil(abs(chunk_size) / 10.0)) * 10

	digits = [int(n) for n in list(pi_digits(x=x_digits))]
	left_side = np.array([3, np.nan])
	right_side = np.array([int(x) for x in digits[1:]])

	# combine left_side and right_side
	all_pi = np.append(left_side, right_side)
	number_elements = all_pi.shape
	number_rows = np.floor_divide(number_elements, col_width)

	if np.mod(number_elements, col_width) != 0:
		# Add zeros to the end of the array to make it evenly divisible by
		# elements_per_line
		missing_elements = np.mod(number_elements, col_width)
		missing_elements = col_width - missing_elements
		all_pi = np.append(all_pi, np.zeros(missing_elements))
	all_pi = all_pi.reshape((number_rows[0] + 1, col_width))

	# add the first line "3.1415926535" to list
	lines = [str(int(all_pi[0][0])) + "." + "".join(
		str(int(_)) for _ in all_pi[0][2:])]

	for row in range(1, int(number_rows)):
		# Add the remaining lines to list
		lines.append("".join(str(int(_)) for _ in all_pi[row]))

	print(f'\tReady to write to file...')

	if cp is not None:
		# If anything is passed to the checkpoint variable, ``cp``, wait for
		# user input before writing to the output file.
		input('Checkpoint parameter is not ``None``. '
		      'Press any key to continue. ')

	number_iters = _writer_thing(list_lines=lines, filename=fn,
	                             chunk_size=chunk_size)

	print(f'Iterations: {number_iters}')
	return number_iters  # todo: this doesn't work right now


def _writer_thing(list_lines, filename, chunk_size, iteration=0):
	"""Write the digits of pi to an output file

		:param list_lines: A list of the lines to write. The lines are the
			digits of pi broken up into n-character long lines, where n is a
			parameter passed to print_digits(...) as `col_width`; default is
			12 characters long.
		:type list_lines: list, tuple
		:param filename: the name of the output file to write the lines to.
		:type filename: str, PathLike
		:param chunk_size: The number of lines to write at a time.
		:type chunk_size: int
		:param iteration: An integer that keeps track of the recursion of this
			function. Default is 0.
		:type iteration: int
	"""
	# if len(list_lines) >= chunk_size:
	# 	_chunk_size = chunk_size
	# else:
	# 	_chunk_size = len(list_lines)

	if len(list_lines) < chunk_size:
		chunk_size = len(list_lines)

	# pi_out = open(file=filename, mode='a')
	with open(filename, 'a', encoding='utf-8') as pi_out:
		# for i, _ in enumerate(list_lines[:_chunk_size]):
		for i, _ in enumerate(list_lines[:chunk_size]):
			pi_out.write(list_lines.pop(0))
			pi_out.write("\n")
			if np.mod(i+1, 10) == 0:
				pi_out.write("\n")
	# pi_out.close()
	print(f'Wrote {chunk_size} lines to file. Saving file...')

	if len(list_lines) > 0:  # recursion case
		_writer_thing(
			list_lines=list_lines,
			filename=filename,
			chunk_size=chunk_size,
			iteration=iteration+1)
	else:  # return control to calling function.
		return iteration + 1


def main(x=1000, chunk_size=500, col_width=79):
	"""Do all the stuff

		:param x: The number of digits of pi to print. Default is 1,000.
		:type x: int
		:param chunk_size: The number of lines to print at a time.
			Default is 500.
		:type chunk_size: int
	"""
	print("\tRunning...")
	print(f'\tCalculating {x} digits of pi...')
	print_digits(col_width=col_width, x_digits=x, chunk_size=chunk_size)

	print(f'Finished formatting {x} digits of Pi.')
	return None


if __name__ == "__main__":
	# 1,000,000 digits = 44268.841465473175 seconds
	# main(x=100000, chunk_size=500)
	main(x=1000000, chunk_size=10, col_width=80)
