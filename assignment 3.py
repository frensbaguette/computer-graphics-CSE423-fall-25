from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
# Camera-related variables
camera_pos = (0,500,500)
fovY = 120  # Field of view
GRID_LENGTH = 3000  # Length of grid lines
rand_var = 423
##########variables#####################
enemyl=[]
p_cord = [0, 0, 0]
player_angle = 0
bullet=[]
hp=5
score=0
missed=0
dead = False
cheat=False
lspawn = 0
camera_angle = 0
first_person = False
cam_radius = 700
camera_pos = (0, 500, 500)
cheatfp=False
change2d=False
################extra functions########################
def color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)

def draw_enemy():
    t=time.time()% 2         
    scale = 1 + 0.2 * math.sin(t * math.pi) 
    for enemy in enemyl:
        x, y, z = enemy  
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)        
        # BODY
        glColor3f(1, 0, 0)
        gluSphere(gluNewQuadric(), 45 , 20, 20)
        # HEAD 
        glTranslatef(0, 0, 30 )
        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), 30 , 15, 15)
        glPopMatrix()

def enemy_cn():
    global enemyl
    while len(enemyl) < 5:
        x = random.randint(10, GRID_LENGTH - 10)
        y = random.randint(10, GRID_LENGTH - 10)
        enemyl.append([x, y, 30])
        if cheat:
            spawning(x, y)

def spawning(ex, ey):
    global bullet, p_cord
    speed = 5
    dx= ex - p_cord[0]
    dy= ey - p_cord[1]
    dist = (dx**2 + dy**2)**0.5
    if dist== 0:
        dist = 1
    vx = speed * dx / dist
    vy = speed* dy / dist
    bullet.append([p_cord[0], p_cord[1],90, vx, vy])

