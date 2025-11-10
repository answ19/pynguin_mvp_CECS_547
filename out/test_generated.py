import sys, os
sys.path.insert(0, '.')
import triangle as mod

def test_case_0():
    res = mod.classify(1, 1, 1)
    assert res == 'equilateral'

def test_case_1():
    arg_a = 6
    arg_b = 3
    arg_c = 7
    res = mod.classify(arg_a, arg_b, arg_c)
    assert res == 'scalene'

def test_case_2():
    arg_a = 1
    arg_b = 2
    arg_c = 9
    res = mod.classify(arg_a, arg_b, arg_c)
    assert res == 'invalid'

def test_case_3():
    arg_a = 10
    arg_b = 10
    arg_c = 7
    res = mod.classify(arg_a, arg_b, arg_c)
    assert res == 'isosceles'

