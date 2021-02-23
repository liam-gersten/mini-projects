import bisect
import math
from tkinter import *


def createWindow(scale_x, version, a, b):
    window = Tk()
    title = "Composites ⊆ [" + str(a) + ", " + str(b) + "]"
    if version == 1:
        title = "Prime Numbers ⊆ [" + str(a) + ", " + str(b) + "]"
    window.title(title)
    window.geometry(f'{int(round(750*scale_x, 0))}x{750}')
    return window


def createCanvas(window):
    canvas = Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill=BOTH, expand=1)
    return canvas


# favors a best case approach for searching a numbers factors
def checkPrime(number, existing):
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
        if checkPrime(i, primes):
            primes.append(i)
    return primes


# used to create and display the desired list
def main(version, a, b, number):
    # dimensions and rows/columns are changed to be displayed
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
    window = createWindow((columns/rows), version, a, b+2)
    canvas = createCanvas(window)
    if a <= 1:
        number = 2
    # creates a 2D-List-like grid of canvas rectangles to create on the canvas
    for rowIndex in range(rows):
        for columnIndex in range(columns):
            boxColor = "white"
            text = "black"
            if number in list:
                boxColor = "blue"
                text = "white"
            canvas.create_rectangle((columnIndex*(750/rows)),
                                    (rowIndex*(750/rows)),
                                    ((columnIndex*(750/rows))+(750/rows)),
                                    ((rowIndex*(750/rows))+(750/rows)),
                                    fill=boxColor)
            canvas.create_text(((columnIndex*(750/rows))+((750/rows)/2)),
                               ((rowIndex*(750/rows))+((750/rows)/2)),
                               fill=text,
                               font=(
            "Times "+str(int(round(((750/rows)*(0.5-(0.1*(math.log((number/100),
                                    10))))), 0))) + " bold"), text=str(number))
            number += 1
    window.mainloop()


bottom = int(input("Enter lower range: "))
top = int(input("Enter upper range: "))
prompt = int(input("Would you like to:\n(1). Display primes in range, "
                   "\nor\n(2). Display composites in range?\n"))
main(prompt, bottom, top, bottom)