###############################################################

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():#shooter 
    global  player_angle,dead

    glPushMatrix()
    glTranslatef(p_cord[0], p_cord[1], 0)
    if dead:
        glRotatef(-90, 1, 0, 0)
    glRotatef(player_angle, 0, 0, 1)    
    glPushMatrix()
    glTranslatef(0,0,0)    
    glPushMatrix()  
    color(85,107,47)
    glTranslatef(0, 0, 30)  
    glScalef(1.4, .6, 2.2)    
    glutSolidCube(60) 
    glPopMatrix()
    glPushMatrix()#rl
    glTranslatef(-25, -5, -10)
    glColor3f(0, 0, 1)  
    glRotatef(180, 0, 1, 0) 
    gluCylinder(gluNewQuadric(), 15, 8, 70, 10, 10)
    glPopMatrix()
    glPushMatrix()#ll
    glTranslatef(25,-5, -10)
    glColor3f(0, 0, 1)  
    glRotatef(180, 0, 1, 0) 
    gluCylinder(gluNewQuadric(), 15, 8, 70, 20, 20)
    glPopMatrix()    

    glPushMatrix()#rh
    glTranslatef(-23, 0, 70)
    glRotatef(-90, 45, 1, 0)
    color(255,228,196) 
    gluCylinder(gluNewQuadric(), 10, 5, 60, 10, 10)  
    glPopMatrix()
    glPushMatrix()#lh
    glTranslatef(23, 0, 70)
    glRotatef(-90, 45, 1, 0)
    color(255,228,196)  
    gluCylinder(gluNewQuadric(), 10, 5, 60, 10, 10)
    glPopMatrix()    

        # gun 
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glRotatef(-90, 45, 1, 0)
    color(220,220,220) 
    gluCylinder(gluNewQuadric(), 14, 5, 100, 15, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, -5, 90) 
    gluSphere(gluNewQuadric(), 25, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()
    glPopMatrix()  
    glPopMatrix()

    
def keyboardListener(key, x, y):
    global p_cord,player_angle, GRID_LENGTH, hp, score, missed, bullet, enemyl, dead,cheat,first_person,cheatfp

    move_speed =10
    rotation_speed =7
    angle_rad = math.radians(player_angle + 90)
    if key == b'w'and dead==False:  # forward
        dx = move_speed * math.cos(angle_rad)
        dy = move_speed * math.sin(angle_rad)
        new_x = p_cord[0] + dx
        new_y = p_cord[1] + dy
        if -GRID_LENGTH <= new_x <= GRID_LENGTH:
            p_cord[0] = new_x
        if -GRID_LENGTH <= new_y <= GRID_LENGTH:
            p_cord[1] = new_y

    if key == b's'and dead==False:  # backward
        dx = move_speed * math.cos(angle_rad)
        dy = move_speed * math.sin(angle_rad)
        new_x = p_cord[0] - dx
        new_y = p_cord[1] - dy
        if -GRID_LENGTH <= new_x <= GRID_LENGTH:
            p_cord[0] = new_x
        if -GRID_LENGTH <= new_y <= GRID_LENGTH:
            p_cord[1] = new_y

    if key == b'a'and dead ==False and cheat==False:  #left
        player_angle += rotation_speed

    if key == b'd' and dead ==False and cheat==False:  #right
        player_angle -= rotation_speed
  
    # Reset the game if R key is pressed
    if dead:
        if key == b'r':  
            hp = 5
            score = 0
            missed = 0
            bullet.clear()
            enemyl.clear()
            enemy_cn()
            dead = False
            cheat = False
        return  
    # Toggle cheat mode (C key)
    if key == b'c':
        first_person=False
        cheat = not cheat

    if key == b'v' and cheat:
        cheatfp=not cheatfp

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, camera_angle
    cam_radius = 700
    x, y, z = camera_pos
    if key == GLUT_KEY_LEFT:
        camera_angle += 3
    if key == GLUT_KEY_RIGHT:
        camera_angle -= 3
    if key == GLUT_KEY_UP:
        z += 10
    if key == GLUT_KEY_DOWN:
        z -= 10
    x = cam_radius * math.cos(math.radians(camera_angle))
    y = cam_radius * math.sin(math.radians(camera_angle))

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    global bullet, p_cord,player_angle,dead,first_person
    speed=1
    gun_point=100
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and dead==False:
        print('Player Bullet Fired!')
        angle_rad = math.radians(player_angle + 90)      
        bul_x = p_cord[0] + gun_point *math.cos(angle_rad)  
        bul_y =p_cord[1]+ gun_point *math.sin(angle_rad)
        bul_z=90
        bx = speed * math.cos(angle_rad)
        by =speed * math.sin(angle_rad)
        bullet.append([bul_x, bul_y, bul_z, bx, by])
        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        new_point = convert_coordinate(x, y)
        print(f"New point created at {new_point}")    
def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (1900/ 2)
    b = (6000 / 2) - y
    return a, b
def setupCamera():
    global first_person,cheatfp
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.01, 3000) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    if first_person and cheat==False:
        angle_rad = math.radians(player_angle + 90)
        x = p_cord[0]
        y = p_cord[1]
        z = 200
        lx = x + math.cos(angle_rad) * 100
        ly = y + math.sin(angle_rad) * 100
        lz = z - 20  
        gluLookAt(
            x, y, z,
            lx, ly, lz,
            0, 0, 1
        )
    elif cheatfp and cheat==True:
        angle_rad = math.radians(player_angle + 90)
        x = p_cord[0]
        y = p_cord[1]
        z = 200
        lx = x + math.cos(angle_rad) * 100
        ly = y + math.sin(angle_rad) * 100
        lz = z - 20  
        gluLookAt(
            x, y, z,
            lx, ly, lz,
            0, 0, 1
        )        
    else:    
        # Extract camera position and look-at target
        x, y, z = camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    global bullet,enemyl,hp,score,missed,dead,player_angle,cheat,lspawn
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    if cheat and dead==False:
        player_angle += 1  
        current_time = time.time()
        if current_time - lspawn > 0.5: 
            for enemy_pos in enemyl:
                spawning(enemy_pos[0], enemy_pos[1])
            lspawn = current_time
    if dead:  
        bullet.clear()
        glutPostRedisplay()
        return
    for b in bullet[:]:
        b[0]+=b[3]
        b[1]+=b[4]
        if abs(b[0]) > GRID_LENGTH or abs(b[1]) > GRID_LENGTH:
            bullet.remove(b)
            missed += 1
            print(f'Bullet missed: {missed}')
            if missed>= 10:
                dead=True
        if missed > 10:
            missed = 10  
        if missed >= 10:
            dead = True    

    player_box = AABB(p_cord[0] - 42, p_cord[1] -30, 60, 60)    
    for i, enemy in enumerate(enemyl):
        enemy_box = AABB(enemy[0] - 40, enemy[1] - 40, 80, 80)  
        ex, ey, ez = enemy
        dx = p_cord[0] - ex
        dy = p_cord[1] - ey
        dist=(dx**2 +dy**2)** 0.5
        if dist != 0:
            speed = 0.0523 
            enemy[0] += speed *dx /dist
            enemy[1] += speed * dy/dist
        enemy_box = AABB(enemy[0]-40, enemy[1]-40, 90, 80)  
        for j, b in enumerate(bullet[:]):
            bullet_box = AABB(b[0]-4, b[1]-4, 8, 8)  
            if hasCollided(enemy_box, bullet_box):
                bullet.pop(j)
                score+=1
                enemyl[i] = [random.randint(-GRID_LENGTH+10, GRID_LENGTH-10),
                             random.randint(-GRID_LENGTH+10, GRID_LENGTH-10),
                             30]
                break  
        if hasCollided(enemy_box, player_box):
            hp-=1
            if hp <=0:  
                hp = 0 
                dead=True      
            print(f'Remaining Player Life: {hp}')
            enemyl[i] = [random.randint(-GRID_LENGTH+10, GRID_LENGTH-10),
                         random.randint(-GRID_LENGTH+10, GRID_LENGTH-10),
                         30]                
        if hp <= 0:
            dead=True        
    glutPostRedisplay()

