#!/usr/bin/env python
# Filename: calc_pi.py

"""
Experimental module containing code for a more efficient pi generator function

See also: https://www.w3resource.com/projects/python/python-projects-1.php

Created by: als0052
Created on: 02-22-2021
Updated on: 02-22-2021
"""

from pathlib import Path


def calc_pi(limit=1000):
	"""Prints out the digits of pi until the given limit
	
		:param limit: The maximum number of digits of pi to calculate. 
			Default is 1000 digits to the right of the decimal place.
		:type limit: int
	"""
	q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
	decimal, counter = limit, 0
	
	while counter != decimal + 1:
		if 4*q + r - t < n*t:
			yield n
			if counter == 0:
				yield '.'
			if decimal == counter:
				print('')
				break
			counter += 1
			nr, n = 10*(r - n*t), ((10*(3*q + r)) // t) - 10*n
			q *= 10
			r = nr
		else:
			nr, nn = (2*q + r)*l, (q*(7*k) + 2 + (r*l)) // (t*l)
			q *= k
			t *= l
			l += 2
			k += 1
			n, r = nn, nr

def make_pi(n_digit, fnout=None, col_width=20, cs=4, bs=5):
	"""Make the pi output file
	
		:param n_digit: The number of digits to the right of the decimal 
			point to calculate for pi
		:type n_digit: int
		:param fnout: The output filename
		:type fnout: Pathlike, str
		:param col_width: The maximum number of characters per line in the 
			output file. Default is 89 characters
		:type col_width: int
		:param cs: Chunk size. The number of lines to accumulate before 
			adding to the block. Each chunk will be followed by a blank 
			line when printed to the output file. Default is 10.
		:type cs: int
		:param bs: Block size. The number of chunks to accumulate before 
			printing to output file. Default is 5.
		:type bs: int
	"""
	msg = (f'Running...\nCreating output file {fnout.stem} with {n_digit:,} '
	       f'digits of pi')
	print(msg, end='\n\n')

	i = 0
	page_no = 1
	chunk_buf = []
	block_buf = []
	line_buf = []

	pi_digits = calc_pi(limit=n_digit)
	
	for digit in pi_digits:
		line_buf += str(digit)
		i += 1
		if i == col_width - 1:
			line_buf += '\n'
			line_buf = ''.join(line_buf)
			chunk_buf.append(line_buf)
			i = 0
			line_buf = []
		if len(chunk_buf) >= cs:
			block_buf.append(chunk_buf)
			chunk_buf = []
		if len(block_buf) >= bs:
			with open(fnout, 'a', encoding='utf-8') as fout:
				for cn, chunk in enumerate(block_buf):
					chunk_out = ''.join(chunk)
					print(chunk_out, file=fout)
					msg = f'\tWrote chunk {cn} of {len(block_buf)} to file...'
					print(msg)
			print(f'Finished writing page {page_no} to output file...')
			page_no += 1
			block_buf = []
	return None


if __name__ == "__main__":
	output_file = Path('pi.txt')
	make_pi(n_digit=89*100, fnout=output_file)
