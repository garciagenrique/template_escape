# -*- coding: utf-8 -*-

import numpy as np
from template_escape.code_escape import square_number


def test_square_number():
    test_number = square_number(np.random.random_sample())
    assert test_number > 0
