# -*- coding: utf-8 -*-
# Template module with an example for the ESCAPE project

import numpy as np
import argparse


def square_number(number):
    """
    Function that returns the square of the input number.

    Parameters:
    -----------
        number: int or float
            Number to square.

    Returns:
    --------
        np.square(number) : numpy.int64
            The square of the input number. The result is rounded to 3 decimal places !
    """
    return np.round(np.square(number), 3)


def main():
    """
    Prints the output of the square_number function, passed as an argument.

    """
    parser = argparse.ArgumentParser(description="Square the input number !")

    parser.add_argument('--input_number', '-i',
                        type=float,
                        dest='input',
                        help='Input number to square. Default = -7.',
                        default=-7.
                        )

    args = parser.parse_args()

    print('\n\tThe square of {} is {} !\n'.format(args.input,
                                                  square_number(args.input)
                                                  ))


if __name__ == '__main__':
    main()
