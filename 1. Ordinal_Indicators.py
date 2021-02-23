def getOrdinalIndicator(number):
    # sets the ordinalIndicator string to its initial, common value
    ordinalIndicator = "th"
    # defines a variable that helps the function skip to the return statement
    skipRemaining = False
    # makes the input number positive for easier comparison
    number = abs(number)
    # if the number is within the range, it ends with the initial string of "th"
    if 11 <= number <= 13 or number == 0:
        skipRemaining = True
    elif number > 9 and not skipRemaining:
        number %= 10
        if number == 0:
            # true for numbers what were initially multiples of ten
            skipRemaining = True
    # series of evaluations the number's last or only digit
    if number == 1 and not skipRemaining:
        ordinalIndicator = "st"
    elif number == 2 and not skipRemaining:
        ordinalIndicator = "nd"
    elif number == 3 and not skipRemaining:
        ordinalIndicator = "rd"
    return ordinalIndicator


# tests the function with a list of numbers and their ordinal indicators in a specified range
for rangeNumber in range(-14, 27):
    print(str(rangeNumber)+str(getOrdinalIndicator(rangeNumber)))

# test the function by printing an any input number with its ordinal indicator
testNumber = int(input("\nEnter number: "))
print("\n"+str(testNumber)+str(getOrdinalIndicator(testNumber))+"\n")
