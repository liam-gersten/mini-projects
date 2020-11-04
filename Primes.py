import bisect
import math
from tkinter import *


def create_window(scale_x, version, a, b):
    window = Tk()
    title = "Composites ⊆ [" + str(a) + ", " + str(b) + "]"
    if version == 1:
        title = "Prime Numbers ⊆ [" + str(a) + ", " + str(b) + "]"
    window.title(title)
    window.geometry(f'{int(round(750*scale_x, 0))}x{750}')
    return window


def create_canvas(window):
    canvas = Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill=BOTH, expand=1)
    return canvas


# helper function that favors a best case approach for searching a numbers factors
def check_prime(number, existing):
    for p in existing:
        if number % p == 0:
            return False
    return True


# generates a list of composite numbers from two to the upper range
def composites(y, composites):
    if y >= 2:
        maximum = int(round((math.sqrt(y)), 0))
        while (maximum**2) > y:
            maximum -= 1
        for i in range(2, int(round((y/2), 0)+1)):
            bisect.insort(composites, (i*2))
        for check in range(3, (maximum+1)):
            if check not in composites:
                for i in range(2, int(round((y/check), 0)+1)):
                    if (i*check) not in composites:
                        bisect.insort(composites, (i*check))
    return composites


# generates a list of prime numbers from three to the upper range (two is given)
def primes(y, primes):
    for i in range(3, y+1, 2):
        if check_prime(i, primes):
            primes.append(i)
    return primes


# used to create and display the desired list
def main(version, a, b, number):
    # the dimensions and corresponding rows/columns are changed to make the list reasonably displayable
    iteration = 0
    columns = int(round(math.sqrt(b-a), 0))
    if (b-a) % columns >= 0.5:
        change = 1
    else:
        change = -1
    while (b-a) % columns != 0:
        columns += change
        iteration += 1
        if iteration >= 3:
            b += 1
            columns = int(round(math.sqrt(b-a), 0))
    rows = int((b-a)/columns)
    # list, window, and canvas creation
    if version == 1:
        list = primes((b+2), [2])
    else:
        list = composites((b+2), [])
    window = create_window((columns/rows), version, a, b+2)
    canvas = create_canvas(window)
    if a <= 1:
        number = 2
    # creates a 2D-List-like grid of canvas rectangles to create on the canvas
    for row_index in range(rows):
        for column_index in range(columns):
            box_color = "white"
            text = "black"
            if number in list:
                box_color = "blue"
                text = "white"
            canvas.create_rectangle((column_index*(750/rows)), (row_index*(750/rows)),
                                    ((column_index*(750/rows))+(750/rows)), ((row_index*(750/rows))+(750/rows)),
                                    fill=box_color)
            canvas.create_text(((column_index*(750/rows))+((750/rows)/2)), ((row_index*(750/rows))+((750/rows)/2)),
                               fill=text,
                               font=("Times " + str(int(round(((750/rows)*(0.5-(0.1*(math.log((number/100), 10))))),
                                                              0))) + " bold"), text=str(number))
            number += 1
    window.mainloop()


bottom = int(input("Enter lower range: "))
top = int(input("Enter upper range: "))
prompt = int(input("Would you like to:\n(1). Display primes in range, \nor\n(2). Display composites in range?\n"))
main(prompt, bottom, top, bottom)
