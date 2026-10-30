#Submitted by s12 group1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
# Camera-related variables
camera_pos = (600,900,800)
fovY = 120  # Field of view
GRID_LENGTH = 900  # Length of grid lines
rand_var=393
######################var#####################
p_cord = [0, 0, 0]
player_angle = 0
first_person = True
start_time = time.time()
day_duration = 3*60  
write=True
PLAYER_W = 50
PLAYER_H = 50
water_ml = 0
MAX_WATER = 1000
seeds=False
sell=False
inventory=False
inventory_items = {"cash": 10,"water": 0, "seeds": {"Spinach": 1,"Carrot": 0,"Radish": 0,"Cauliflower": 0 }, "crops": {"Spinach": 0,"Carrot": 0,  "Radish": 0,"Cauliflower": 0}}
seed_prices = { "Spinach": 3,"Carrot": 6,"Radish": 13,"Cauliflower": 20}
seed_shop_stock = {}
last_shop_day = -1
day=1
last_hour= None
crop_prices = {"Spinach": 7,"Carrot": 13,"Radish": 33,"Cauliflower": 50}
growth_times = {
    "Spinach": 6,
    "Carrot": 9,
    "Radish": 14,
    "Cauliflower": 20
}
game_over = False
game_over_message = ""
############################func####
def check_game_over():
    global game_over, game_over_message, inventory_items, seedbeds
    if seedbeds[2]["unlocked"] and seedbeds[1]["unlocked"]:
        game_over = True
        game_over_message = "Congratulations on your new farm!"
    total_seeds = sum(inventory_items["seeds"].values())
    total_crops = sum(inventory_items["crops"].values())
    if inventory_items["cash"] <= 0 and total_seeds == 0 and total_crops == 0:
        game_over = True
        game_over_message = "Game Over!."
def harvest_bed(bed, seed_name):
    current_hour = get_game_hour_24()
    planted_hour = bed["planted_time"].get(seed_name, None)
    if planted_hour is None:
        return
    hours_passed = (current_hour - planted_hour) % 24
    if hours_passed >= growth_times[seed_name] and bed["watered"].get(seed_name, False):
        bed["planted"][seed_name] -= 1
        if bed["planted"][seed_name] == 0:
            del bed["planted"][seed_name]
            del bed["watered"][seed_name]
            del bed["planted_time"][seed_name]
        inventory_items["crops"][seed_name] += 1
def get_active_seedbed(player_box):
    for bed in seedbeds:
        if bed["unlocked"] and hasCollided(player_box, bed["box"]):
            return bed
    return None

def sell_crop(crop_name):
    global inventory_items
    if inventory_items["crops"][crop_name]<= 0:
        return
    inventory_items["crops"][crop_name]-=1
    inventory_items["cash"] += crop_prices[crop_name]

def buy_seed(seed_name):
    global inventory_items
    price = seed_prices[seed_name]
    if seed_shop_stock[seed_name] <= 0:
        return
    if inventory_items["cash"] < price:
        return
    inventory_items["cash"] -= price
    inventory_items["seeds"][seed_name] += 1
    seed_shop_stock[seed_name] -= 1
def get_game_hour_24():
    elapsed = (time.time() - start_time) % day_duration
    dayf = elapsed / day_duration
    t_min = int(dayf * 24 * 60)
    hour24 = t_min // 60
    return hour24
