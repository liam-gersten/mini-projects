import math
import tkinter
import time
import random


class Circle:
    def __init__(self, canvas, w, h, radius, rIndex, cIndex, scale, ranges, initMaxVel):
        self.state = 'normal'  # is not a bullet
        self.speed = 'inc'  # starts speeding up
        self.color = ('#'+('{:06x}'.format(random.randint(0, 0x1000000))))
        self.swap = ''
        # coordinates and velocities based on amount and window dimensions
        self.x1 = ((scale-((scale*(ranges.index(rIndex)))/3))*math.cos(((2*math.pi)/rIndex)*cIndex))+(w/2)-radius
        self.y1 = ((scale-((scale*(ranges.index(rIndex)))/3))*math.sin(((2*math.pi)/rIndex)*cIndex))+(h/2)-radius
        self.x2 = ((scale-((scale*(ranges.index(rIndex)))/3))*math.cos(((2*math.pi)/rIndex)*cIndex))+(w/2)+radius
        self.y2 = ((scale-((scale*(ranges.index(rIndex)))/3))*math.sin(((2*math.pi)/rIndex)*cIndex))+(h/2)+radius
        self.velX = (random.uniform(1, (1+initMaxVel))*0.5*math.cos(((2*math.pi)/rIndex)*cIndex))
        self.velY = (random.uniform(1, (1+initMaxVel))*0.5*math.sin(((2*math.pi)/rIndex)*cIndex))
        # respective canvas objects:
        self.literal = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=0)

    def __str__(self):  # not used but helpful for identifying circles during debugging
        return f'type={self.state}; speed={self.speed}; xVelocity={self.velX}; yVelocity={self.velY}'

    def move(self, canvas):
        canvas.move(self.literal, self.velX, self.velY)


# circle creation and placement in 'rings' or layers of a larger circle that fits inside the window
def createCirlces(w, h, canvas, r, circleNum, circles, ranges, scaleDecrease, cIndex, initMaxVel):
    scale = ((2.1*circleNum*r)/(2*math.pi))
    while (scale+(4*r)-(scale*scaleDecrease)) >= (min(w, h))/2:
        scaleDecrease += 0.1
    ranges.append(math.floor((circleNum*(1-scaleDecrease))))
    ranges.append(math.floor((circleNum-ranges[0])*(3/5)))
    ranges.append(circleNum-ranges[0]-ranges[1])
    scale *= (1-scaleDecrease)
    for ring in ranges:
        if ring > 0:
            for circle in range(ring):
                circles[cIndex] = Circle(canvas, w, h, r, ring, circle, scale, ranges, initMaxVel)
                cIndex += 1
    return circles


def direction(x, y):  # calculates direction for a circle with or without respect to another circle
    if y == 0:
        if x > 0: return 0
        return math.pi
    elif x == 0:
        if y < 0: return math.pi/2
        return (3*math.pi)/2
    else:
        radians = math.atan(y/x)
        if (y < 0) and (x < 0): radians = (math.atan(abs(y)/abs(x)))+math.pi
        elif y > 0: radians = math.pi-(math.atan(y/abs(x)))
        elif x > 0: radians = (2*math.pi)-(math.atan(abs(y)/x))
    return radians


