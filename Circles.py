import math
import tkinter
import time
import random


class Circle:
    def __init__(self, canvas, w, h, radius, r_index, c_index, scale, ranges, init_max_vel):
        self.state = 'normal'
        self.speed = 'inc'
        self.color = ('#'+('{:06x}'.format(random.randint(0, 0x1000000))))
        self.swap = ''
        # initial coordinates and velocities based on amount and window dimensions
        self.x1 = ((scale-((scale*(ranges.index(r_index)))/3))*math.cos(((2*math.pi)/r_index)*c_index))+(w/2)-radius
        self.y1 = ((scale-((scale*(ranges.index(r_index)))/3))*math.sin(((2*math.pi)/r_index)*c_index))+(h/2)-radius
        self.x2 = ((scale-((scale*(ranges.index(r_index)))/3))*math.cos(((2*math.pi)/r_index)*c_index))+(w/2)+radius
        self.y2 = ((scale-((scale*(ranges.index(r_index)))/3))*math.sin(((2*math.pi)/r_index)*c_index))+(h/2)+radius
        self.vel_x = (random.uniform(1, (1+init_max_vel))*0.5*math.cos(((2*math.pi)/r_index)*c_index))
        self.vel_y = (random.uniform(1, (1+init_max_vel))*0.5*math.sin(((2*math.pi)/r_index)*c_index))
        # respective canvas objects:
        self.literal = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=0)

    def __str__(self):  # not used but helpful for identifying circles if needed
        return f'type={self.state}; speed={self.speed}; x_velocity={self.vel_x}; y_velocity={self.vel_y}'

    def move(self, canvas):
        canvas.move(self.literal, self.vel_x, self.vel_y)


# circle creation and placement in 'rings' or layers of a larger circle that fits inside the window
def create_circles(w, h, canvas, r, c_number, circles, ranges, scale_decrease, c_index, init_max_vel):
    scale = ((2.1*c_number*r)/(2*math.pi))
    while (scale+(4*r)-(scale*scale_decrease)) >= (min(w, h))/2:
        scale_decrease += 0.1
    ranges.append(math.floor((c_number*(1-scale_decrease))))
    ranges.append(math.floor((c_number-ranges[0])*(3/5)))
    ranges.append(c_number-ranges[0]-ranges[1])
    scale *= (1-scale_decrease)
    for ring in ranges:
        if ring > 0:
            for circle in range(ring):
                circles[c_index] = Circle(canvas, w, h, r, ring, circle, scale, ranges, init_max_vel)
                c_index += 1
    return circles


def direction(x, y):  # calculates direction for a circle with or without respect to another circle
    if y == 0:
        if x > 0:
            return 0
        return math.pi
    elif x == 0:
        if y < 0:
            return math.pi/2
        return (3*math.pi)/2
    else:
        radians = math.atan(y/x)
        if (y < 0) and (x < 0):
            radians = (math.atan(abs(y)/abs(x)))+math.pi
        elif y > 0:
            radians = math.pi-(math.atan(y/abs(x)))
        elif x > 0:
            radians = (2*math.pi)-(math.atan(abs(y)/x))
    return radians


