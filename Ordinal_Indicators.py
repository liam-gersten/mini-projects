def get_ordinal_indicator(number):
    # sets the ordinal_indicator string to its initial, common value
    ordinal_indicator = "th"
    # defines a variable that helps the function skip to the return statement
    skip_remaining = False
    # makes the input number positive for easier comparison
    number = abs(number)

    # if the number is within this unique range, it ends with the initial string of "th"
    if 11 <= number <= 13 or number == 0:
        skip_remaining = True

    # mods numbers greater that one digit so the function only evaluates its last digit
    elif number > 9 and not skip_remaining:
        number %= 10
        if number == 0:
            # this would  be the case for numbers what were initially multiples of ten
            skip_remaining = True

    # series of evaluations the number's last or only digit
    if number == 1 and not skip_remaining:
        ordinal_indicator = "st"
    elif number == 2 and not skip_remaining:
        ordinal_indicator = "nd"
    elif number == 3 and not skip_remaining:
        ordinal_indicator = "rd"
    # at this point, ending digits from 4 and 9 do not modify the get_ordinal_indicator, and receive its initial value

    # ** note: the function only returns the ordinal indicator, not the ordinal indicator and the input number **
    return ordinal_indicator


# tests the function with a list of numbers and their ordinal indicators in a specified range
for range_number in range(-14, 27):
    print(str(range_number) + str(get_ordinal_indicator(range_number)))

# test the function by printing an any input number with its ordinal indicator
test_number = int(input("\nEnter number: "))
print("\n" + str(test_number) + str(get_ordinal_indicator(test_number)) + "\n")