def col():

    #house
    glBegin(GL_QUADS)
    color(0,100,0)
    glVertex3f(-650, -300, 1)
    glVertex3f(-300, -300, 1)
    glVertex3f(-300, -150, 1)
    glVertex3f(-650, -150, 1)
    glEnd()

    #water
    glBegin(GL_QUADS)
    color(0,100,0)
    glVertex3f(1200, -580, 1)
    glVertex3f(1400, -580, 1)
    glVertex3f(1400, -400, 1)
    glVertex3f(1200, -400, 1)  
    glEnd()

   #shop
    glBegin(GL_QUADS)   
    color(0,100,0)
    glVertex3f(2600, 680, 1)
    glVertex3f(2400, 680, 1)
    glVertex3f(2400, 400, 1)
    glVertex3f(2600, 400, 1)
    glEnd()   

    #vegan
    glBegin(GL_QUADS)   
    color(0,100,0)
    glVertex3f(2400, 2600, 1)
    glVertex3f(2200, 2600, 1)
    glVertex3f(2200, 2300, 1)
    glVertex3f(2400, 2300, 1)
    glEnd()   

    glBegin(GL_QUADS)
    color(0,100,0)
    glVertex3f(120, 1100, 0)
    glVertex3f(280, 1100, 0)
    glVertex3f(280, 1900, 0)
    glVertex3f(120, 1900, 0)
    glEnd()

    glBegin(GL_QUADS)
    color(0,100,0)
    glVertex3f(420, 1100,0)
    glVertex3f(580, 1100,0)
    glVertex3f(580, 1900,0)
    glVertex3f(420, 1900,0)
    glEnd()

    glBegin(GL_QUADS)
    color(0,100,0)
    glVertex3f(720, 1100, 0)
    glVertex3f(880, 1100, 0)
    glVertex3f(880, 1900, 0)
    glVertex3f(720, 1900, 0)
    glEnd()
def get_player_aabb():
    return AABB(
        p_cord[0] - PLAYER_W/2,
        p_cord[1] - PLAYER_H/2,
        PLAYER_W,
        PLAYER_H
    )

def color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)

def land():
    start = -GRID_LENGTH    
    landx = start - (-800)
    landy = start+2000
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+300, landy,1)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 80, 80, 800, 30, 20)
    glPopMatrix()
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+300, landy+800, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()  
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+300, landy+10, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()   

    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+600, landy,1)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 80, 80, 800, 30, 20)
    glPopMatrix()
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+600, landy+800, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()  
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+600, landy+10, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()   

    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+900, landy,1)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 80, 80, 800, 30, 20)
    glPopMatrix()
  
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+900, landy+800, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()  
    glPushMatrix()
    color(139,69,19)
    glTranslatef(landx+900, landy+10, 1) 
    gluSphere(gluNewQuadric(), 78, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()       

def skyc():
    elapsed = time.time() - start_time
    angle = (elapsed / day_duration) * 2 * math.pi  
    t = (math.sin(angle - math.pi/2) + 1) / 2  
    r = 25 + t * (135 - 25)     
    g = 25 + t * (206 - 25)
    b = 40 + t * (235 - 40)
    return r/255.0, g/255.0, b/255.0  

def vegan():
    start = -GRID_LENGTH    
    sx = start - (-800)
    sy = start+2000    
    t=time.time()% 2         
    scale = 1 +0.05*math.sin(t * math.pi) 
    hour=get_game_hour_24()
    if 11<=hour<20:
        glPushMatrix()
        glTranslatef(sx+2600, sy+1400, 1)
        glScalef(scale, scale, scale)        
        #BODY
        glTranslatef(0, 0, 40 )    
        color(75,0,130)
        gluSphere(gluNewQuadric(), 100 , 20, 20)
        #HEAD 
        glTranslatef(0, 0, 100)
        color(210,180,140)
        gluSphere(gluNewQuadric(), 60 , 15, 15) 
        color(105,105,105)
        glTranslatef(0, 0,30)
        glRotatef(0, 1, 0, 0) 
        gluCylinder(gluNewQuadric(), 50, 40, 40, 30, 20)     
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2460, 2470, 160)
        color(0,0,0)
        gluSphere(gluNewQuadric(), 6, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2450, 2500, 160)
        gluSphere(gluNewQuadric(), 6, 10, 10)
        glPopMatrix()    

def seed():    
    start = -GRID_LENGTH    
    sdx = start - (-800)
    sdy = start+2000      
    glPushMatrix()
    color(114,54,54)
    glTranslatef(sdx+2700, sdy-550,1)
    glScale(2.3,7,3.6)
    glutSolidCube(60)
    glPopMatrix()
    glPushMatrix()
    color(114,54,54)
    glTranslatef(sdx+2700, sdy-450,30)
    gluCylinder(gluNewQuadric(), 10, 10, 300, 30, 20)
    glPopMatrix()    
    glPushMatrix()
    color(114,54,54)
    glTranslatef(sdx+2700, sdy-600,30)
    gluCylinder(gluNewQuadric(), 10, 10, 300, 30, 20)
    glPopMatrix()        

