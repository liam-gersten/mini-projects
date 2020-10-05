import operator

# these are used to prompt different user inputs or use operators on their inputs
statements = [["", "First ", "", "Second "],
              ["Command", "Number", "Operator", "Number"],
              ["", "a Valid "],
              ["Enter ", "Invalid "],
              [": ", ""]]
operator_dictionary = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
    'ROOT': operator.pow
}


# this converts whole number floats into integers
def integer(number):
    if number % 1 == 0:
        return int(number)
    return number


# this function prints different prompts and messages, based on the statements 2D list and different scenarios
def print_prompt(prompt_number, statement_type, prompt_iteration):
    return ((statements[3][statement_type]) + (statements[2][prompt_iteration]) + (statements[0][prompt_number]) +
            (statements[1][prompt_number]) + (statements[4][statement_type]))


# this is used to prompt the user to give commands, numbers and operators, and also ensures they are valid/correct
def value_creator(prompt_version, comparison_list):
    value_creation_loop = True
    creation_attempts = 0
    exclamation_point = "!"
    while value_creation_loop:
        new_value = input(print_prompt(prompt_version, 0, creation_attempts))
        if prompt_version == 1 or prompt_version == 3:
            # where the input should be the first number or the second
            integer = True
            try:
                int(new_value)
            except ValueError:
                integer = False
            if integer:
                return int(new_value)
        elif prompt_version == 0:
            # the input should be a command, which will need to be made uppercase
            if new_value.upper() in comparison_list:
                return new_value.upper()
        elif new_value.upper() in comparison_list:
            # the input should be one of the known operators
            return new_value.upper()
        if value_creation_loop:
            # if this is reached, the input is unknown or invalid and the print statement will make that clear
            creation_attempts = 1
            exclamation_point += "!"
            print(print_prompt(prompt_version, 1, 0) + exclamation_point)


# this is where the "calculating" is done
def calculations(num1, num2, operator, operator_dict):
    pre_statement = "Your Answer is: "
    if operator in operator_dict and operator != "ROOT":
        # this is used for any operator in the operator dictionary except for "ROOT"
        op = operator_dict.get(operator)
        return pre_statement + str(integer(op(num1, num2))) + "\n"
    elif operator == "=":
        if num1 == num2:
            return pre_statement + "True" + "\n"
        else:
            return pre_statement + "False" + "\n"
    elif operator == "%":
        return pre_statement + str(integer(num1 * num2 * 0.01)) + "\n"
    elif operator in ["Root", "root", "ROOT"]:
        operator = operator.upper()
        op = operator_dict.get(operator)
        return pre_statement + str(integer(op(num1, (1 / num2)))) + "\n"


# this function acts as the "hub" of everything, and calls everything else
def prompts():
    calculator_use = 0
    known_operators = ["+", "-", "*", "/", "=", "^", "ROOT", "%"]
    valid_commands = ["ON", "OFF", "RESET", "CLEAR", "YES", "Y", "NO", "N"]
    thank_you = ["It's a shame you didn't use my calculator\n:(", "Thank you for using my calculator!"]
    while True:
        command = value_creator(0, valid_commands)
        if command == "OFF":
            print(thank_you[calculator_use])
            exit()
        else:
            number_1 = value_creator(1, [])
            operator = value_creator(2, known_operators)
            number_2 = value_creator(3, [])
            calculator_use = 1
            print(calculations(number_1, number_2, operator, operator_dictionary))


prompts()
