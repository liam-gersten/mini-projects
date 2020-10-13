# tells the main function to use or ignore rarer denominations like two dollar bills or half dollar coins
def rare_denomination_prompt(rare_denomination_type, rare_denomination_number):
    while True:  # prompts the user to input whether or not they'd like to use the specified rare denomination
        choice = input("Would you like to use " + rare_denomination_type + "? ")
        choice = choice.upper()
        if choice == "YES":
            if rare_denomination_type == "two-dollar bills":
                return rare_denomination_number + 2
            else:
                return rare_denomination_number + 0.5
        if choice == "NO":
            return rare_denomination_number
        else:
            print("Invalid choice, please enter \"Yes\" or \"No\"")


# uses basic recursion to build the main statement from lists that it modifies
def denomination_statement(c_value, t_value, constant_list, statement_list, previously_used):
    if len(constant_list) or len(statement_list) != 0:  # the recursive case of the function
        denomination_string = (statement_list[0][0])  # defaults the denomination string to an empty string
        denomination_number = 0  # defaults the number of the denomination being used to 0
        while c_value + constant_list[0] <= t_value:
            denomination_number += 1
            c_value += constant_list[0]
            c_value = round(c_value, 2)
            denomination_string = (statement_list[0][1])  # where there is only one of the denomination
            if denomination_number > 1:
                denomination_string = (str(denomination_number)) + (statement_list[0][2])
        constant_list.pop(0)  # the lists are destructively modified before being passed to the recursive call
        statement_list.pop(0)
        if c_value == t_value:  # the main statement should end here, with a period instead of a comma
            denomination_string = denomination_string.replace(", ", ".")
            if previously_used:  # the main string already has another denomination, so "and " is necessary
                denomination_string = "and " + denomination_string
            constant_list = []
            statement_list = []  # the denomination_constants/statements are destroyed, so all future recursive
            # ... calls will return an empty string (the base case where the list is empty)
        if denomination_number != 0:
            previously_used = True
        return denomination_string + denomination_statement(c_value, t_value, constant_list, statement_list,
                                                            previously_used)
        # calls itself on the updated versions of denomination_constants/statements, with an updated c_value
    return ""  # the base case: where nothing should be added to the statement


# modifies the main lists to reflect the rare denominations that are used, and also prints the main statement
def main_statement(target_value, rare_denomination_number):
    if target_value == 0:
        return "\nYou don't need anything!\n"
    constants = [100, 50, 20, 10, 5, 2, 1, 0.5, 0.25, 0.1, 0.05, 0.01]
    statements = [["", "a hundred-dollar bill, ", " hundreds, "], ["", "a fifty-dollar bill, ", " fifties, "],
                  ["", "a twenty-dollar bill, ", " twenties, "], ["", "a ten-dollar bill, ", " tens, "],
                  ["", "a five-dollar bill, ", " fives, "], ["", "a two-dollar bill, ", " two-dollar bills, "],
                  ["", "a one-dollar bill, ", " ones, "], ["", "a half-dollar coin, ", " half-dollar coins, "],
                  ["", "a quarter, ", " quarters, "], ["", "a dime, ", " dimes, "], ["", "a nickel, ", " nickels, "],
                  ["", "a penny, ", " pennies, "]]
    if rare_denomination_number == 2:  # in this case, we want to use two's, but not half dollar coins
        constants.remove(0.5)
        statements.pop(7)
    elif rare_denomination_number == 0.5:  # in this case, we want to use half dollar coins, but not two's
        constants.remove(2)
        statements.pop(5)
    elif rare_denomination_number == 0:  # here, we want to remove all rare denominations from our lists
        constants.remove(2)
        constants.remove(0.5)
        statements.pop(5)
        statements.pop(6)
    # calls the recursive function that creates the main statement from the target value and the two lists above:
    return "\nYou're gonna need " + denomination_statement(0, target_value, constants, statements, False) + "\n"


def main_prompts(rare_denomination_number):  # acts as a hub to call everything and prompt choice
    rare_denomination_number = rare_denomination_prompt("two-dollar bills", rare_denomination_number)
    rare_denomination_number = rare_denomination_prompt("half-dollar coins", rare_denomination_number)
    while True:  # this outer loop keeps the program running by prompting new inputs
        print(main_statement(round(float(input("How much will you be spending today? $ ")), 2),
                             rare_denomination_number))
        choice_loop = True
        while choice_loop:  # this inner loop prompts a user to exit or reset their target value
            choice = input("Would you like to RESET your money, or EXIT? ")
            choice = choice.upper()
            if choice == "EXIT":
                exit()
            elif choice != "RESET":
                print("Invalid choice, please enter \"Reset\" or \"Exit\"")
            else:
                choice_loop = False


main_prompts(0)  # by default, no rare denominations are used