#GRIDC,wall, bullet
def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
#chessboard
    global GRID_LENGTH,bullet
    size = GRID_LENGTH * 2         
    square = size / 13               
    start = -GRID_LENGTH           
    for row in range(13):
        for col in range(13):
            if (row + col) % 2 == 0:
                glColor3f(1,1,1)
                x1=start+col*square
                x2=start+(col+1)*square
                y1=start+row*square
                y2=start+(row+1)*square
                glBegin(GL_QUADS)
                glVertex3f(x1,y1,0)
                glVertex3f(x2,y1,0)
                glVertex3f(x2,y2,0)
                glVertex3f(x1,y2,0)
                glEnd()
    for row in range(13):
        for col in range(13):
            if (row + col) % 2 == 1:
                glColor3f(0.7,0.5,0.95)
                x1=start+col*square
                x2=start+(col+1)*square
                y1=start+row*square
                y2=start+(row+1)*square
                glBegin(GL_QUADS)
                glVertex3f(x1,y1,0)
                glVertex3f(x2,y1,0)
                glVertex3f(x2,y2,0)
                glVertex3f(x1,y2,0)
                glEnd()
    #4wall
    zwall = 120
    glBegin(GL_QUADS)#white
    color(255,255,255)
    glVertex3f(start, start + size, 0)
    glVertex3f(start + size, start + size, 0)
    glVertex3f(start + size, start + size, zwall)
    glVertex3f(start, start + size, zwall)
    glEnd()
    glBegin(GL_QUADS)#blue
    color(0,0,255)
    glVertex3f(start + size, start, 0)
    glVertex3f(start + size, start + size, 0)
    glVertex3f(start + size, start + size, zwall)
    glVertex3f(start + size, start, zwall)
    glEnd()
    glBegin(GL_QUADS)#cyan
    color(0,255,255)
    glVertex3f(start, start, 0)
    glVertex3f(start + size, start, 0)
    glVertex3f(start + size, start, zwall)
    glVertex3f(start, start, zwall)
    glEnd()
    glBegin(GL_QUADS)#limegre
    color(0,255,0)
    glVertex3f(start, start, 0)
    glVertex3f(start, start + size, 0)
    glVertex3f(start, start + size, zwall)
    glVertex3f(start, start, zwall)
    glEnd() 

    draw_text(10, 770, f"Player Life Remaining: {hp}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player Bullet Missed: {missed}")
    draw_shapes()
    draw_enemy()
    for bul in bullet:
        glPushMatrix()
        glTranslatef(bul[0], bul[1], bul[2])
        glColor3f(1, 0, 0)  
        glutSolidCube(8)
        glPopMatrix()    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()
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

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    enemy_cn()
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