def circleCollision(c1X, c1Y, c2X, c2Y, c1Tmp, c2Tmp):
    # calculates new velocities for circle to circle collision
    c2DC1 = direction((c1X-c2X), (c1Y-c2Y))
    c2D = direction(c2Tmp[0], c2Tmp[1])
    if (c2DC1-(math.pi/6)) <= c2D <= (c2DC1+(math.pi/6)):
        if (math.sqrt((c1Tmp[0]**2)+(c1Tmp[1]**2))) <= (math.sqrt((c2Tmp[0]**2)+(c2Tmp[1]**2))):
            return [-(c1Tmp[0]), -(c1Tmp[1])]
        return [(c1Tmp[0]+c2Tmp[0]), (c1Tmp[1]+c2Tmp[1])]
    if (c2DC1-(math.pi/4)) <= c2D <= (c2DC1+(math.pi/4)):
        if (math.sqrt((c1Tmp[0]**2)+(c1Tmp[1]**2))) <= (math.sqrt((c2Tmp[0]**2)+(c2Tmp[1]**2))):
            return [(c1Tmp[0]+c2Tmp[0]), (c1Tmp[1]+c2Tmp[1])]
        return [(c1Tmp[0]+(c2Tmp[0]/2)), (c1Tmp[1]+(c2Tmp[1]/2))]
    if (c2DC1-(math.pi/2)) < c2D < (c2DC1+(math.pi/2)):
        if (math.sqrt((c1Tmp[0]**2)+(c1Tmp[1]**2))) <= (math.sqrt((c2Tmp[0]**2)+(c2Tmp[1]**2))):
            return [(c1Tmp[0]+(c2Tmp[0]/3)), (c1Tmp[1]+(c2Tmp[1]/3))]
        return [(c1Tmp[0]+(c2Tmp[0]/5)), (c1Tmp[1]+(c2Tmp[1]/5))]
    return [(c1Tmp[0]+(c2Tmp[0]/10)), (c1Tmp[1]+(c2Tmp[1]/10))]


# returns velocity for circle to wall collision
def wallCollision(x1, y1, x2, y2, cVelocities, w, h, cSpeed):
    if (x2+(cVelocities[0]) >= w) or (x1+(cVelocities[0]) <= 0):
        cVelocities[0] = -cSpeed*(cVelocities[0])
    if (y2+(cVelocities[1]) >= h) or (y1+(cVelocities[1]) <= 0):
        cVelocities[1] = -cSpeed*(cVelocities[1])
    return cVelocities


# reverses acceleration based on max and min velocities
def speedChange(velX, velY, speed, speedKey):
    movement = math.sqrt((velX*velX)+(velY*velY))
    if movement >= speedKey[1]: return 'dec'
    elif (movement*0.9) <= speedKey[0]: return 'inc'
    return speed