def circle_collision(c1_x, c1_y, c2_x, c2_y, c1_tmp, c2_tmp):  # calculates velocity for circle to circle collision
    c2_d_c1 = direction((c1_x-c2_x), (c1_y-c2_y))
    c2_d = direction(c2_tmp[0], c2_tmp[1])
    if (c2_d_c1-(math.pi/6)) <= c2_d <= (c2_d_c1+(math.pi/6)):
        if (math.sqrt((c1_tmp[0]**2)+(c1_tmp[1]**2))) <= (math.sqrt((c2_tmp[0]**2)+(c2_tmp[1]**2))):
            return [-(c1_tmp[0]), -(c1_tmp[1])]
        return [(c1_tmp[0]+c2_tmp[0]), (c1_tmp[1]+c2_tmp[1])]
    if (c2_d_c1-(math.pi/4)) <= c2_d <= (c2_d_c1+(math.pi/4)):
        if (math.sqrt((c1_tmp[0]**2)+(c1_tmp[1]**2))) <= (math.sqrt((c2_tmp[0]**2)+(c2_tmp[1]**2))):
            return [(c1_tmp[0]+c2_tmp[0]), (c1_tmp[1]+c2_tmp[1])]
        return [(c1_tmp[0]+(c2_tmp[0]/2)), (c1_tmp[1]+(c2_tmp[1]/2))]
    if (c2_d_c1-(math.pi/2)) < c2_d < (c2_d_c1+(math.pi/2)):
        if (math.sqrt((c1_tmp[0]**2)+(c1_tmp[1]**2))) <= (math.sqrt((c2_tmp[0]**2)+(c2_tmp[1]**2))):
            return [(c1_tmp[0]+(c2_tmp[0]/3)), (c1_tmp[1]+(c2_tmp[1]/3))]
        return [(c1_tmp[0]+(c2_tmp[0]/5)), (c1_tmp[1]+(c2_tmp[1]/5))]
    return [(c1_tmp[0]+(c2_tmp[0]/10)), (c1_tmp[1]+(c2_tmp[1]/10))]


def wall_collision(x1, y1, x2, y2, c_velocities, w, h, c_speed):  # returns velocity for circle to wall collision
    if (x2+(c_velocities[0]) >= w) or (x1+(c_velocities[0]) <= 0):
        c_velocities[0] = -c_speed*(c_velocities[0])
    if (y2+(c_velocities[1]) >= h) or (y1+(c_velocities[1]) <= 0):
        c_velocities[1] = -c_speed*(c_velocities[1])
    return c_velocities


def speed_change(vel_x, vel_y, speed, speed_key):  # reverses acceleration based on max and min velocities
    movement = math.sqrt((vel_x*vel_x)+(vel_y*vel_y))
    if movement >= speed_key[1]:
        return 'dec'
    elif (movement*0.9) <= speed_key[0]:
        return 'inc'
    return speed


