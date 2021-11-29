# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import student
# Press the green button in the gutter to run the script.

import math
def sigmoid(z):
    return 1.0/ (1+ math.exp(-1 * z))

if __name__ == '__main__':

    print(sigmoid(0.155))
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