def animate(window, canvas, w, h, circles, circleNum, velConfig, speedKey, collision, colorSwap):
    remaining = circleNum
    while True:
        collisionCheck = []
        for c1 in range(circleNum):  # calculations for all circles
            if circles[c1].state != 'none':
                c1X1, c1Y1, c1X2, c1Y2 = canvas.coords(circles[c1].literal)
                circles[c1].x1 = c1X1
                circles[c1].y1 = c1Y1
                circles[c1].x2 = c1X2
                circles[c1].y2 = c1Y2
                c1X = (((c1X2-c1X1)/2)+c1X1)+circles[c1].velX
                c1Y = (((c1Y2-c1Y1)/2)+c1Y1)+circles[c1].velY
                c1VelX = circles[c1].velX
                c1VelY = circles[c1].velY
                c1Tmp = [c1VelX, c1VelY]
                if circles[c1].state != 'bullet' and collision:  # calculations for circle collision if enabled
                    for c2 in range(circleNum):
                        if circles[c2].state != 'none' and c2 != c1 and c1 not in collisionCheck and \
                                circles[c1].state != 'bullet':
                            c2X1, c2Y1, c2X2, c2Y2 = canvas.coords(circles[c2].literal)
                            c2VelX = circles[c2].velX
                            c2VelY = circles[c2].velY
                            c2Tmp = [c2VelX, c2VelY]
                            c2X = (((c2X2-c2X1)/2)+c2X1)+c2VelX
                            c2Y = (((c2Y2-c2Y1)/2)+c2Y1)+c2VelY
                            if math.sqrt(((c2Y-c1Y)**2)+((c2X-c1X)**2)) <= (c2X2-c2X1):
                                if (colorSwap and circles[c1].swap) == '' and circles[c2].swap == '':
                                    circles[c1].swap = (circles[c2].color+'')  # alias breaking
                                    circles[c2].swap = (circles[c1].color+'')
                                    circles[c1].color = (circles[c1].swap+'')
                                    circles[c2].color = (circles[c2].swap+'')
                                    canvas.delete(circles[c1].literal)
                                    canvas.delete(circles[c2].literal)
                                    circles[c1].literal = canvas.create_oval(circles[c1].x1, circles[c1].y1,
                                                                             circles[c1].x2, circles[c1].y2,
                                                                             fill=circles[c1].color, width=0)
                                    circles[c2].literal = canvas.create_oval(circles[c2].x1, circles[c2].y1,
                                                                             circles[c2].x2, circles[c2].y2,
                                                                             fill=circles[c2].color, width=0)
                                c1Collision = circleCollision(c1X, c1Y, c2X, c2Y, c1Tmp, c2Tmp)
                                c2Collision = circleCollision(c2X, c2Y, c1X, c1Y, c2Tmp, c1Tmp)
                                circles[c2].velX = c2Collision[0]
                                circles[c2].velY = c2Collision[1]
                                c1Tmp = c1Collision
                                collisionCheck.append(c1)
                circles[c1].speed = speedChange(c1Tmp[0], c1Tmp[1], circles[c1].speed, velConfig)
                c1Tmp = wallCollision(c1X1, c1Y1, c1X2, c1Y2, c1Tmp, w, h, speedKey[circles[c1].speed])
                circles[c1].velX = c1Tmp[0]
                circles[c1].velY = c1Tmp[1]
        for bullet in range(circleNum):  # calculations for all bullets
            if circles[bullet].state == 'bullet':
                bX = ((circles[bullet].x2-circles[bullet].x1)/2)+circles[bullet].x1+circles[bullet].velX
                bY = ((circles[bullet].y2-circles[bullet].y1)/2)+circles[bullet].y1+circles[bullet].velY
                for c in range(circleNum):
                    if c != bullet:
                        cX = ((circles[c].x2-circles[c].x1)/2)+circles[c].x1+circles[c].velX
                        cY = ((circles[c].y2-circles[c].y1)/2)+circles[c].y1+circles[c].velY
                        if circles[c].state != 'none' and (math.sqrt(((bY-cY)**2)+((bX-cX)**2))) <= (
                                circles[bullet].x2-circles[bullet].x1):
                            canvas.delete(circles[c].literal)
                            circles[c].state = 'none'
                            remaining -= 1
                            print(str(remaining)+' circles remaining')
        if colorSwap and collision:
            for c in range(circleNum): circles[c].swap = ''
        # all circles are moved and the window is updated
        for c in range(circleNum):
            if circles[c].state != 'none': circles[c].move(canvas)
        window.update()
        time.sleep(0.0000000000001)


def main(w, h, fill, circleNum, bNum, acceleration, collision, colorSwap, velConfig, bg):
    window = tkinter.Tk()
    window.title('CIRCLES')
    window.geometry(f'{w}x{h}')
    canvas = tkinter.Canvas(window)
    canvas.configure(bg=bg)
    canvas.pack(fill='both', expand=True)
    circles = createCirlces(w, h, canvas, (round((math.sqrt((w*h)/((circleNum*math.pi)/fill))), 2)),
                            circleNum, {}, [], 0, 0, velConfig[0])
    if circleNum > 150: collision = False
    if circleNum > 1000: bNum = 0
    bullets = 0
    while bullets < bNum:
        bullet = random.randint(0, (circleNum-1))
        if circles[bullet].state != 'bullet':
            circles[bullet].state = 'bullet'
            bullets += 1
    animate(window, canvas, w, h, circles, circleNum, velConfig[1:],
            {'inc': (1.1*acceleration), 'dec': (0.9*acceleration)}, collision, colorSwap)


dimensions = [1440, 720]  # width and height
main(dimensions[0], dimensions[1],
     0.005,  # the proportion of the screen filled by circles
     random.randint(15, 1000),  # the number of circles
     random.randint(1, 5),  # the number of bullets
     1,  # the scale applied to positive and negative acceleration for all circles
     True,  # whether circles collide with each other (not recommended for higher numbers)
     True,  # whether colliding circles swap colors (requires collision ^)
     [9,  # maximum initial velocity for all circles
      5,  # minimum velocity for all circles
      (min(dimensions[0], dimensions[1])/2)],  # maximum velocity for all circles
     'white')  # background color
