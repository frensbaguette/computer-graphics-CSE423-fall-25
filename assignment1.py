########assignment1 task1################
from OpenGL.GL import *   
from OpenGL.GLUT import *   
from OpenGL.GLU import *  
import math


def main():
    glutInit()                               
    glutInitDisplayMode(GLUT_RGBA)          
    glutInitWindowSize(500, 500)             
    glutInitWindowPosition(0, 0)             
    glutCreateWindow(b"rainy")     
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutKeyboardFunc(keyboard_listener)                               
    glutMainLoop()                              

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()                                    
    setup_projection()                                                           
    draw_bg()
    draw_house()
    rain(gap_a,gap_b)                                       
    glutSwapBuffers()  

def setup_projection():
    glViewport(0, 0, 500, 500)     
    glMatrixMode(GL_PROJECTION)    
    glLoadIdentity()              
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)  
    glMatrixMode(GL_MODELVIEW)   

def color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)
c,c1,c2=0,0,0
def draw_bg(): #sky,3land,shrubs
    global c,c1,c2     
    color(c,c1,c2)    #sky
    glBegin(GL_QUADS)
    glVertex2d(0, 0)
    glVertex2d(0, 500)
    glVertex2d(500, 500)
    glVertex2d(500, 0)
    glEnd()
    color(111, 78, 55)  #land  
    glBegin(GL_TRIANGLES)          
    glVertex2d(0, 0)      
    glVertex2d(250, 240)
    glVertex2d(500, 0)          
    glEnd()             
    color(111, 78, 55)
    glBegin(GL_TRIANGLES)          
    glVertex2d(0, 0)      
    glVertex2d(0, 240)
    glVertex2d(250, 240)          
    glEnd()
    color(111, 78, 55)          
    glBegin(GL_TRIANGLES)          
    glVertex2d(250, 240)      
    glVertex2d(500, 240)
    glVertex2d(500, 0)          
    glEnd()
    
    glBegin(GL_TRIANGLES)   #shrubs
    above=170
    top=220
    width=40
    for i in range(500//width+1):
      start=i*width
      color(50,205,50)
      glVertex2d(start, above)
      color(0,128,128)
      glVertex2d(start+(width//2), top)
      color(50,205,50)
      glVertex2d(start+width, above)
    glEnd()                   

def draw_house():#3roof,3house,2door,2+2window
    color(175,133,49)     #roof     
    glBegin(GL_TRIANGLES)          
    glVertex2d(120, 250)      
    glVertex2d(250, 100)
    glVertex2d(380, 250)          
    glEnd()
    color(175,133,49)         
    glBegin(GL_TRIANGLES)          
    glVertex2d(380, 250)      
    glVertex2d(320, 200)
    glVertex2d(410, 200)          
    glEnd()
    color(175,133,49)        
    glBegin(GL_TRIANGLES)          
    glVertex2d(120, 250)      
    glVertex2d(200, 200)
    glVertex2d(90, 200)          
    glEnd()              
    color(222,184,135)       #HOUSE   
    glBegin(GL_TRIANGLES)          
    glVertex2d(100, 200)      
    glVertex2d(250, 100)
    glVertex2d(400, 200)          
    glEnd()
    color(222,184,135)
    glBegin(GL_TRIANGLES)          
    glVertex2d(100, 200)      
    glVertex2d(250, 100)
    glVertex2d(80, 100)          
    glEnd()
    color(222,184,135)          
    glBegin(GL_TRIANGLES)          
    glVertex2d(400, 200)      
    glVertex2d(250, 100)
    glVertex2d(420, 100)          
    glEnd()
    color(205,133,63)  #door
    glBegin(GL_TRIANGLES)          
    glVertex2d(230, 160)      
    glVertex2d(230, 100)
    glVertex2d(270, 100)          
    glEnd()
    color(205,133,63)
    glBegin(GL_TRIANGLES)          
    glVertex2d(270, 100)      
    glVertex2d(270, 160)
    glVertex2d(230, 160)          
    glEnd()
    #doorknob        
    color(255,215,0)   
    glPointSize(5)         
    glBegin(GL_POINTS)      
    glVertex2f(263, 135)           
    glEnd()    
    color(123,104,238) #window
    glBegin(GL_TRIANGLES)          
    glVertex2d(200, 150)      
    glVertex2d(200, 170)
    glVertex2d(150, 150)          
    glEnd()
    color(106,90,205)          
    glBegin(GL_TRIANGLES)          
    glVertex2d(200, 170)      
    glVertex2d(150, 150)
    glVertex2d(150, 170)          
    glEnd()
    color(123,104,238)
    glBegin(GL_TRIANGLES)          
    glVertex2d(310, 150)      
    glVertex2d(310, 170)
    glVertex2d(360, 150)          
    glEnd()
    color(106,90,205)
    glBegin(GL_TRIANGLES)          
    glVertex2d(310, 170)      
    glVertex2d(360, 150)
    glVertex2d(360, 170)          
    glEnd()

tilt=0

def rain(gap_a,gap_b):
    global tilt
    color(83, 221, 230)
    glLineWidth(2)     
    glBegin(GL_LINES)
    for x in range(0,500,20):
        glVertex2f(x, 500-gap_a)
        glVertex2f(x+tilt,480-gap_a)
    glEnd()
    glLineWidth(2)         
    color(10, 49, 207)
    glBegin(GL_LINES)        
    for x in range(0,500,15):
        glVertex2f(x, 500-gap_b)
        glVertex2f(x+tilt,475-gap_b)    
    glEnd()

gap_a=0
gap_b=0
def animate():
    global gap_a,gap_b
    gap_a=(gap_a+.5)%500
    gap_b=(gap_b+.3)%500
    glutPostRedisplay()


def special_key_listener(key, x, y):
    global tilt
    if key == GLUT_KEY_LEFT:
        if tilt<=-10:
            tilt=-10
            print("max left")
        else:    
            tilt-=5
            print("left")            
    elif key == GLUT_KEY_RIGHT:
        if tilt>=10:
            tilt=10
            print("max right")
        else:    
            tilt+=5
            print("right")    
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global c,c1,c2
    if key == b'n':
        if c<=0 and c1<=0 and c2<=0:            
            c,c1,c2=0,0,0
            print("max night")
        elif c>0 and c>0 and c>0:      
            c -=64 
            c1 -=64 
            c2 -=64 
            print("night")                               
    elif key == b'd': 
        if c>=255 and c1>=255 and c2>=255:            
            c,c1,c2=255,255,255
            print("max day")
        elif c<255 and c<255 and c<255:      
            c +=64 
            c1 +=64 
            c2 +=64 
            print("day") 
    glutPostRedisplay()

if __name__ == "__main__":
    main()    





########assignment1 task2################


from OpenGL.GL import *   
from OpenGL.GLUT import *   
from OpenGL.GLU import *  
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
ball_size = 10
ball_speed = 0.1
blink=False
stop=False
og_color=[]
balls = []

def main():
    glutInit()                               
    glutInitDisplayMode(GLUT_RGBA)          
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)             
    glutInitWindowPosition(0, 0)             
    glutCreateWindow(b"Magic BAllss")     
    glutMouseFunc(mouse_listener)
    glutSpecialFunc(special_key_listener)   
    glutKeyboardFunc(keyboard_listener)     
    glutIdleFunc(animate)               
    glutDisplayFunc(display)                       
    glutMainLoop()                              

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)     
    glMatrixMode(GL_PROJECTION)    
    glLoadIdentity()              
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)  
    glMatrixMode(GL_MODELVIEW)   

