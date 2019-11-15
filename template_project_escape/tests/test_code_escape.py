# -*- coding: utf-8 -*-

import numpy as np
from template_project_escape.code_template_escape import square_number


def test_square_number():
    test_number = square_number(np.random.random_sample())
    assert test_number > 0
    np.testing.assert_equal(square_number(2), 4)  # Another example of syntax for the unitary test
