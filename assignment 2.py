from OpenGL.GL import *   
from OpenGL.GLUT import *   
from OpenGL.GLU import *  
import random
import time

window_width = 400
window_height = 500
cheat = False
xdi = random.randint(1, 380) 
current_diamond = []
d_color = [255, 230, 0]
y0 = 455
y1 = 470
y2 = 455
y3 = 440
speed = 90  
past = time.time()  
score = 0
game_over = False
catcher_width = 80
catcher_x = 0
paused=False
mcatch = 10

def color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)

def convert_coordinate(x, y):
    return x, window_height - y

def diamond():
    global current_diamond, d_color,xdi
    if y3 == 440: 
        d_color[0] = random.randint(0, 255)
        d_color[1] = random.randint(0, 255)
        d_color[2] = random.randint(0, 255)

    d1 = zone(0+xdi, y0, 10+xdi, y1)
    d2 = zone(10+xdi, y1, 20+xdi, y2)
    d3 = zone(20+xdi, y2, 10+xdi, y3)
    d4 = zone(10+xdi, y3, 0+xdi, y0)

    current_diamond = d1 + d2 + d3 + d4

def animate():
    global y0, y1, y2, y3, xdi, past, speed
    global catcher_x, catcher_width, score, game_over,cheat

    if game_over or paused:
        past=time.time()
        return  

    present = time.time()
    dt = present - past
    past = present

    y0 -= speed* dt
    y1-= speed * dt
    y2 -= speed * dt
    y3 -=speed * dt

    if cheat:
        target_x = xdi + 10 - catcher_width / 2  
        if catcher_x < target_x:
            catcher_x += speed * dt  
            if catcher_x > target_x:
                catcher_x = target_x
        elif catcher_x > target_x:
            catcher_x -= speed * dt 
            if catcher_x < target_x:
                catcher_x = target_x
    if catcher_x < 0:
        catcher_x = 0
    elif catcher_x > window_width - catcher_width:
        catcher_x = window_width - catcher_width            

    catcher_box = AABB(catcher_x, 0, catcher_width, 30)
    diamond_box = AABB(xdi, y3, 20, 30)
    if hasCollided(diamond_box, catcher_box):
        score += 1
        print("Score:", score)
        speed += 30
        if speed > 200:
           speed = 200        
        y0, y1, y2, y3 = 455, 470, 455, 440
        xdi = random.randint(1, window_width - 20)

    if y3 <= 0:
        print("Game Over! Final Score:", score)
        game_over = True
        y0, y1, y2, y3 = 455, 470, 455, 440
    diamond()
    glutPostRedisplay()

def catcher():
    if game_over:
        color(255, 0, 0) 
    else:
        color(91, 153, 212)       
    global catcher_x 
    c1 = zone(0 + catcher_x, 30 , 80 + catcher_x, 30)
    c2 = zone(80 + catcher_x, 30 , 70 + catcher_x, 0)
    c3 = zone(70 + catcher_x, 0 , 10 + catcher_x, 0)
    c4 = zone(10 + catcher_x, 0 , 0 + catcher_x, 30)
 
def mouse_listener(button, state, x, y):
    global y0, y1, y2, y3, xdi, score, speed, game_over, catcher_x, paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mousex, mousey = convert_coordinate(x, y)  

        if 10 <= mousex <= 40 and 455 <= mousey <= 485:
            print("Starting Over")
            score = 0
            speed = 100     
            y0, y1, y2, y3 = 516, 531, 516, 501  
            xdi = random.randint(1, window_width - 20)
            game_over =False
            catcher_x = 0     

        elif 180 <= mousex <= 210 and 455 <= mousey <= 485:
            paused = not paused
            if paused:
                print("Paused")
            else:
                print("Resumed")


        elif 365 <= mousex <= 390 and 455 <= mousey <= 485:
            print(f"Goodbye! Your score: {score}")
            glutLeaveMainLoop()

def special_key_listener(key, x, y):
    global catcher_x,mcatch
 
    if paused or game_over:
        return
    if key == GLUT_KEY_LEFT:
        catcher_x -= mcatch
        if catcher_x < 0:
            catcher_x = 1

    if key == GLUT_KEY_RIGHT:
        catcher_x += mcatch
        if catcher_x > window_width - catcher_width:
            catcher_x = window_width - catcher_width

    glutPostRedisplay()
      #3topbuttons