def color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)

def convert_coordinate(x, y):
    return x, WINDOW_HEIGHT - y   

def mouse_listener(button, state, x, y):
    global blink,og_color,stop
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and stop==False:
        bx, by = convert_coordinate(x, y)
        ball_speedx=random.choice([-.05,.05])
        ball_speedy=random.choice([-.05,.05]) 
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)      
        balls.append([bx, by, ball_speedx,ball_speedy,r,g,b])  
        print(f"Ball created at ({bx}, {by})")
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and stop==False:
        blink = not blink
        if blink:
            og_color=[]
            for b in balls:
                og_color.append([b[4], b[5], b[6]])
                b[4] = b[5] = b[6] = 0   
        else:
            for i in range(len(balls)):
                balls[i][4] = og_color[i][0]
                balls[i][5] = og_color[i][1]
                balls[i][6] = og_color[i][2]      

def draw_point(x, y, ball_size,r,g,b):
    glPointSize(ball_size)
    color(r,g,b)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def animate():
    for b in balls:
        b[0] += b[2] * ball_speed
        b[1] += b[3] * ball_speed
        if b[0] <= 0 or b[0] >= WINDOW_WIDTH:
            b[2] = -b[2]
        if b[1] <= 0 or b[1] >= WINDOW_HEIGHT:
            b[3] = -b[3]
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()                                    
    setup_projection()
    for b in balls:
        draw_point(b[0], b[1], ball_size, b[4],b[5],b[6])                                                                                                       
    glutSwapBuffers()

def special_key_listener(key, x, y):
    global ball_speed,stop
    if key == GLUT_KEY_UP and stop==False:
        ball_speed += 0.15 
        print("speeding up")
    elif key == GLUT_KEY_DOWN:
        ball_speed-= 0.15
        if ball_speed<=0:
            ball_speed=0  
        print("speeding down")        
    glutPostRedisplay()

bs=ball_speed
def keyboard_listener(key, x, y):
    global ball_speed,stop,bs    
    if key == b' ':
        stop=not stop
        if stop:
            bs=ball_speed
            ball_speed=0
        else:
            ball_speed=bs
         
if __name__ == "__main__":
    main()