def sign():
    start = -GRID_LENGTH    
    six = start - (-800)
    siy = start+2000     
    hour = get_game_hour_24()  
    glPushMatrix()
    color(114,54,54)
    glTranslatef(six+2700, siy-530,250)
    glScale(1,4,2)
    glutSolidCube(60)
    glPopMatrix()

    glPushMatrix()
    if 8 <=hour<17:
        color(60,179,113)   
    else:
        color(178,34,34)    
    glTranslatef(six+2670, siy-530,250)
    glScale(.3,3.3,2)
    glutSolidCube(50)
    glPopMatrix()

def get_game_clock():
    elapsed = (time.time() - start_time) % day_duration
    dayf = elapsed / day_duration  
    t_min = int(dayf * 24 * 60)
    hour24 = t_min // 60
    minute = t_min % 60
    am_pm = "AM" if hour24 < 12 else "PM"
    hour12 = hour24 % 12
    if hour12 == 0:
        hour12 = 12
    return f"{hour12:02d}:{minute:02d} {am_pm}"

def draw_letter_screen():
    global write,seeds, sell,inventory,inventory_items
    if write==True and seeds==False and sell==False and inventory==False:
        begin_2d()
        color(233,150,122)
        glBegin(GL_QUADS)
        glVertex2f(100, 100)
        glVertex2f(920, 100)
        glVertex2f(860, 700)
        glVertex2f(150, 700)   
        glEnd() 
        draw_text(180, 650, "Welcome to Beecher's Hope fellow...neighbour? Heard you're only two")
        draw_text(180, 620, "seedbeds away from owning the farm, good for you. Let me help you get")
        draw_text(180, 590, "started.")
        draw_text(170, 540, "Seed shop opens at 08:00Am sharp and the health-nut living a few blocks away")
        draw_text(170, 510, "will drop by at 11:00Am for some fresh produce. Don't worry, he pays.")
        draw_text(170, 470, "Not much but, sending you 10 bucks and a spinach seed. Plant the seed on the")    
        draw_text(165, 440, "seedbed and water the spot to encourage sprouting. Wait a while until you are")
        draw_text(160, 410, "able to harvest. The growth rate varies for each type of plant. Also, take a nap")
        draw_text(150, 370, "at the barn to wake up at 06:00Am the next day to get some of that well deserved rest.")
        draw_text(150, 340, "Good luck!")     
        draw_text(666, 160, "Press 'i' to view inventory")         
        draw_text(666, 130, "Press 'b' to return")     
        end_2d()
    elif write==False and seeds==True and sell==False and inventory==False:
        begin_2d()
        color(0,100,0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(1000, 0)
        glVertex2f(1000, 1200)
        glVertex2f(0, 1200)   
        glEnd()         
        color(189,183,107)
        glBegin(GL_QUADS)
        glVertex2f(150, 100)
        glVertex2f(850, 100)
        glVertex2f(850, 700)
        glVertex2f(150, 700)   
        glEnd() 
        color(0, 0, 0) 
        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex2f(150, 650)               
        glVertex2f(850,650)  
        glEnd()        
        draw_text(180, 670, "Seed Shop (Open 08:00AM to 05:00PM)")
        draw_text(120, 720, "Note: Spinach, Carrots, Radish and Cauliflower take 6, 9, 14 and 20 hours to grow respectively")        
        draw_text(640, 150, "Press 1-4 to buy seeds")       
        draw_text(640, 130, "Press 'b' to return")     
        i = 1
        y=600
        for seed, price in seed_prices.items():
            stock=seed_shop_stock.get(seed, 0)
            y -=40
            draw_text(180, y,f"{i}. {seed} - ${price} (Stock: {stock})")
            i += 1        
        unlock_prices = [200, 400]  
        unlock_keys = ['o', 'p']  # Keys corresponding to lands 2 and 3
        y -= 60
        draw_text(180, y, "Unlock Land:")
        for idx, (price, key) in enumerate(zip(unlock_prices, unlock_keys), start=2):
            y -= 40
            status = "Unlocked" if seedbeds[idx-1]["unlocked"] else f"${price}"
            draw_text(200, y, f"Land {idx} - {status} (Press '{key}')")
        end_2d()
    elif write==False and seeds==False and sell==True and inventory==False:
        begin_2d()
        color(72,61,139)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(1000, 0)
        glVertex2f(1000, 1200)
        glVertex2f(0, 1200)   
        glEnd()         
        color(106,90,205)
        glBegin(GL_QUADS)
        glVertex2f(150, 100)
        glVertex2f(850, 100)
        glVertex2f(850, 700)
        glVertex2f(150, 700)   
        glEnd() 
        color(0, 0, 0) 
        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex2f(150, 630)               
        glVertex2f(850,630)  
        glEnd()        
        draw_text(180, 670, "This farm belonged to my granddad. We used to hangout ")
        draw_text(180, 640, "from 11Am till 5PM on the regular here. I'm sure you won't mind either")
        draw_text(180, 600, f"1. Spinach      x {inventory_items['crops']['Spinach']}")
        draw_text(180, 570, f"2. Carrot       x {inventory_items['crops']['Carrot']}")
        draw_text(180, 540, f"3. Radish       x {inventory_items['crops']['Radish']}")
        draw_text(180, 510, f"4. Cauliflower  x {inventory_items['crops']['Cauliflower']}")
        draw_text(649, 160, "Press 1-4 to sell crops")
        draw_text(649, 130, "Press 'b' to return")     
        end_2d()
    elif write==False and seeds==False and sell==False and inventory==True:
        begin_2d()
        color(72,61,139)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(1000, 0)
        glVertex2f(1000, 1200)
        glVertex2f(0, 1200)   
        glEnd()         
        color(106,90,205)
        glBegin(GL_QUADS)
        glVertex2f(150, 100)
        glVertex2f(850, 100)
        glVertex2f(850, 700)
        glVertex2f(150, 700)   
        glEnd() 
        color(0, 0, 0) 
        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex2f(150, 650)               
        glVertex2f(850,650)  
        glEnd()        
        draw_text(180, 670, "Inventory")
        draw_text(666, 130, "Press 'i' to return")     
        draw_text(180, 620, f"Cash: ${inventory_items['cash']}")
        draw_text(180, 590, f"Water level: {water_ml}/{MAX_WATER} ml")

        # seeds
        y_seed = 550
        draw_text(180, y_seed, "Seeds:")
        for seed, qty in inventory_items["seeds"].items():
            y_seed -= 30
            draw_text(200, y_seed, f"{seed} seed: {qty}")

        #crops
        y_crop = y_seed - 45
        draw_text(180, y_crop, "Crops:")
        y_crop -= 3
        for crop, qty in inventory_items["crops"].items():
            y_crop -= 30
            draw_text(200, y_crop, f"{crop}: {qty}")        
        end_2d()        

def skip_to_next_day_6am():
    global start_time,day
    day+=1
    start_time = time.time()-(180*0.25)
def check_collisions():
    global water_ml,seeds,sell,last_shop_day
    player_box = get_player_aabb()
    if hasCollided(player_box, barn_sleep_box):
        skip_to_next_day_6am()
        push_player_back()
        
    if hasCollided(player_box, well_box):
        push_player_back()  
        water_ml = min(water_ml + 1000, MAX_WATER) 

    if hasCollided(player_box, seed_box):
        hour = get_game_hour_24()
        if 8 <=hour<17:   
            current_day = day
            if current_day != last_shop_day:
                refresh_seed_shop_stock()
                last_shop_day = current_day
            push_player_back()
            seeds = True
            if seeds==True:
                draw_letter_screen()
        else:
            push_player_back() 

    if hasCollided(player_box, sell_box):
        hour = get_game_hour_24()
        if 11<=hour<20:   
            push_player_back()
            sell = True
            if sell==True:
                draw_letter_screen()
        else:
            push_player_back() 

def push_player_back(steps=10, step_size=50):
    angle_rad = math.radians(player_angle + 90)
    p_cord[0] -= math.cos(angle_rad) * step_size * steps
    p_cord[1] -= math.sin(angle_rad) * step_size * steps        
############################################collision
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
barn_sleep_box = AABB(-650, -300,350,150 )
well_box = AABB(1200, -580, 200, 180)
seed_box= AABB(2400,400,200,280)
sell_box=AABB(2200, 2300, 200, 300)
seedbeds = [{
"box": AABB(120, 1100, 160, 800),
"unlocked": True,
"planted": {},        
"watered": {},        
"planted_time": {}   
    },
    {
"box": AABB(420, 1100, 160, 800),
"unlocked": False,
"planted": {},
"watered": {},
"planted_time": {}},{
"box": AABB(720, 1100, 160, 800),
"unlocked": False,
"planted": {},
"watered": {},
"planted_time": {} }]
def refresh_seed_shop_stock():
    global seed_shop_stock
    seed_shop_stock = {
        "Spinach": random.randint(0, 3),
        "Carrot": random.randint(0, 3),
        "Radish": random.randint(0, 3),
        "Cauliflower": random.randint(0, 3)}
###########view################
def begin_2d():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()   
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()   
    glLoadIdentity()

def end_2d():
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#################
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

def draw_shapes():
    global  player_angle
    glPushMatrix()
    glTranslatef(p_cord[0], p_cord[1], 0)
    glRotatef(player_angle, 0, 0, 1)    
    glPushMatrix()
    glTranslatef(0,0,0)    
    glPushMatrix()  
    color(85,107,47)
    glTranslatef(0, 0, 30)  
    glScalef(1.4, .6, 2.2)    
    glutSolidCube(60) 
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
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, -5, 90) 
    gluSphere(gluNewQuadric(), 25, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()    
    glPopMatrix()  
    glPopMatrix()  



def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global p_cord,player_angle, GRID_LENGTH, write,seeds,sell,inventory,water_ml,game_over,game_over_message,seedbeds,inventory_items

    move_speed =25
    rotation_speed =7
    angle_rad = math.radians(player_angle + 90)
    if key == b'w':  # forward
        dx = move_speed * math.cos(angle_rad)
        dy = move_speed * math.sin(angle_rad)
        new_x = p_cord[0] + dx
        new_y = p_cord[1] + dy
        if -GRID_LENGTH <= new_x <= GRID_LENGTH*3:
          p_cord[0] = new_x
        if -GRID_LENGTH <= new_y <= GRID_LENGTH*3:
          p_cord[1] = new_y
    if key == b's':  # backward
        dx = move_speed * math.cos(angle_rad)
        dy = move_speed * math.sin(angle_rad)
        new_x = p_cord[0] - dx
        new_y = p_cord[1] - dy
        if -GRID_LENGTH <= new_x <= GRID_LENGTH*3:
          p_cord[0] = new_x
        if -GRID_LENGTH <= new_y <= GRID_LENGTH*3:
          p_cord[1] = new_y

    if key == b'a':  #left
        player_angle += rotation_speed

    if key == b'd':  #right
        player_angle -= rotation_speed    
    if key==b'b':
        if write==True and seeds==False and sell==False and inventory==False:
            write=not write
        elif write==False and seeds==True and sell==False and inventory==False:
            seeds=not seeds
        elif write==False and seeds==False and sell==True and inventory==False:
            sell=not sell
    if key==b'i':
        inventory= not inventory
        write = seeds = sell = False         

    if seeds and not write and not sell and not inventory:
        if key == b'1':
            buy_seed("Spinach")
        elif key == b'2':
            buy_seed("Carrot")
        elif key == b'3':
            buy_seed("Radish")
        elif key == b'4':
            buy_seed("Cauliflower")

    if sell and not write and not seeds and not inventory:
        if key == b'1':
            sell_crop("Spinach")
        elif key == b'2':
            sell_crop("Carrot")
        elif key == b'3':
            sell_crop("Radish")
        elif key == b'4':
            sell_crop("Cauliflower")
    bed = get_active_seedbed(get_player_aabb())

    if bed:
        if key in [b'1', b'2', b'3', b'4']:
            seed_list = ["Spinach","Carrot","Radish","Cauliflower"]
            seed_to_plant = seed_list[int(key)-1]
            if inventory_items["seeds"][seed_to_plant] > 0:
                inventory_items["seeds"][seed_to_plant] -= 1
                bed["planted"][seed_to_plant] = bed["planted"].get(seed_to_plant,0) + 1
                bed["watered"][seed_to_plant] = False
                bed["planted_time"][seed_to_plant] = get_game_hour_24()

    # Water
    if key == b'q' and water_ml > 0:
        for seed in bed["planted"]:
            bed["watered"][seed] = True
        water_ml = max(0, water_ml - 250)

    # Harvest
    if key == b'e':
        harvested = []
        for seed in list(bed["planted"].keys()):
            if bed["watered"].get(seed, False):
                harvest_bed(bed, seed)
                harvested.append(seed)
    if key == b'o':  
        land_idx = 1
        price = 200
        if not seedbeds[land_idx]["unlocked"]:
            if inventory_items["cash"] >= price:
                inventory_items["cash"] -= price
                seedbeds[land_idx]["unlocked"] = True
                print("Land 2 unlocked!")
            else:
                print("Not enough money!")

    elif key == b'p': 
        land_idx = 2
        price = 400
        if not seedbeds[land_idx]["unlocked"]:
            if inventory_items["cash"] >= price:
                inventory_items["cash"] -= price
                seedbeds[land_idx]["unlocked"] = True
                print("Land 3 unlocked!")
            else:
                print("Not enough money!")        
    if key == b'r' and game_over:
        game_over = False
        game_over_message = ""
        p_cord = [0, 0, 0]
        player_angle = 0
        inventory_items = {"cash": 400,"water": 0, "seeds": {"Spinach": 1,"Carrot": 0,"Radish": 0,"Cauliflower": 0 }, "crops": {"Spinach": 0,"Carrot": 0,  "Radish": 0,"Cauliflower": 0}}
        seedbeds = [
            {"box": seedbeds[0]["box"], "unlocked": True, "planted": {}, "watered": {}, "planted_time": {}},
            {"box": seedbeds[1]["box"], "unlocked": False, "planted": {}, "watered": {}, "planted_time": {}},
            {"box": seedbeds[2]["box"], "unlocked": False, "planted": {}, "watered": {}, "planted_time": {}}]                  
def setupCamera():
    global first_person    
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, .1, 6000) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    if first_person:
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


