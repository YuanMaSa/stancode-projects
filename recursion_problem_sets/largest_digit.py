"""
File: largest_digit.py
Name:
----------------------------------
This file recursively prints the biggest digit in
5 different integers, 12345, 281, 6, -111, -9453
If your implementation is correct, you should see
5, 8, 6, 1, 9 on Console.
"""


def main():
	print(find_largest_digit(12345))      # 5
	print(find_largest_digit(281))        # 8
	print(find_largest_digit(6))          # 6
	print(find_largest_digit(-111))       # 1
	print(find_largest_digit(-9453))      # 9

def find_largest_digit(n):
	"""
	:param n:
	:return:
	"""
	return find_largest_digit_helper(n, 0)

def find_largest_digit_helper(input_number, largest_num):
	"""
	helper function to find the largest number
	:param input_number:
	:param largest_num:
	:return:
	"""
	input_number = abs(input_number)
	divisor = 10 ** get_digit_num_helper(input_number, 0)
	if input_number // divisor > largest_num:
		largest_num = input_number // divisor

	if input_number % divisor == 0:
		# base case
		return largest_num

	# recursion case
	return find_largest_digit_helper(input_number % divisor, largest_num)

def get_digit_num_helper(num, count):
	"""
	return the number of zeros for x-digit number
	e.g. three-digit number --> 10**2, four-digit number --> 10**3

	:param num:
	:param count:
	:return:
	"""
	if num == 0:
		return count-1
	return get_digit_num_helper(num//10, count+1)


if __name__ == '__main__':
	main()