def animate(window, canvas, w, h, circles, c_number, vel_config, speed_key, collision, color_swap):
    remaining = c_number
    while True:
        collision_check = []
        for c1 in range(c_number):  # calculations for all circles
            if circles[c1].state != 'none':
                c1_x1, c1_y1, c1_x2, c1_y2 = canvas.coords(circles[c1].literal)
                circles[c1].x1 = c1_x1
                circles[c1].y1 = c1_y1
                circles[c1].x2 = c1_x2
                circles[c1].y2 = c1_y2
                c1_x = (((c1_x2-c1_x1)/2)+c1_x1)+circles[c1].vel_x
                c1_y = (((c1_y2-c1_y1)/2)+c1_y1)+circles[c1].vel_y
                c1_vel_x = circles[c1].vel_x
                c1_vel_y = circles[c1].vel_y
                c1_tmp = [c1_vel_x, c1_vel_y]
                if circles[c1].state != 'bullet' and collision:  # calculations for circle collision if enabled
                    for c2 in range(c_number):
                        if circles[c2].state != 'none' and c2 != c1 and c1 not in collision_check and \
                                circles[c1].state != 'bullet':
                            c2_x1, c2_y1, c2_x2, c2_y2 = canvas.coords(circles[c2].literal)
                            c2_vel_x = circles[c2].vel_x
                            c2_vel_y = circles[c2].vel_y
                            c2_tmp = [c2_vel_x, c2_vel_y]
                            c2_x = (((c2_x2-c2_x1)/2)+c2_x1)+c2_vel_x
                            c2_y = (((c2_y2-c2_y1)/2)+c2_y1)+c2_vel_y
                            if math.sqrt(((c2_y-c1_y)**2)+((c2_x-c1_x)**2)) <= (c2_x2-c2_x1):
                                if (color_swap and circles[c1].swap) == '' and circles[c2].swap == '':
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
                                c1_collision = circle_collision(c1_x, c1_y, c2_x, c2_y, c1_tmp, c2_tmp)
                                c2_collision = circle_collision(c2_x, c2_y, c1_x, c1_y, c2_tmp, c1_tmp)
                                circles[c2].vel_x = c2_collision[0]
                                circles[c2].vel_y = c2_collision[1]
                                c1_tmp = c1_collision
                                collision_check.append(c1)
                circles[c1].speed = speed_change(c1_tmp[0], c1_tmp[1], circles[c1].speed, vel_config)
                c1_tmp = wall_collision(c1_x1, c1_y1, c1_x2, c1_y2, c1_tmp, w, h, speed_key[circles[c1].speed])
                circles[c1].vel_x = c1_tmp[0]
                circles[c1].vel_y = c1_tmp[1]
        for bullet in range(c_number):  # calculations for all bullets
            if circles[bullet].state == 'bullet':
                b_x = ((circles[bullet].x2-circles[bullet].x1)/2)+circles[bullet].x1+circles[bullet].vel_x
                b_y = ((circles[bullet].y2-circles[bullet].y1)/2)+circles[bullet].y1+circles[bullet].vel_y
                for c in range(c_number):
                    if c != bullet:
                        c_x = ((circles[c].x2-circles[c].x1)/2)+circles[c].x1+circles[c].vel_x
                        c_y = ((circles[c].y2-circles[c].y1)/2)+circles[c].y1+circles[c].vel_y
                        if circles[c].state != 'none' and (math.sqrt(((b_y-c_y)**2)+((b_x-c_x)**2))) <= (
                                circles[bullet].x2-circles[bullet].x1):
                            canvas.delete(circles[c].literal)
                            circles[c].state = 'none'
                            remaining -= 1
                            print(str(remaining)+' circles remaining')
        if color_swap and collision:
            for c in range(c_number):
                circles[c].swap = ''
        # all circles are moved and the window is updated
        for c in range(c_number):
            if circles[c].state != 'none':
                circles[c].move(canvas)
        window.update()
        time.sleep(0.0000000000001)


def main(w, h, fill, c_number, b_number, acceleration, collision, color_swap, vel_config, bg):
    window = tkinter.Tk()
    window.title('CIRCLES')
    window.geometry(f'{w}x{h}')
    canvas = tkinter.Canvas(window)
    canvas.configure(bg=bg)
    canvas.pack(fill='both', expand=True)
    circles = create_circles(w, h, canvas, (round((math.sqrt((w*h)/((c_number*math.pi)/fill))), 2)),
                             c_number, {}, [], 0, 0, vel_config[0])
    if c_number > 150:
        collision = False
    if c_number > 1000:
        b_number = 0
    bullets = 0
    while bullets < b_number:
        bullet = random.randint(0, (c_number-1))
        if circles[bullet].state != 'bullet':
            circles[bullet].state = 'bullet'
            bullets += 1
    animate(window, canvas, w, h, circles, c_number, vel_config[1:],
            {'inc': (1.1*acceleration), 'dec': (0.9*acceleration)}, collision, color_swap)


dimensions = [700, 700]  # width and height
main(dimensions[0], dimensions[1],
     0.005,  # the proportion of the screen filled by circles
     random.randint(15, 100),  # the number of circles
     random.randint(0, 3),  # the number of bullets
     1,  # the scale applied to positive and negative acceleration for all circles
     True,  # whether circles collide with each other (not recommended for higher numbers)
     True,  # whether colliding circles swap colors (requires collision ^)
     [9,  # maximum initial velocity for all circles
      5,  # minimum velocity for all circles
      (min(dimensions[0], dimensions[1])/2)],  # maximum velocity for all circles
     'white')  # background color
