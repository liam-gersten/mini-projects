from tkinter import *
from functools import partial
import random
import math
import copy

# tries directly evaluating the formatted string
def evaluate(string):
    # elements used for factorial are replaced with 'math.factorial(elements)'
    if '!' in string:
        factorialIndex = string.find('!')
        string = 'math.factorial('+string[:factorialIndex]+')'+\
                 string[factorialIndex+1:]
    try: evaluated = eval(string)
    except: evaluated = 'Error'
    return evaluated

# places asterisks in the string based on locations found in addOperators
def addAstericks(string, locations):
    newString = ''
    for i in range(len(string)):
        if (locations != []) and (i == locations[0]):
            newString += ('*'+string[i])
            locations.pop(0)
        else: newString += string[i]
    return newString

# checks appropriateness of placing * between 2 classified characters
def checkSwitch(priorType, currentType, operators, others, prior, current):
    if priorType == operators:
        if (currentType == operators) and (prior == ')') and (current == '('):
            return True
        elif (currentType != operators) and (prior == ')'): return True
    if priorType == others:
        if (currentType == operators) and (current == '('): return True
        elif currentType != operators: return True
    return False

# categorizes characters and adds operators needed for direct evaluation
def addOperators(inputStr, operators, functions, others):
    [places,priorType,currentType] = [[],None,None]
    [switch,current,finalPlaces] = [False,'',[]]
    for i in range(len(inputStr)):
        checkCurrentType = copy.copy(currentType)
        checkPriorType = copy.copy(priorType)
        character = inputStr[i]
        if (character == 'm') and (inputStr[i+1] != '.') and \
                (inputStr[i+1] != '('):  # usually a func
            if (inputStr[i:i+7] != 'math.pi') and (inputStr[i:i+6] != 'math.e'):
                [priorType,switch] = [currentType,True]
                [currentType,current] = [functions,'m']
            else:  # current starts with m but is not a function
                [priorType,switch] = [currentType,True]
                [currentType,current] = [others,character]
        elif (character == 'r') and (inputStr[i:i+13] == 'random.random'):
            [priorType,switch] = [currentType,True]
            [currentType,current] = [others,'r']
        elif (character in operators) and (current+'(' not in functions):
            # functions parenthesis do not count
            [priorType,switch] = [currentType,True]
            [currentType,current] = [operators,character]
        elif character in others:
            if (inputStr[i-1] != 'h') and (inputStr[i-1] != 'm'):
                # does not include 'math' or 'random'
                [priorType,switch] = [currentType,True]
                [currentType,current] = [others,character]
        else: current += character
        if (inputStr[i-1] in others[3:]) and (character in others[3:]):
            switch = False
            # digits next to each other behave differently and don't need *
        if ((currentType != checkCurrentType) or (priorType != checkPriorType))\
                and switch:
            if checkSwitch(priorType, currentType, operators, others,
                           inputStr[i-1], character):
                places += [i]
                switch = False
    for place in places:
        if (inputStr[place-2:place] != 'om') and (inputStr[place-5:place] !=
                'log10'):  # specific cases: random and log10
            finalPlaces += [place]
    inputStr = addAstericks(inputStr, finalPlaces)
    return inputStr

# balances parenthesis and converts text strings for use of the math module
def classify(inputStr, operators, string):
    for element in inputStr:
        if (element.isalpha()) and (element != 'π'): string += element.upper()
        else: string += element
    for operator in operators:
        string = string.replace(operator, operators[operator])
    for element in string:
        if element.isalpha() and element.isupper() and element.lower() != 'π':
            return 'Error: unknown variable \''+str(element)+'\''
    if string.count(')') > string.count('('):
        return 'Error: missing parenthesis'
    while string.count('(') > string.count(')'):
        string += ')'
    operators = [')','(','*','/','+','-','!']
    functions = ['math.fabs(','math.asin(','math.acos(','math.atan(',
                 'math.sqrt(','math.sin(','math.cos(','math.tan(','math.log(',
                 'math.log10(']
    others = ['math.pi','math.e','random.random()','0','1','2','3','4','5','6',
              '7','8','9','.']
    string = addOperators(string, operators, functions, others)
    return evaluate(string)

