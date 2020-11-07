"""
Contains Generators for the equations
"""

from random import randint

def add_gen(rangeArray):
    """Takes array of min and max values. Returns str of unique 2 num equation and their sum"""
    num1 = randint(rangeArray[0], rangeArray[1])
    num2 = randint(rangeArray[0], rangeArray[1])

    sum = num1 + num2
    equation = str(num1) + " + " + str(num2) + " = "

    return equation, sum

def subtract_gen(rangeArray):
    """Takes array of min and max values. Returns str of unique 2 num equation and their difference"""
    num1 = randint(rangeArray[0], rangeArray[1])
    num2 = randint(rangeArray[0], rangeArray[1])
    diff = num1 - num2
    equation = str(num1) + " - " + str(num2) + " = "

    return equation, diff

def multiply_gen(rangeArray):
    """Takes array of min and max values. Returns str of unique 2 num equation and their product"""
    num1 = randint(rangeArray[0], rangeArray[1])
    num2 = randint(rangeArray[2], rangeArray[3])
    product = num1 * num2
    equation = str(num1) + " * " + str(num2) + " = "

    return equation, product


def division_gen(rangeArray):
    """Takes array of min and max values. Returns str of unique 2 num equation and their quotient"""
    quotient = randint(rangeArray[0], rangeArray[1])
    num2 = randint(rangeArray[2], rangeArray[3])
    num1 = quotient * num2

    equation = str(num1) + " / " + str(num2) + " = "

    return equation, quotient

# Level: [[add min and max], [subtract min and max], [multiply min and max], [divide min and max]]
levels = {
    "easy": [[1, 10], [1, 10], [1, 10, 1, 10], [1, 10, 1, 10]],
    "medium": [[1, 100], [1, 100], [1, 100, 1, 10], [1, 100, 1, 10]],
    "hard": [[1, 1000], [1, 1000], [1, 100, 1, 100], [1, 100, 1, 100]]
}


#FIXME: in main, add eq_gen(difficulty) with difficulty gotten from user
def eq_gen(difficulty):
    """Takes in difficulty. Randomly returns sum_gen, subtract_gen, multiply_gen, or division_gen"""


    options = {
        1: add_gen(levels[difficulty][0]),
        2: subtract_gen(levels[difficulty][1]),
        3: multiply_gen(levels[difficulty][2]),
        4: division_gen(levels[difficulty][3])
    }

    # randomly picks a generator from options
    return options[randint(1, len(options))]


# # difficulty = input("easy, medium, hard")
# difficulty = "hard"
# for i in range(20):
#
#     # print(add_gen(levels[difficulty][0]))
#     eq, ans = eq_gen(difficulty)
#     print(eq + " " + str(ans).ljust(20))



