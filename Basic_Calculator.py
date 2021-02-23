import operator

# used to prompt different user inputs or use operators on their inputs
statements = [["", "First ", "", "Second "],
              ["Command", "Number", "Operator", "Number"],
              ["", "a Valid "],
              ["Enter ", "Invalid "],
              [": ", ""]]
operatorDictionary = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
    'ROOT': operator.pow
}


# converts whole number floats into integers
def integer(number):
    if number % 1 == 0: return int(number)
    return number


# prints different prompts and messages, based on the statements 2D list and different scenarios
def printPrompt(promptNumber, statementType, promptIteration):
    return ((statements[3][statementType])+(statements[2][promptIteration])+(statements[0][promptNumber])+
            (statements[1][promptNumber])+(statements[4][statementType]))


# used to prompt the user to give commands, numbers and operators, and also ensures they are valid/correct
def valueCreator(promptVersion, comparisonList):
    valueCreationLoop = True
    creationAttempts = 0
    exclamationPoints = "!"
    while valueCreationLoop:
        newValue = input(printPrompt(promptVersion, 0, creationAttempts))
        if promptVersion == 1 or promptVersion == 3:
            # where the input should be the first number or the second
            integer = True
            try: int(newValue)
            except ValueError: integer = False
            if integer: return int(newValue)
        elif promptVersion == 0:
            # the input should be a command, which will need to be made uppercase
            if newValue.upper() in comparisonList: return newValue.upper()
        elif newValue.upper() in comparisonList: return newValue.upper()
        if valueCreationLoop:
            # if this is reached, the input is unknown or invalid and the print statement will make that clear
            creationAttempts = 1
            exclamationPoints += "!"
            print(printPrompt(promptVersion, 1, 0) + exclamationPoints)


def calculations(num1, num2, operator, operatorDict):
    statement = "Your Answer is: "
    if operator in operatorDict and operator != "ROOT":
        # this is used for any operator in the operator dictionary except for "ROOT"
        op = operatorDict.get(operator)
        return statement + str(integer(op(num1, num2))) + "\n"
    elif operator == "=":
        if num1 == num2: return statement+"True"+"\n"
        return statement + "False" + "\n"
    elif operator == "%": return statement+str(integer(num1*num2*0.01))+"\n"
    elif operator in ["Root", "root", "ROOT"]:
        operator = operator.upper()
        op = operatorDict.get(operator)
        return statement+str(integer(op(num1, (1/num2))))+"\n"


def prompts(operatorDictionary):
    calculatorUse = 0
    knownOperators = ["+", "-", "*", "/", "=", "^", "ROOT", "%"]
    validCommands = ["ON", "OFF", "RESET", "CLEAR", "YES", "Y", "NO", "N"]
    thankYou = ["It's a shame you didn't use my calculator\n:(", "Thank you for using my calculator!"]
    while True:
        command = valueCreator(0, validCommands)
        if command == "OFF":
            print(thankYou[calculatorUse])
            exit()
        else:
            num1 = valueCreator(1, [])
            operator = valueCreator(2, knownOperators)
            num2 = valueCreator(3, [])
            calculatorUse = 1
            print(calculations(num1, num2, operator, operatorDictionary))


prompts(operatorDictionary)
