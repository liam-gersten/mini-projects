from math import *
import tkinter, time


# object for the main rectangle of a disk
class Disk:
    def __init__(self, canvas, disk, diskHeight, trueHeight, base, xPeg, color):
        self.y2 = base-(disk*diskHeight)
        self.y1 = self.y2-diskHeight
        self.x2 = xPeg+((trueHeight-(disk*diskHeight))/2)
        self.x1 = xPeg-((trueHeight-(disk*diskHeight))/2)
        self.literal = canvas.create_rectangle(self.x1, self.y1, self.x2,
                                               self.y2, fill=color,
                                               outline=color)

    def move(self, canvas, xAmount, yAmount):
        canvas.move(self.literal, xAmount, yAmount)

    # performed after most moves
    def updateCoords(self, xTransform, yTransform):
        self.x1 += xTransform
        self.x2 += xTransform
        self.y1 += yTransform
        self.y2 += yTransform


# objects for upper and lower circles that accompany the rectangle of a disk
class Circle:
    def __init__(self, canvas, disk, side, color):
        circleHeight = (disk.x2-disk.x1)/(2*pi)
        self.x1 = disk.x1
        self.x2 = disk.x2
        self.y1 = disk.y2-circleHeight
        self.y2 = disk.y2+circleHeight
        if side == 'top':
            self.y1 = disk.y1-circleHeight
            self.y2 = disk.y1+circleHeight
        self.color = color
        self.literal = canvas.create_oval(self.x1, self.y1, self.x2,
                                          self.y2, fill=self.color,
                                          outline=self.color)

    def move(self, canvas, xAmount, yAmount):
        canvas.move(self.literal, xAmount, yAmount)


# moves three objects, updates coords, and sleeps for a given disk
def move(disks, disk, circles, canvas, xMove, yMove, frames, speed):
    disks[disk].move(canvas, xMove, yMove)
    circles[disk]['bottom'].move(canvas, xMove, yMove)
    circles[disk]['top'].move(canvas, xMove, yMove)
    disks[disk].updateCoords(xMove, yMove)
    time.sleep((1/frames)/speed)


# finds where a disk should be post-animation and returns the difference
def findError(disks, diskA, peg, xPeg, pegBase):
    xA = ((disks[diskA].x2-disks[diskA].x1)/2)+disks[diskA].x1
    yA = disks[diskA].y2
    xB = xPeg
    yB = pegBase
    if peg: yB = disks[peg[-1]].y1
    return [(xB-xA), (yB-yA)]


# dict that contains sequential move distances for a circular animation
def makeCircleDict(frames, radius):
    moves = {}
    for i in range(0, frames+1): moves[i] = {'θ': (pi*(i/frames))}
    for i in range(frames):
        moves[i]['xMove'] = (radius*(cos(moves[i+1]['θ'])-cos(moves[i]['θ'])))
        moves[i]['yMove'] = -(radius*(sin(moves[i+1]['θ'])-sin(moves[i]['θ'])))
    return moves


# recursively tests for a legal move from a to b or from b to a
def tryMove(pegs, a, b):
    if not pegs[a]: return tryMove(pegs, b, a)
    for disk in pegs[b]:
        # legal if the disk bellow is larger
        if disk > pegs[a][-1]: return tryMove(pegs, b, a)
    return [a, b]


# animates the movement of one disk from peg a to peg b (ints between 0 and 2)
def animateDisk(canvas, window, disks, circles, pegs, cDicts, cFrames, a, b,
                direction, frames, speed, pegHeight, disk, diskHeight):
    aLength = (pegHeight-(len(pegs[a])*diskHeight))
    bLength = (pegHeight-(len(pegs[b])*diskHeight))
    abLength = aLength+bLength
    abFrames = frames-cFrames
    aFrames = int(ceil(abFrames*(aLength/abLength)))
    bFrames = frames-cFrames-aFrames
    for frame in range(aFrames):  # moving up off of origin peg a
        move(disks, disk, circles, canvas, 0, -(aLength/aFrames), frames, speed)
        window.update()
    size = 'small'  # default
    if abs(b-a) == 2: size = 'large'  # jumps distance of 2 pegs
    [lowerFrame, upperFrame, loopMovement] = [0, cFrames, 1]  # default
    if direction < 0:
        # opposite direction reverse iterates through the circleDict
        [lowerFrame, upperFrame, loopMovement] = [cFrames-1, -1, -1]
    # circular movement (jumping from peg a to peg b)
    for frame in range(lowerFrame, upperFrame, loopMovement):
        xMove = direction*cDicts[size][frame]['xMove']
        yMove = direction*cDicts[size][frame]['yMove']
        if size == 'large':  # stops the disk from jumping too far up off screen
            yMove *= (3/4)
        move(disks, disk, circles, canvas, xMove, yMove, frames, speed)
        window.update()
    for frame in range(bFrames-1):  # moving down into destination peg b
        move(disks, disk, circles, canvas, 0, (bLength/bFrames), frames, speed)
        window.update()


