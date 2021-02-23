# tells the main function to use or ignore rarer denominations like two dollar bills or half dollar coins
def rareDenominationPrompt(rareDenominationType, rareDenominationNumber):
    while True:  # prompts the user to input whether or not they'd like to use the specified rare denomination
        choice = input("Would you like to use "+rareDenominationType+"? ")
        choice = choice.upper()
        if choice == "YES":
            if rareDenominationType == "two-dollar bills":
                return rareDenominationNumber+2
            return rareDenominationNumber+0.5
        if choice == "NO":
            return rareDenominationNumber
        print("Invalid choice, please enter \"Yes\" or \"No\"")


# uses basic recursion to build the main statement from lists that it modifies
def denominationStatement(cValue, tValue, constantList, statementList, used):
    if len(constantList) or len(statementList) != 0:  # the recursive case of the function
        denominationStr = (statementList[0][0])  # defaults the denomination string to an empty string
        denominationNumber = 0  # defaults the number of the denomination being used to 0
        while cValue+constantList[0] <= tValue:
            denominationNumber += 1
            cValue += constantList[0]
            cValue = round(cValue, 2)
            denominationStr = (statementList[0][1])  # where there is only one of the denomination
            if denominationNumber > 1:
                denominationStr = (str(denominationNumber))+(statementList[0][2])
        constantList.pop(0)
        statementList.pop(0)
        if cValue == tValue:
            denominationStr = denominationStr.replace(", ", ".")
            if used:  # the main string already has another denomination, so "and " is necessary
                denominationStr = "and "+denominationStr
            constantList = []
            statementList = []
        if denominationNumber != 0:
            used = True
        return denominationStr+denominationStatement(cValue, tValue, constantList, statementList, used)
        # calls itself on the updated versions of denomination_constants/statements, with an updated cValue
    return ""  # the base case: where nothing should be added to the statement


# modifies the main lists to reflect the rare denominations that are used, and also prints the main statement
def mainStatement(targetValue, rareDenominationNumber):
    if targetValue == 0:
        return "\nYou don't need anything!\n"
    constants = [100, 50, 20, 10, 5, 2, 1, 0.5, 0.25, 0.1, 0.05, 0.01]
    statements = [["", "a hundred-dollar bill, ", " hundreds, "], ["", "a fifty-dollar bill, ", " fifties, "],
                  ["", "a twenty-dollar bill, ", " twenties, "], ["", "a ten-dollar bill, ", " tens, "],
                  ["", "a five-dollar bill, ", " fives, "], ["", "a two-dollar bill, ", " two-dollar bills, "],
                  ["", "a one-dollar bill, ", " ones, "], ["", "a half-dollar coin, ", " half-dollar coins, "],
                  ["", "a quarter, ", " quarters, "], ["", "a dime, ", " dimes, "], ["", "a nickel, ", " nickels, "],
                  ["", "a penny, ", " pennies, "]]
    if rareDenominationNumber == 2:  # in this case, we want to use two's, but not half dollar coins
        constants.remove(0.5)
        statements.pop(7)
    elif rareDenominationNumber == 0.5:  # in this case, we want to use half dollar coins, but not two's
        constants.remove(2)
        statements.pop(5)
    elif rareDenominationNumber == 0:  # here, we want to remove all rare denominations from our lists
        constants.remove(2)
        constants.remove(0.5)
        statements.pop(5)
        statements.pop(6)
    # calls the recursive function that creates the main statement from the target value and the two lists above:
    return "\nYou're gonna need "+denominationStatement(0, targetValue, constants, statements, False)+"\n"


def mainPrompts(rareDenominationNumber):  # acts as a hub to call everything and prompt choice
    rareDenominationNumber = rareDenominationPrompt("two-dollar bills", rareDenominationNumber)
    rareDenominationNumber = rareDenominationPrompt("half-dollar coins", rareDenominationNumber)
    while True:  # this outer loop keeps the program running by prompting new inputs
        print(mainStatement(round(float(input("How much will you be spending today? $ ")), 2),
                            rareDenominationNumber))
        choiceLoop = True
        while choiceLoop:  # this inner loop prompts a user to exit or reset their target value
            choice = input("Would you like to RESET your money, or EXIT? ")
            choice = choice.upper()
            if choice == "EXIT":
                exit()
            elif choice != "RESET":
                print("Invalid choice, please enter \"Reset\" or \"Exit\"")
            else:
                choiceLoop = False


mainPrompts(0)  # no rare denominations are used by default
