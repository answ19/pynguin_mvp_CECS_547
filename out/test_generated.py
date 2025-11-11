import sys, os
sys.path.insert(0, '.')
import triangle as mod

def test_bootstrap_0():
    res = mod.classify(1, 1, 1)
    assert res == 'equilateral'

def test_invalid_1():
    arg_0 = 1
    arg_1 = 2
    arg_2 = 9
    res = mod.classify(arg_0, arg_1, arg_2)
    assert res == 'invalid'

def test_boundary_2():
    arg_0 = 10
    arg_1 = 10
    arg_2 = 7
    res = mod.classify(arg_0, arg_1, arg_2)
    assert res == 'isosceles'

def test_boundary_3():
    arg_0 = 6
    arg_1 = 3
    arg_2 = 7
    res = mod.classify(arg_0, arg_1, arg_2)
    assert res == 'scalene'

def test_invalid_4():
    arg_0 = 0
    arg_1 = 5
    arg_2 = 5
    res = mod.classify(arg_0, arg_1, arg_2)
    assert res == 'invalid'