# iteratively solves towers of hanoi and animates along the way
def solve(canvas, window, disks, circles, pegs, xPegs, pegBase, speed,
              pegHeight, diskHeight, fps):
    [i, frames] = [0, int(ceil(fps/speed))]
    sequence = [[0, 2], [0, 1], [1, 2]]  # default solution algorithm
    if len(disks) % 2 == 0: sequence = [[0, 1], [0, 2], [1, 2]]  # alternate
    circleFrames = int(frames*(2/3))  # frames dedicated to circular animation
    circleDicts = {'large': makeCircleDict(circleFrames, (xPegs[2]-xPegs[0])/2),
                   'small': makeCircleDict(circleFrames, (xPegs[1]-xPegs[0])/2)}
    while (pegs[0] != []) or (pegs[1] != []):
        direction = -1
        [a, b] = tryMove(pegs, sequence[i][0], sequence[i][1])
        if b < a: direction = 1
        disk = pegs[a][-1]
        animateDisk(canvas, window, disks, circles, pegs, circleDicts,
                    circleFrames, a, b, direction, frames, speed, pegHeight,
                    disk, diskHeight)
        [xMove, yMove] = findError(disks, disk, pegs[b], xPegs[b], pegBase)
        move(disks, disk, circles, canvas, xMove, yMove, frames, speed)
        window.update()
        # edits lists to reflect change shown in animation
        tmp = pegs[a].pop()
        pegs[b] += [tmp]
        i += 1
        if i == 3: i = 0


# sets up canvas, fixed coords/lengths, and several dictionaries
def main(diskNum, speed, fps, colors):
    window = tkinter.Tk()
    window.title('Towers of Hanoi')
    window.geometry(f'{1440}x{750}')
    canvas = tkinter.Canvas(window)
    canvas.configure(bg='white')
    canvas.pack(fill='both', expand=True)
    [pegBase, pegHeight] = [665, 400]
    xPegs = [290, 720, 1150]  # middle x-locations of pegs 0, 1, and, 2
    diskHeight = round(pegHeight/(diskNum+1))
    [disks, circles, pegs] = [{}, {}, [[], [], []]]  # empty variable creation
    for i in range(3):  # peg creation
        pColors = ['#494949', '#848484']  # default colors: grey and light grey
        # should be the same width as the largest disk (uses same formula)
        [x1, x2] = [xPegs[i]-(pegHeight/2), xPegs[i]+(pegHeight/2)]
        height = (x2-x1)/(2*pi)
        [y1, y2] = [pegBase-height, pegBase+height]
        if i == 2: pColors = ['#fec619', 'gold']  # gold colors for final peg
        canvas.create_rectangle(x1, pegBase, x2, 750, fill=pColors[0],
                                outline=pColors[0])
        canvas.create_oval(x1, y1, x2, y2, fill=pColors[1], outline=pColors[1])
    for disk in range(0, diskNum):  # disk creation with 3 objects
        if disk >= len(colors): dColors = colors[int(disk % len(colors))]
        else: dColors = colors[disk]
        disks[disk] = Disk(canvas, disk, diskHeight, pegHeight, pegBase,
                           xPegs[0], dColors[0])
        circles[disk] = {'bottom': Circle(canvas, disks[disk], 'bottom',
                                          dColors[0])}
        circles[disk]['top'] = Circle(canvas, disks[disk], 'top', dColors[1])
    # list creation to help with solving
    for disk in range(0, diskNum): pegs[0] += [disk]
    solve(canvas, window, disks, circles, pegs, xPegs, pegBase, speed,
                    pegHeight, diskHeight, fps)  # includes animation
    canvas.destroy()
    window.destroy()


frameRate = 100  # larger framerates will significantly slow down animation
speed = 5
minDisks = 10  # must be an int
maxDisks = 20  # must be an int
colors = {0: {0: '#FF0E0E', 1: '#FE4C4C'}, 1: {0: '#FF880A', 1: '#FFA749'},
          2: {0: '#FFF000', 1: '#FFF779'}, 3: {0: '#49FF00', 1: '#91FF65'},
          4: {0: '#00FF7C', 1: '#8FFFC6'}, 5: {0: '#00FFE0', 1: '#9EFFF3'},
          6: {0: '#00ABFF', 1: '#69CDFF'}, 7: {0: '#0C00FF', 1: '#574FFF'},
          8: {0: '#6B00FC', 1: '#A35FFF'}, 9: {0: '#A200FF', 1: '#CA6FFF'},
          10: {0: '#FF00F7', 1: '#FF65FA'}, 11: {0: '#FF0083', 1: '#FF60B2'},
          12: {0: '#950C0C', 1: '#B74F4F'}, 13: {0: '#977300', 1: '#BEA452'}}
for disks in range(minDisks, maxDisks):  # optional for loop (10 runs)
    main(disks, speed, frameRate, colors)