def restart():
    r1=zone(10,470,40,470)
    r2=zone(10, 470, 18, 485)
    r3=zone(10, 470, 18, 455)

def pause():    
    if paused:
        p1 = zone(180, 455, 180, 485)
        p2 = zone(180, 485, 210, 470)
        p3 = zone(210, 470, 180, 455)
    else:
        p1 = zone(190, 455, 190, 485)
        p2 = zone(210, 455, 210, 485)
def exit():
    e1=zone(365,485,390,455)
    e2=zone(365,455,390,485)        


#extra

def keyboard_listener(key, x, y):
    global cheat, speed,mcatch 
    if key == b'c':
        cheat= not cheat
        if cheat:
            print("Cheat mode:on")
        else:
            print("Cheat Mode:off")   
    if cheat:
        return        
    if key == b'w': #catcher
        mcatch += 2
        if mcatch > 25:
            mcatch = 25

    if key == b's':
        mcatch -= 2
        if mcatch < 4:
            mcatch = 4
               #diamond
    if key == b'd':
        speed += 5
        if speed > 200:   
            speed = 200
    if key == b'a':
        speed -= 5
        if speed < 40:   
            speed = 40            
#mainmpl


def DrawLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    adx = abs(dx)
    ady = abs(dy)
    points = []

    if adx >= ady:
        d = 2*ady - adx       
        incE = 2*ady           
        incNE = 2*(ady - adx)  
        x = x1
        y = y1
        x_end = x2
        if dx > 0:
            step_x = 1
        else:
            step_x = -1

        if dy > 0:
            step_y = 1
        else:
            step_y = -1

        while x != x_end + step_x:  
            points.append((x, y))
            if d > 0:
                y += step_y
                d += incNE
            else:
                d += incE
            x += step_x
    else:
        d = 2*adx - ady
        incE = 2*adx
        incNE = 2*(adx - ady)
        x = x1
        y = y1
        y_end = y2
        if dx > 0:
            step_x= 1
        else:
            step_x= -1

        if dy > 0:
            step_y =1
        else:
            step_y =-1
        while y != y_end + step_y:
            points.append((x, y))
            if d > 0:
                x += step_x
                d += incNE
            else:
                d += incE
            y += step_y

    return points


def pixelline(xylist):
    glBegin(GL_POINTS)
    for point in xylist:
        glVertex2i(int(point[0]), int(point[1]))
    glEnd()

def zone(x1, y1, x2, y2):
    xylist = FindZone(x1, y1, x2, y2)
    pixelline(xylist)
    return xylist

def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy) and dx >= 0 and dy >= 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dy) > abs(dx) and dx >= 0 and dy >= 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dy) > abs(dx) and dx < 0 and dy >= 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dx) >= abs(dy) and dx < 0 and dy >= 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dx) >= abs(dy) and dx < 0 and dy < 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dy) > abs(dx) and dx < 0 and dy < 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dy) > abs(dx) and dx >= 0 and dy < 0:  
      return DrawLine(x1, y1, x2, y2)
    elif abs(dx) >= abs(dy) and dx >= 0 and dy < 0:  
      return DrawLine(x1, y1, x2, y2)

class AABB:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def hasCollided(box1, box2):
    return (box1.x < box2.x + box2.width and
            box1.x + box1.width > box2.x and
            box1.y < box2.y + box2.height and
            box1.y + box1.height > box2.y)
catcher_box = AABB(catcher_x, 0, catcher_width, 30)  
diamond_box = AABB(xdi, y3, 20, 30)  
if hasCollided(diamond_box, catcher_box):
    score += 1
    print("Score:", score)      

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    catcher()
    glPointSize(2)    
    global current_diamond
    color(d_color[0], d_color[1], d_color[2])
    pixelline(current_diamond)
    color(91, 153, 212)    
    restart()
    color(227,239,125)
    pause()
    color(255, 3, 2)  
    exit()
    glutSwapBuffers()

def setup_projection():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"catcher")
    setup_projection()  
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener) 
    glutKeyboardFunc(keyboard_listener)   
    glutMainLoop()


if __name__ == "__main__":
    main()


