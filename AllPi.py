#!/usr/bin/env python
# Filename: AllPi.py

"""
Format a string containing an arbitrary number of digits of Pi for output to
a text file.

This module contains a class that accomplishes all the functionality of the
functions in module ``all_the_pi.py``. This module supersedes module
``all_the_pi.py``

Created by als0052
Created on 02-16-2021
Updated on 02-16-2021
"""

from datetime import datetime as dt
from pathlib import Path
import numpy as np
import math


class AllPi:
	"""Create an object to print out ``x`` digits of pi

		:param x: The number of digits to print to the file. Default is 1000
		:type x: int
		:param col_width: The width of the line (number of characters per line)
			to print to file. Default is 12 characters.
		:type col_width: int
		:param fn: The file to print the result to. Default is None which
			results in filename of pattern
			``piPrinter_<chunk_size>x<col_width>x<x>_<mm-dd-yyyy>_<hhmmss>.
			txt``
		:type fn: Pathlike, str
		:param chunk_size: The number of lines to print in each group.
			Default is 10 lines per group.
		:type chunk_size: int
		:param cp: Checkpoint flag. If anything other than ``None`` enter the
			checkpoint and wait for user to press a key before printing file.
			Default value is None (checkpoint disabled)
		:type cp: None, bool, int, float, str


		Properties
		----------
		output_file: The name of the output file. Either returns the value
		             passed at object creation to parameter ``fn`` or returns
		             the default filename if parameter ``fn`` is ``None`` at
		             object creation.

		n: The total number of digits requested. This is the same as the
		   parameter ``x`` used during object creation.
	"""
	def __init__(self, x=1000, col_width=12, fn=None, chunk_size=10,
	             cp=None):
		self.x_digits = x
		self._total_digits = x
		self.col_width = col_width
		self.fn = fn
		self.chunk_size = chunk_size
		self._cp = cp
		
		if self.col_width < 2:
			msg = (f'col_width must be an integer >= 2. {self.col_width} is '
			       f'not a valid value')
			raise ValueError(msg)
		if self.x_digits > 11000000:
			msg = (f"Cannot operate with {self.n:,} digits. Execution time "
			       f"would be excessive.")
			raise RuntimeError(msg)		

		# todo: This will need some thought before it can be added to the logic
		# if self.chunk_size is None or self.chunk_size == 0:
		# 	# print output in one continuous block
		# 	pass
		if np.mod(self.chunk_size, 5) != 0:
			print('chunk_size must be a positive multiple of 5')
			ncs = int(math.ceil(abs(self.chunk_size)/5.0))*5
			print(f'Changing chunk_size from {self.chunk_size} to {ncs}')
			self.chunk_size = ncs
		if self.fn is None:
			date = dt.now().strftime("%m-%d-%Y_%H%M%S")
			fn = f'piPrinter_{self.chunk_size}x{self.col_width}x{self.n}_' \
			     f'{date}.txt'
			self.fn = Path(fn)
		self._pi_digits_list = list(self._pi_digits())
		self.list_lines = []
		self.iteration = 0

	def __repr__(self):
		r = (f'AllPi(x={self.x_digits}, col_width={self.col_width}, '
		     f'fn={str(self.fn.as_posix())}, chunk_size={self.chunk_size}, '
		     f'cp={self._cp}')
		return r

	@property
	def n(self):
		return self._total_digits

	@property
	def output_file(self):
		return str(self.fn.as_posix())

	def _pi_digits(self):
		"""Generate x_digits of Pi.

			Shamelessly usurped from StackOverflow
			https://stackoverflow.com/a/54967370/11895567

			Not sure what this method is doing but it works. Do not	touch.
		"""
		k, a, b, a1, b1 = 2, 4, 1, 12, 4
		while self.x_digits > 0:
			p, q, k = k*k, 2*k + 1, k + 1
			a, b, a1, b1 = a1, b1, p*a + q*a1, p*b + q*b1
			d, d1 = a/b, a1/b1
			while d == d1 and self.x_digits > 0:
				yield int(d)
				self.x_digits -= 1
				a, a1 = 10*(a % b), 10*(a1 % b1)
				d, d1 = a/b, a1/b1

	def _checkpoint(self):
		"""Enter a checkpoint state
		
			If anything is passed to the checkpoint flag wait for user input
			before writing to the output file.
		"""
		if self._cp is not None:
			print(f'\tCheckpoint invoked. \n\tReady to write to file...')
			input('\t\tPress any key to continue. ')
		return self

	def _write_digits(self, verbose=False):
		"""Write the digits of Pi to an output file

			:param verbose: Flag to change whether or not to print status
				messages to console. Default is False (disabled)
			:type verbose: bool
		"""
		if len(self.list_lines) < self.chunk_size:
			self.chunk_size = len(self.list_lines)

		with open(self.fn, 'a', encoding='utf-8') as pi_out:
			for i, _ in enumerate(self.list_lines[:self.chunk_size]):
				pi_out.write(self.list_lines.pop(0))
				pi_out.write("\n")
				if np.mod(i+1, self.chunk_size) == 0:
					# todo: Write header between each chunk similar to how
					#       NASTRAN does .f06 files
					pi_out.write("\n")
					# s = f'\n{(self.col_width+2)*" "}{i}\n'
					# pi_out.write(s)
		if verbose:
			print(f'\tWrote {self.chunk_size} lines to file. Saving file...')
		if len(self.list_lines) > 0:  # recursion case
			self.iteration += 1
			self._write_digits()
		return self

	def print_digits(self, verbose=False):
		"""Write the digits of pi to a file

			This method is the primary execution method for this object. Call
			this method to actually print the digits to the file

			:param verbose: Flag to turn on message printing to the console.
				Default is False.
			:type verbose: bool
		"""
		if verbose:
			print(f"Formatting {self.n:,} digits of Pi...")
		digits = [int(n) for n in self._pi_digits_list]
		left_side = np.array([3, np.nan])
		right_side = np.array([int(x) for x in digits[1:]])

		# combine left_side and right_side
		all_pi = np.append(left_side, right_side)
		number_elements = all_pi.shape
		number_rows = np.floor_divide(number_elements, self.col_width)

		if np.mod(number_elements, self.col_width) != 0:
			# Add zeros to the end of the array to make it evenly divisible by
			# self.col_width
			# todo: Fill the line with spaces instead of zeros.
			missing_elements = np.mod(number_elements, self.col_width)
			missing_elements = self.col_width - missing_elements
			all_pi = np.append(all_pi, np.zeros(missing_elements))
		all_pi = all_pi.reshape((number_rows[0] + 1, self.col_width))

		# add the first line "3.1415926535..." to list
		self.list_lines = [str(int(all_pi[0][0])) + "." + "".join(
			str(int(_)) for _ in all_pi[0][2:])]
		for row in range(1, int(number_rows)):
			# Add the remaining lines to list
			self.list_lines.append("".join(str(int(_)) for _ in all_pi[row]))

		self._checkpoint()
		self._write_digits(verbose=verbose)
		if verbose:
			print(f"\nFinished formatting {self.n:,} digits of Pi...")
			print(f'\tIterations: {self.iteration}')
			print(f"\tOutput located in file:\n\t{self.output_file}")
		return self


def main(x=1000, chunk_size=10, col_width=12):
	"""Create an AllPi object and print it to file

		:param x: The number of digits of pi to print. Default is 1,000.
		:type x: int
		:param chunk_size: The number of lines to print at a time.
			Default is 10.
		:type chunk_size: int
		:param col_width: The width of the column to print. Default is 12.
		:type col_width: int
	"""
	ap = AllPi(x=x, chunk_size=chunk_size, col_width=col_width)
	ap.print_digits(verbose=True)
	return None


if __name__ == "__main__":
	main(x=10000, chunk_size=10, col_width=50)