# sends entries to be classified, cleaned, and evaluated
def buttonCmd(input, ebox, entry):
    operators = {'ABS(': 'math.fabs(','ASIN(': 'math.asin(','ACOS(':
        'math.acos(','ATAN(': 'math.atan(','√(': 'math.sqrt(','SIN(':
        'math.sin(','COS(': 'math.cos(','TAN(': 'math.tan(','π': 'math.pi',
        'LN(': 'math.log(','LOG(': 'math.log()','LOG10(':'math.log10(','E':
        'math.e','RAND': 'random.random()','(-)': '(-1)','^': '**','X': '*','[':
        '(',']': ')','{':'(','}': ')','÷': '/'}
    if input == 'Clear': entry.delete(0, 'end')
    elif input == 'Enter':
        evaluated = classify(str(ebox.get()+''), operators, '')
        ebox.set((evaluated))
    else: ebox.set(ebox.get()+input)

# creates 39 frames, 35 buttons, and 1 entry with text to pass into buttonCmd
def createVisuals(scale, root, ebox, texts):
    [frames, buttons] = [{}, {}]
    mainFrame = Frame(root, height=round(16*scale), width=round(10*scale))
    mainFrame.pack_propagate(0)
    mainFrame.grid(row=0, column=0, padx=(0.01*scale), pady=(0.5*scale))
    entryFrame = Frame(mainFrame, height=(3*scale), width=(10*scale))
    entryFrame.pack_propagate(0)
    entryFrame.grid(row=0, column=0, padx=(0.5*scale), pady=(0.05*scale))
    entry = Entry(entryFrame, textvariable=ebox, borderwidth=(0.25*scale),
            font=('calibri', int((2/3)*scale)), bg='lightgrey', justify='left')
    entry.anchor(SE)
    entry.pack(fill=BOTH, expand=1)
    smallBFrame = Frame(mainFrame, height=(3*scale), width=(10*scale))
    smallBFrame.pack_propagate(0)
    smallBFrame.grid(row=1, column=0)
    largeBFrame = Frame(mainFrame, height=(10*scale), width=(10*scale))
    largeBFrame.pack_propagate(0)
    largeBFrame.grid(row=2, column=0)
    ranges = [[2,5],[5,5]]
    sizes = [[2,1.5],[2,2]]  # each section has differently-sized buttons
    for type in range(2):
        for row in range(ranges[type][0]):
            for col in range(ranges[type][1]):
                text = texts[type][row][col]
                outterFrame = smallBFrame
                if type == 1: outterFrame = largeBFrame
                frames[text] = Frame(outterFrame, height=(sizes[type][1]*scale),
                                     width=(sizes[type][0]*scale))
                frames[text].pack_propagate(0)
                frames[text].grid(row=row, column=col)
                command = (partial(buttonCmd, text, ebox, entry))
                color = 'black'
                if (text.isdigit()) or (text in ['.','(-)','Enter','+','-','x',
                                                 '÷']): color = 'blue'
                buttons[text] = Button(frames[text], text=text, font=('calibri',
                    round(0.5*scale),'bold'), foreground=color, command=command,
                                       activeforeground='red')
                buttons[text].pack(fill=BOTH, expand=1)

def main(scale):
    # buttons arranged into a 3D list (sections, rows, columns)
    texts = [[['log10(','Sin(','Cos(','Tan(','rand',],['Abs(','aSin(','aCos(',
                'aTan(','Clear',]],[['ln(','^(','(',')','÷'],['√(','7','8','9',
                'x'],['π','4','5','6','-'],['e','1','2','3','+'],['!','0','.',
                '(-)','Enter']]]
    root = Tk()
    root.title('Liam\'s Calculator')
    ebox = StringVar()  # entry
    createVisuals(scale, root, ebox, texts)
    root.mainloop()

main(35)  # default scale of 35