def reshape(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glutPostRedisplay()

def idle():
    global day,last_hour
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    if not game_over:
        hour = get_game_hour_24()
        if last_hour is None:
            last_hour = hour
        if last_hour == 23 and hour == 0:
            day += 1
        last_hour = hour
        check_game_over()  
    # Ensure the screen updates with the latest changes

    glutPostRedisplay()

def showScreen():
    global write, seeds, sell, inventory, game_over, game_over_message

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if write or seeds or sell or inventory:
        glViewport(0, 0, 1000, 800)
        draw_letter_screen()
        glutSwapBuffers()
        return

    # Keep the rest of your existing showScreen() code below.

    r, g, b = skyc()
    glClearColor(r, g, b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    check_collisions()
    # Draw the grid (game floor)
    size = (GRID_LENGTH +1000) * 4
    start = -(GRID_LENGTH+1000)
    glBegin(GL_QUADS)
    color(34,139,34)
    glVertex3f(start, start, 0)
    color(34,139,34)
    glVertex3f(start + size, start, 0)
    color(0,100,0)
    glVertex3f(start + size, start + size, 0)
    color(144,238,144)
    glVertex3f(start, start + size, 0)
    glEnd()
#############fence
    start = -GRID_LENGTH
    end = start + GRID_LENGTH * 4
    h = 120
    plank_w = 30
    gap = 20
    color(184,134,11)
    x = start
    while x < end:
        glBegin(GL_QUADS)
        # front
        glVertex3f(x, start, 0)
        glVertex3f(x + plank_w, start, 0)
        glVertex3f(x + plank_w, start, h)
        glVertex3f(x, start, h)
        # back
        glVertex3f(x, end, 0)
        glVertex3f(x + plank_w, end, 0)
        glVertex3f(x + plank_w, end, h)
        glVertex3f(x, end, h)
        glEnd()
        x += plank_w + gap
    y = start
    while y < end:
        glBegin(GL_QUADS)
        # left
        glVertex3f(start, y, 0)
        glVertex3f(start, y + plank_w, 0)
        glVertex3f(start, y + plank_w, h)
        glVertex3f(start, y, h)
        # right
        glVertex3f(end, y, 0)
        glVertex3f(end, y + plank_w, 0)
        glVertex3f(end, y + plank_w, h)
        glVertex3f(end, y, h)
        glEnd()
        y += plank_w + gap
###################barn
    barn_size = 100
    glPushMatrix()
    color(128,0,0)
    glTranslatef(start - (-380) + barn_size/2, start+barn_size+200, 1)
    glScale(8,6,4.5)
    glutSolidCube(barn_size)
    glPopMatrix()
    #door##########################################
    door_width = 300
    door_height = 200
    barn_x = start - (-380) + barn_size/2
    barn_y = start + barn_size + 500
    barn_z = 1
    glLineWidth(10)
    glColor3f(255,255,255)  
    glBegin(GL_LINES)
    #bottom
    glVertex3f(barn_x - door_width/2, barn_y, barn_z)
    glVertex3f(barn_x + door_width/2, barn_y, barn_z)
    #top
    glVertex3f(barn_x - door_width/2, barn_y, barn_z + door_height)
    glVertex3f(barn_x + door_width/2, barn_y, barn_z + door_height)
    #left 
    glVertex3f(barn_x - door_width/2, barn_y, barn_z)
    glVertex3f(barn_x - door_width/2, barn_y, barn_z + door_height)
    #right side
    glVertex3f(barn_x + door_width/2, barn_y, barn_z)
    glVertex3f(barn_x + door_width/2, barn_y, barn_z + door_height)
    glVertex3f(barn_x - door_width/2, barn_y, barn_z + door_height)
    glVertex3f(barn_x + door_width/2, barn_y, barn_z)    
    glEnd()

    glPushMatrix()
    color(105,105,105)
    glTranslatef(start - (-400) + barn_size/2, start + (280) + barn_size/2, 250)
    glScale(8.6,6.6,.6)
    glutSolidCube(barn_size)
    glPopMatrix()
    # Display game info text at a fixed screen position
    clock_text = get_game_clock()
    draw_text(840, 760, clock_text)
    if game_over:
        begin_2d()
        color(255, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(200, 300)
        glVertex2f(800, 300)
        glVertex2f(800, 500)
        glVertex2f(200, 500)
        glEnd()
        draw_text(300, 450, game_over_message)
        draw_text(350, 400, "Press 'r' to restart")
        end_2d()
        glutSwapBuffers()
        return
#######well
    well_x = start - (-2200)
    well_y = start+200
    draw_text(well_x + 50, well_y + 0, "Well")
    glPushMatrix()
    color(205,133,63)
    glTranslatef(well_x, well_y, 0)
    gluCylinder(gluNewQuadric(), 120, 120, 140, 30, 1)
    glPopMatrix()
    glPushMatrix()#water
    color(204, 229, 255)
    glTranslatef(well_x, well_y, 100)
    glRotate(180,1,0,0)
    gluCylinder(gluNewQuadric(), 120, 0, 50, 30, 20)
    glPopMatrix()
    player_box = get_player_aabb()
    bed = get_active_seedbed(player_box)
    if bed:
        total_planted = sum(bed["planted"].values())
        total_watered = sum(1 for w in bed["watered"].values() if w)
        if total_planted < 3:
            draw_text(350, 120, "Press 1-4 to plant seed")
        if total_planted > 0 and total_watered < total_planted:
            draw_text(350, 90, "Press Q to water")
        if total_planted > 0:
            draw_text(350, 60, "Press E to harvest")

    glPushMatrix()
    glColor3f(0, 0, 255)
    glTranslatef(well_x, well_y, 350) 
    gluSphere(gluNewQuadric(), 77, 20, 20)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()   
    glPushMatrix()#water
    color(0,0,255)
    glTranslatef(well_x, well_y, 350)
    gluCylinder(gluNewQuadric(), 80, 0, 140, 30, 20)
    glPopMatrix()
    draw_shapes()
    land()
    vegan()
    seed()
    sign()
    #########collision coord
    col()
    draw_text(13, 770, f"Cash: ${inventory_items['cash']}")      
    draw_text(13, 740, f"Watering can carrying {water_ml} ml water")    
    #########

    glutSwapBuffers()


# Main function to set up OpenGL window and loop

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(100, 100)

    wind = glutCreateWindow(b"3D OpenGL Intro")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(showScreen)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)

    glutPostRedisplay()
    glutMainLoop()


if __name__ == "__main__":
    main()
