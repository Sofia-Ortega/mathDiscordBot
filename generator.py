"""
Contains Generators for the equations
"""


from random import randint

def add_gen():
    """Takes no input. Returns str of unique 2 num equation and their sum"""
    num1 = randint(1, 10)
    num2 = randint(1, 10)
    sum = num1 + num2
    equation = str(num1) + " + " + str(num2) + " = "

    return equation, sum

def subtract_gen():
    """Takes no input. Returns str of unique 2 num equation and their difference"""
    num1 = randint(1, 10)
    num2 = randint(1, 10)
    diff = num1 - num2
    equation = str(num1) + " - " + str(num2) + " = "

    return equation, diff

def multiply_gen():
    """Takes no input. Returns str of unique 2 num equation and their product"""
    num1 = randint(1, 10)
    num2 = randint(1, 10)
    product = num1 * num2
    equation = str(num1) + " * " + str(num2) + " = "

    return equation, product


def division_gen():
    """Takes no input. Returns str of unique 2 num equation and their quotient"""
    quotient = randint(1, 10)
    num2 = randint(1, 10)
    num1 = quotient * num2

    equation = str(num1) + " / " + str(num2) + " = "

    return equation, quotient

def eq_gen():
    """Takes no input. Randomly returns sum_gen, subtract_gen, multiply_gen, or division_gen"""
    options = {
        1: add_gen(),
        2: subtract_gen(),
        3: multiply_gen(),
        4: division_gen()
    }

    # randomly picks a generator from options
    return options[randint(1, len(options))]
#
# for i in range(10):
#     eq, ans = eq_gen()
#     print(eq + " " + str(ans).ljust(20))