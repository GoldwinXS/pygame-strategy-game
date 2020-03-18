import pygame as pg
import numpy as np
import os
import math


class Game():



    def __init__(self):
        self.GAME_HEIGHT = 800
        self.GAME_WIDTH = 1200
        self.DIFFICULTY = 1
        self.GRID_SIZE = 5
        self.current_game_session = None
        self.menus = Menus(GAME_HEIGHT=self.GAME_HEIGHT ,GAME_WIDTH=self.GAME_WIDTH)

        self.new_game()  # make a new game right away for now




    def new_game(self):
        self.current_game_session = Universe(GAME_HEIGHT = self.GAME_HEIGHT,
                                             GAME_WIDTH = self.GAME_WIDTH,
                                             DIFFICULTY = self.DIFFICULTY,
                                             GRID_SIZE = self.GRID_SIZE)


    # def save_game(self):
    #     # self.empty_grids = {'pos': [], 'planets': [], 'mobs': [], 'enemy_mobs': [], 'starfields': [], 'discovered': []}
    #
    #     dir_list = os.listdir('saves/')
    #     dat = pd.DataFrame({'pos': [], 'planets': [], 'mobs': [], 'enemy_mobs': [], 'starfields': [], 'discovered': []})
    #     pd.to_pickle(dat,'saves/save_'+str(len(dir_list))+'.pickle')

    # def load_game(self,save):
    #     self.current_game_session = pk.load()

    def run(self):
        running = True
        game_window = pg.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        clock = pg.time.Clock()

        self.main_menu = True
        self.start_game = False
        self.game_running = False

        # self.main_menu = False
        # self.start_game = True
        # self.game_running = True

        while running:
            if self.start_game:
                self.GAME_WIDTH,self.GAME_HEIGHT,self.DIFFICULTY,self.GRID_SIZE = self.menus.get_settings()
                self.new_game()
                self.start_game = False
                self.main_menu = False
                self.game_running = True
            elif self.main_menu:
                self.start_game = self.menus.menus(game_window)
            elif self.game_running:
                self.run_game(game_window)
                if self.current_game_session.make_save:
                    self.save_game()

            pg.display.update()
            clock.tick()

    def run_game(self,surface):
        surface.fill((0, 0, 0))
        self.current_game_session.handle_event(surface)
        self.current_game_session.render_grid(surface)

def clear_dict_at_index(dict, index):
    keys = dict.keys()
    for key in keys:
        del dict[key][index]

    return dict


class Menus():

    light_grey = (155, 155, 155)
    dark_grey = (75, 75, 75)
    darker_grey = (25, 25, 25)


    def __init__(self,GAME_WIDTH,GAME_HEIGHT):

        self.GAME_WIDTH = GAME_WIDTH
        self.GAME_HEIGHT = GAME_HEIGHT
        self.main_menu_active = True
        self.game_running = False
        self.setting_menu_active = False
        self.make_starfield()
        self.main_menu_options = ['New Game','How to Play','Settings','Load Game','Quit']
        self.settings_menu_options = ['Difficulty:','Game Resolution:','Universe Size:','Music Volume:','Music On:']
        self.passing_mobs = Mobs(GAME_WIDTH=GAME_WIDTH,GAME_HEIGHT=GAME_HEIGHT,color=(200,0,50))

        all_fonts = pg.font.get_fonts()
        self.player_stats = None
        if all_fonts.__contains__('helveticattc'):
            self.font = all_fonts[all_fonts.index('helveticattc')]

        else:
            self.font = all_fonts[0]

        # pg.mixer.music.load('sounds/music/background.mp3')
        # pg.mixer.music.set_volume(0.105)
        # pg.mixer.music.play()
        self.bacground_music_on = True

        self.DIFFICULTY = 1
        self.GRID_SIZE = 5
        self.menu_starfields = []

    # def play_background_music(self):

    def get_settings(self):
        return self.GAME_WIDTH,self.GAME_HEIGHT,self.DIFFICULTY,self.GRID_SIZE

    def menus(self,surface):
        surface.fill((10,10,10))
        self.render_starfield(surface)
        self.make_cool_starting_mobs()
        self.render_cool_mobs(surface)

        if self.main_menu_active:
            self.main_menu(surface)
        elif self.setting_menu_active:
            self.settings_menu(surface)
        return self.game_running

    def make_cool_starting_mobs(self):
        if np.random.randint(0,1000)<=1: # and len(self.passing_mobs.info['x'])< 10:
            self.passing_mobs.spawn_mob(0,np.random.randint(0,self.GAME_HEIGHT))
        for i in range(len(self.passing_mobs.info['x'])):
            self.passing_mobs.info['speed'][i] = 1
            self.passing_mobs.info['d_pos'][i] = (self.GAME_WIDTH+200,np.random.randint(0,self.GAME_HEIGHT))
        clearing_mobs = True
        while clearing_mobs:
            for i in range(len(self.passing_mobs.info['x'])):
                if self.passing_mobs.info['x'][i]>self.GAME_WIDTH:
                    clear_dict_at_index(self.passing_mobs.info,i)
                    break
            clearing_mobs = False



    def render_cool_mobs(self,surface):
        self.passing_mobs.move()
        self.passing_mobs.render(surface)

    def make_cool_menu_starfield(self,x,y):
        if pg.time.get_ticks()%111:
            r = np.random.randint(0,150)
            g = np.random.randint(0,150)
            b = np.random.randint(100,255)
            star_field = StarField(pos=(x-25, y-25),num_stars=3, size=50,flow=True,color=(r,g,b),speed=0.2)
            self.menu_starfields.append(star_field)
        if len(self.menu_starfields)>1000:
            self.menu_starfields = self.menu_starfields[2:-1]


    def make_starfield(self):
        self.white_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,num_stars=150)
        self.red_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(50, 0, 0), num_stars=50)
        self.blue_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(10, 10, 65), num_stars=50)
        self.green_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(1, 65, 15), num_stars=25)
        self.yellow_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(65, 65, 15), num_stars=15)

    def render_starfield(self, surface):
        self.white_stars.render(surface)
        self.red_stars.render(surface)
        self.blue_stars.render(surface)
        self.green_stars.render(surface)
        self.yellow_stars.render(surface)

    def main_menu(self,surface):

        text_size = int(self.GAME_HEIGHT/8)
        font = pg.font.SysFont(self.font,text_size)
        labels = []

        for starfield in self.menu_starfields:
            starfield.render(surface)

        for i,option in enumerate(self.main_menu_options):
            label = font.render(option, 1, (200, 200, 200))
            if option == 'Load Game' or option == 'How to Play':
                label = font.render(option, 1, (115,115,115))

            lx, ly, lw, lh =self.GAME_WIDTH/2-label.get_width()/2,self.GAME_WIDTH / 9 +(i*text_size),label.get_width(),label.get_height()
            labels.append((lx, ly, lw, lh))
            surface.blit(label, [lx,ly ])



        for event in pg.event.get():

            for i in range(len(self.main_menu_options)):
                x,y = pg.mouse.get_pos()
                lx, ly, lw, lh = labels[i]
                if lx < x < lx + lw and ly < y < ly + lh:
                    self.make_cool_menu_starfield(x,y)
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0] == 1:
                x,y = pg.mouse.get_pos()
                for i in range(len(self.main_menu_options)):
                    lx, ly, lw, lh =labels[i]
                    if lx < x < lx + lw and ly < y < ly + lh:
                        if self.main_menu_options[i] == 'New Game':
                            self.main_menu_active = False
                            self.game_running = True
                        if self.main_menu_options[i] == 'Quit':
                            quit()
                        if self.main_menu_options[i] == 'Settings':
                            self.setting_menu_active = True
                            self.main_menu_active = False




    def settings_menu(self,surface):

        text_size = int(self.GAME_HEIGHT/10)
        font = pg.font.SysFont(self.font,text_size)
        labels = []

        for i,option in enumerate(self.settings_menu_options):
            label = font.render(option, 1, (200, 200, 200))
            lx, ly, lw, lh,text = self.GAME_WIDTH/2-label.get_width(),self.GAME_WIDTH / 9 +(i*text_size),label.get_width(),label.get_height(),option
            labels.append((lx, ly, lw, lh,text))
            surface.blit(label, [lx,ly])

            if option == 'Universe Size:':
                current_option_val_label = font.render(" "+str(self.GRID_SIZE), 1, (200, 200, 200))
                surface.blit(current_option_val_label, [lx+lw, ly])
            elif option == 'Difficulty:':
                diffilculty_names = ['Ensign','Lieutenant','Captain','Grand Admiral']
                r = 55*self.DIFFICULTY
                if r>255: r = 255
                current_option_val_label = font.render(" "+diffilculty_names[self.DIFFICULTY-1], 1, (r, 255-r, 255-r))
                surface.blit(current_option_val_label, [lx+lw, ly])
            elif option == 'Game Resolution:':
                current_option_val_label = font.render(str(self.GAME_WIDTH)+' x '+str(self.GAME_HEIGHT), 1, (200, 200, 200))
                surface.blit(current_option_val_label, [lx+lw, ly])
            elif option == 'Music Volume:':
                current_option_val_label = font.render(str(int(pg.mixer.music.get_volume()*100))+'%', 1, (200, 200, 200))
                surface.blit(current_option_val_label, [lx+lw, ly])
            elif option == 'Music On:':
                current_option_val_label = font.render(str(self.bacground_music_on), 1, (200, 200, 200))
                surface.blit(current_option_val_label, [lx+lw, ly])

        back_label = font.render('( Return to main menu )', 1, (155, 155, 200))
        lx, ly, lw, lh,text = self.GAME_WIDTH / 2 - back_label.get_width()/2, self.GAME_HEIGHT - back_label.get_height(), back_label.get_width(), back_label.get_height(),'( Return to main menu )'
        labels.append((lx, ly, lw, lh,text))
        surface.blit(back_label, [lx, ly])

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0] == 1:
                x,y = pg.mouse.get_pos()
                for i in range(len(labels)):
                    lx, ly, lw, lh ,text =labels[i]
                    if lx < x < lx + lw and ly < y < ly + lh:
                        if text == 'Universe Size:':
                            self.GRID_SIZE += 2
                            if self.GRID_SIZE > 11:
                                self.GRID_SIZE = 5
                        if text == 'Difficulty:':
                            self.DIFFICULTY += 1
                            if self.DIFFICULTY > 4:
                                self.DIFFICULTY = 1
                        if text == 'Game Resolution:':
                            ratio = self.GAME_WIDTH/self.GAME_HEIGHT
                            self.GAME_HEIGHT += 100
                            self.GAME_WIDTH += ratio*100

                            if self.GAME_HEIGHT> 1000:
                                self.GAME_HEIGHT = 400
                                self.GAME_WIDTH = 600
                            surface = pg.display.set_mode((int(self.GAME_WIDTH),int(self.GAME_HEIGHT)))
                        if text == 'Music On:':
                            if self.bacground_music_on == True:
                                pg.mixer.music.pause()
                                self.bacground_music_on = False
                            else:
                                # pg.mixer.music.play()
                                self.bacground_music_on = True
                        if text == 'Music Volume:':
                            if pg.mixer.music.get_volume()>=1:
                                pg.mixer.music.set_volume(0.105)
                            else:
                                pg.mixer.music.set_volume(pg.mixer.music.get_volume()+0.105)
                        if text == '( Return to main menu )':
                            self.setting_menu_active= False
                            self.main_menu_active = True


def angle_find(x1, y1, x2, y2):
    angle = 0

    if x2 > x1 and y2 > y1:
        d_x = abs_dif(x1, x2)
        d_y = abs_dif(y1, y2)
        angle = math.degrees(math.atan(d_x / (d_y + 1)))
    elif x1 > x2 and y1 > y2:
        d_x = abs_dif(x1, x2)
        d_y = abs_dif(y1, y2)
        angle = math.degrees(math.atan(d_x / (d_y + 1))) + 180
    elif x2 > x1 and y1 > y2:
        d_x = abs_dif(x1, x2)
        d_y = abs_dif(y1, y2)
        angle = math.degrees(math.atan(d_y / (d_x + 1))) + 90
    elif x1 > x2 and y2 > y1:
        d_x = abs_dif(x1, x2)
        d_y = abs_dif(y1, y2)
        angle = math.degrees(math.atan(d_y / (d_x + 1))) + 270

    return angle


def abs_dif(a, b):
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    t = a - b
    if t < 0:
        t = -t
    return t


def total_speed(a, b):
    t = math.sqrt(a ** 2 + b ** 2)
    return t


def randint(): return np.random.randint(0, 100)


def drift_physics(player_drift, change_x, change_y):
    if change_x > 0:
        change_x -= player_drift
    if change_y > 0:
        change_y -= player_drift

    if change_x < 0:
        change_x += player_drift
    if change_y < 0:
        change_y += player_drift

    return change_x, change_y


def collision(x1, y1, s1, x2, y2, s2):
    if x2 <= x1 + s1 and x2 + s2 > x1:
        if y2 <= y1 + s1 and y2 + s2 > y1:
            return True


# SAME AS PLAYER ROTATION FUNCTION BUT MORE GENERAL
def rotation_movement_math(rotation, movement_step):
    # define internal rotation var and predefine other vars
    new_rot = rotation
    change_x, change_y = 0, 0

    # make rotation var positive all the time
    if 0 > new_rot > -360:
        new_rot = 360 + rotation

    def rotation_math(rot, move_step):
        if 0 > rot > -360:
            rot = -rot

        cos_math = math.cos(math.radians(rot))
        sin_math = math.sin(math.radians(rot))

        if cos_math < 0:
            cos_math = -cos_math
        if sin_math < 0:
            sin_math = -sin_math

        x_change = math.sqrt(move_step ** 2 - (cos_math * move_step) ** 2)
        y_change = math.sqrt(move_step ** 2 - (sin_math * move_step) ** 2)

        return x_change, y_change

    # return an x and y change so that their vector sums equal the desired move step
    x_change, y_change = rotation_math(new_rot, movement_step)

    # here we say that depending on what the rotation, change x and y according to these rules
    if 360 >= new_rot > 270:
        change_y = -y_change
        change_x = +x_change
    elif 270 >= new_rot > 180:
        change_y = +y_change
        change_x = +x_change
    elif 180 >= new_rot > 90:
        change_y = +y_change
        change_x = -x_change
    elif 90 >= new_rot >= 0:
        change_y = -y_change
        change_x = -x_change

    return change_x, change_y


def is_between(num0, num1, point):
    is_between_val = False
    nums = [num0, num1]

    large_num = max(nums)
    small_num = min(nums)

    if point - small_num > 0 and point - large_num < 0:
        is_between_val = True

    return is_between_val


def is_close_enough(num0, num1, margin):
    close = False
    if abs(num0 - num1) <= margin:
        close = True

    return close


def swap_color(img_path, from_, to_):
    surf = pg.image.load(img_path).convert(32)

    arr = pg.PixelArray(surf)
    arr.replace(from_, to_)
    del arr

    pixels = pg.PixelArray(surf)
    pixels.replace(from_ + (255,), to_ + (255,))

    image = pixels.surface
    image.set_colorkey((0, 0, 0))

    return image




def pythag(x0, y0, x1, y1):
    dx = abs(x0 - x1)
    dy = abs(y0 - y1)
    dist = math.sqrt((dx * dx) + (dy * dy))

    return dist


# def place_randomly():
#     margin = 0.1
#     x = np.random.randint(GAME_WIDTH*margin, GAME_WIDTH-GAME_WIDTH*margin)
#     y = np.random.randint(GAME_HEIGHT*margin, GAME_HEIGHT-GAME_HEIGHT*margin)
#
#     return x, y


def append_to_dict_from_index(dict0, dict1, index):
    for key in dict0.keys():
        dict0[key].append(dict1[key][index])

    return dict0


class StarField():
    def __init__(self,GAME_WIDTH=None,GAME_HEIGHT=None, color=(255, 255, 255),num_stars=100, pos=None, size=None, speed=1,flow = False):
        self.flow = flow
        self.GAME_WIDTH = GAME_WIDTH
        self.GAME_HEIGHT = GAME_HEIGHT
        self.color = color
        self.pos = pos
        self.size = size
        self.num_stars = num_stars
        self.xpos, self.ypos = np.zeros(self.num_stars), np.zeros(self.num_stars)
        self.sizes = np.zeros(self.num_stars)
        self.speed = np.zeros(self.num_stars)
        self.speed_coef = speed

        for i in range(self.num_stars):
            if pos != None and size != None:
                self.xpos[i] = np.random.randint(pos[0], pos[0] + size)
                self.ypos[i] = np.random.randint(pos[1], pos[1] + size)
            elif pos != self.GAME_WIDTH and size != self.GAME_HEIGHT:
                self.xpos[i] = np.random.randint(0, self.GAME_WIDTH)
                self.ypos[i] = np.random.randint(0, self.GAME_HEIGHT)
            else:
                print('Specify parameters')
            self.sizes[i] = np.random.randint(1, 4)
            self.speed[i] = np.random.random_sample() / self.speed_coef

    def render(self, surface):
        for i in range(self.num_stars):
            self.xpos[i] += self.speed[i]
            if self.flow:
                pass
            elif self.pos == None:
                if self.xpos[i] > self.GAME_WIDTH:
                    self.xpos[i] = 0
            elif self.pos != None:
                if self.xpos[i] > self.pos[0] + self.size:
                    self.xpos[i] = self.pos[0]

            rectangle = (self.xpos[i], self.ypos[i], self.sizes[i], self.sizes[i])
            pg.draw.rect(surface, self.color, rectangle, )


class DrawBoxes():
    blue = (6, 151, 176)

    def __init__(self):
        self.first_point = False
        self.first_pos_x, self.first_pos_y = 0, 0
        self.box_w, self.box_h = 0, 0

    def game_loop(self, event, surface, return_start=False):

        if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[0] == 1:
            if self.first_point == False:
                self.first_point = True
                self.first_pos_x, self.first_pos_y = pg.mouse.get_pos()

        if self.first_point:
            current_x, current_y = pg.mouse.get_pos()
            self.box_w, self.box_h = current_x - self.first_pos_x, current_y - self.first_pos_y

        if event.type == pg.MOUSEBUTTONUP:
            self.first_point = False
            self.first_pos_x, self.first_pos_y = 0, 0
            self.box_w, self.box_h = 0, 0

        if return_start:
            return self.first_pos_x, self.first_pos_y, self.first_point

    def render(self, surface):
        rectangle = (self.first_pos_x, self.first_pos_y, self.box_w, self.box_h)
        pg.draw.rect(surface, self.blue, rectangle, 1)


class Mobs():
    green = (0, 200, 0)
    black = (0, 0, 0)

    mask_color = (255, 174, 201)

    basic_ship_path = 'images/basic_ship.png'

    def __init__(self, GAME_WIDTH,GAME_HEIGHT,color=(200, 170, 30)):
        self.ship_color = color
        self.GAME_HEIGHT = GAME_HEIGHT
        self.GAME_WIDTH = GAME_WIDTH

        self.set_shoot_dir = None
        self.size = 50, 50
        self.scaling_factor = (1200/self.GAME_WIDTH)
        self.clear()
        self.movement = False
        # self.original_image = pg.image.load('images/basic_ship.png').convert(32)
        # self.original_image = pg.transform.smoothscale((self.size[0]*self.scaling_factor,self.size[0]*self.scaling_factor))
        self.image = swap_color(self.basic_ship_path, self.mask_color, self.ship_color)
        self.image = pg.transform.smoothscale(self.image,(int(self.size[0]*self.scaling_factor),int(self.size[0]*self.scaling_factor)))

        self.selected_image = swap_color(self.basic_ship_path, self.mask_color, self.green)
        self.selected_image = pg.transform.smoothscale(self.selected_image,(int(self.size[0]*self.scaling_factor),int(self.size[0]*self.scaling_factor)))

        self.bullets = {'pos': [],
                        'dest': [],
                        'cpos': [],
                        'ship_index': [],
                        'damage': []}
        self.sprite_clock = 0
        self.anim_speed = 5  # higher numbers go slower

        self.boss_ship_image = pg.image.load('images/boss_ship.png').convert(32)
        self.boss_ship_image = pg.transform.scale(swap_color('images/boss_ship.png', self.mask_color, self.ship_color), (70, 70))
        self.boss_ship_image_selected = pg.transform.scale(swap_color('images/boss_ship.png', self.mask_color, self.green), (70, 70))

    def clear(self):
        self.info = {'x': [], 'y': [],
                     'd_pos': [],
                     'speed': [],
                     'damage': [],
                     'img': [],
                     'selected_img': [],
                     'selected': [],
                     'shoot_dir': [],
                     'hull0': [], 'hull1': [],
                     'crew0': [], 'crew1': [],
                     'affects': [],
                     'kills': [],
                     'control_mode': [],
                     'energy': [],
                     'available_buildings': []}

    def spawn_mob(self, x, y, ship_type=None):

        if ship_type == None:
            # random speed number
            speed = np.random.random()
            if speed < 0.3:
                speed = 0.3

            # setup vars
            self.info['x'].append(x), self.info['y'].append(y)
            self.info['d_pos'].append((x, y))
            self.info['speed'].append(speed)
            self.info['damage'].append((3, 10))
            self.info['img'].append(self.image)
            self.info['selected'].append(False)
            self.info['selected_img'].append(self.selected_image)
            self.info['shoot_dir'].append(None)
            self.info['affects'].append(set())
            self.info['kills'].append(0)
            self.info['control_mode'].append(0)
            self.info['available_buildings'].append(set())
            self.info['energy'].append(np.random.randint(100, 300))

            # control modes
            # 0 = manual
            # 1 = simple autonomous

            # vessel stats
            hull = np.random.randint(10, 100)
            crew = np.random.randint(5, 15)

            self.info['hull0'].append(hull), self.info['hull1'].append(hull)
            self.info['crew0'].append(crew), self.info['crew1'].append(crew)

            self.xs = np.array(self.info['x'])
            self.ys = np.array(self.info['y'])
        elif ship_type == 'boss':
            # random speed number
            speed = np.random.random() * 1.3
            if speed < 0.6:
                speed = 0.6

            # setup vars
            self.info['x'].append(x), self.info['y'].append(y)
            self.info['d_pos'].append((x, y))
            self.info['speed'].append(speed)
            self.info['damage'].append((20, 30))
            self.info['img'].append(self.boss_ship_image)
            self.info['selected_img'].append(self.boss_ship_image_selected)
            self.info['selected'].append(False)
            self.info['shoot_dir'].append(None)
            self.info['affects'].append(set())
            self.info['kills'].append(10)
            self.info['control_mode'].append(0)
            self.info['available_buildings'].append(set())
            self.info['energy'].append(np.random.randint(200, 500))

            # control modes

            # vessel stats
            hull = np.random.randint(300, 450)
            crew = np.random.randint(100, 125)

            self.info['hull0'].append(hull), self.info['hull1'].append(hull)
            self.info['crew0'].append(crew), self.info['crew1'].append(crew)

            self.xs = np.array(self.info['x'])
            self.ys = np.array(self.info['y'])

    def detect_selection(self, start_x, start_y, button):
        current_x, current_y = pg.mouse.get_pos()

        if button == True:
            if start_x != None and start_y != None:
                for i in range(len(self.info['x'])):
                    x, y = self.info['x'][i], self.info['y'][i]

                    if is_between(start_x, current_x, x) and is_between(start_y, current_y, y):
                        self.info['selected'][i] = True
                        self.info['img'][i] = self.selected_image

    def detect_clicked(self, x, y):
        for i in range(len(self.info['x'])):
            w = self.info['img'][i].get_width()
            sx,sy = self.info['x'][i], self.info['y'][i]
            if sx<x<sx+w and sy<y<sy+w:
                self.info['selected'][i] = True
                self.info['img'][i] = self.selected_image

    def detect_bullet_collision(self, mob_object, return_kill_credits=None):
        kill_credits = 0
        for i in range(len(self.info['x'])):
            for j in range(len(mob_object.bullets['pos'])):
                bx, by = mob_object.bullets['pos'][j]

                try:
                    w = self.info['img'][i].get_width()
                    sx,sy = self.info['x'][i],self.info['y'][i]
                    if sx<bx<sx+w and sy<by<sy+w:
                        min_damage, max_damage = mob_object.bullets['damage'][j]
                        self.info['hull1'][i] -= np.random.randint(min_damage, max_damage)
                        self.info['speed'][i] -= 0.01

                        frac_remaining_hull = (self.info['hull1'][i] / self.info['hull0'][i]) * 100
                        if 0 < frac_remaining_hull < 20:
                            self.info['crew1'][i] -= np.random.randint(0, 4)
                        elif 20 < frac_remaining_hull < 50:
                            self.info['crew1'][i] -= np.random.randint(0, 3)
                        else:
                            self.info['crew1'][i] -= np.random.randint(0, 2)

                        mob_object.bullets['pos'][j] = (-1000, -1000)

                        if self.info['hull1'][i] <= 0:
                            self.info = clear_dict_at_index(self.info, i)
                            mob_object.info['kills'][mob_object.bullets['ship_index'][j]] += 1
                            kill_credits += np.random.randint(0, 200)

                            break
                        if self.info['speed'][i] <= 0:
                            self.info['speed'][i] = 0
                        if self.info['crew1'][i] <= 0:
                            self.info['crew1'][i] = 0
                            self.info['affects'][i].add('crew_dead')
                        if randint() > 90:
                            self.info['affects'][i].add('on_fire')


                except IndexError:
                    pass

        if return_kill_credits != None:
            return kill_credits

    def detect_warpable_ships(self):
        warpable = 0

        for i in range(len(self.info['x'])):
            if self.info['energy'][i] > 30 and self.info['selected'][i] and not self.info['affects'].__contains__('crew_dead'):
                warpable += 1
        return warpable

    def detect_available_planets(self, planets_object):
        for j in range(len(self.info['x'])):

            for i in range(len(planets_object.planets['buildings'])):
                px, py = planets_object.planets['pos'][i]
                mx, my = self.info['x'][j], self.info['y'][j]
                size = (planets_object.sprite_size*planets_object.planets['scale'][i])

                if px<mx<px+size and py<my<py+size and self.info['selected'][j]:
                    self.info['available_buildings'][j] = planets_object.planets['buildings'][i]
                if not px<mx<px+size and not px<mx<px+size and not self.info['selected'][j]:
                    self.info['available_buildings'][j] = set()



    def place_randomly(self):
        margin = 0.1
        x = np.random.randint(self.GAME_WIDTH*margin, self.GAME_WIDTH-self.GAME_WIDTH*margin)
        y = np.random.randint(self.GAME_HEIGHT*margin, self.GAME_HEIGHT-self.GAME_HEIGHT*margin)

        return x, y

    def unselect(self):
        for i in range(len(self.info['selected'])):
            self.info['selected'][i] = False
            self.info['img'][i] = self.image

    def move_pos(self, x_pos, y_pos):
        self.move_pos_x, self.move_pos_y = x_pos, y_pos

        for i in range(len(self.info['x'])):
            if self.info['control_mode'] == 1:
                pass

            elif self.info['selected'][i]:
                self.info['d_pos'][i] = (x_pos, y_pos)

    def stop(self):
        for i in range(len(self.info['x'])):
            if self.info['selected'][i]:
                self.info['d_pos'][i] = self.info['x'][i], self.info['y'][i]

    def move(self):
        self.sprite_clock += 1
        if self.sprite_clock > 7 * self.anim_speed:
            self.sprite_clock = 0

        def mob_collision(x0, y0, x1, y1):
            collision = False
            if is_close_enough(x0, x1, self.size[0]) and is_close_enough(y0, y1, self.size[1]):
                collision = True

            return collision

        ships_destroyed = True
        while ships_destroyed:
            for i in range(len(self.info['x'])):

                # process stuff that happens to ships
                if self.info['affects'][i].__contains__('crew_dead'):
                    self.info['speed'][i] = 0
                if self.info['affects'][i].__contains__('on_fire'):
                    if randint() >= 99:
                        self.info['hull1'][i] -= np.random.randint(0, 10)

                # if there is crew, do stuff
                if self.info['crew1'][i] > 0:
                    precent_crew_remaining = (self.info['crew1'][i] / self.info['crew0'][i]) * 100

                    # put out fires
                    if np.random.randint(0, 100000) < precent_crew_remaining and self.info['affects'][i].__contains__('on_fire'):
                        self.info['affects'][i].remove('on_fire')

                    # repair hull
                    if randint() < precent_crew_remaining * 0.000001 and self.info['hull1'][i] < self.info['hull0'][i]:
                        self.info['hull1'][i] += self.info['crew1'][i] * np.random.randint(0, 2)
                        if self.info['hull1'][i] > self.info['hull0'][i]:
                            self.info['hull1'][i] = self.info['hull0'][i]

                x, y = self.info['x'][i], self.info['y'][i]
                d_x, d_y = self.info['d_pos'][i]
                speed = self.info['speed'][i]

                t_xs, t_ys = np.delete(self.xs, i), np.delete(self.ys, i)

                cx, cy = 0, 0

                if x != d_x and y != d_y:
                    cx, cy = rotation_movement_math(angle_find(x, y, d_x, d_y), speed)
                    x, y = x - cx, y - cy

                for j in range(len(t_xs)):
                    if mob_collision(x, y, t_xs[j], t_ys[j]):
                        x, y = x + cx, y + cy

                self.info['x'][i], self.info['y'][i] = x, y

                if is_close_enough(x, d_x, 3) and is_close_enough(y, d_y, 3):
                    self.info['d_pos'][i] = (x, y)

                self.xs[i], self.ys[i] = x, y

                if self.info['hull1'][i] < 0:
                    self.info = clear_dict_at_index(self.info, i)
                    break
            ships_destroyed = False

    def render(self, surface):
        for i in range(len(self.info['x'])):
            x, y = self.info['x'][i], self.info['y'][i]
            surface.blit(self.info['img'][i], [x, y])
            if self.info['selected'][i]:
                # show health bar
                w = self.info['img'][i].get_width()
                health_bar_red_rect = (x , y, w, 2)
                pg.draw.rect(surface, (255, 0, 0), health_bar_red_rect)
                length = (self.info['hull1'][i] / self.info['hull0'][i]) * w
                health_bar_status_rect = (x , y, length, 2)
                pg.draw.rect(surface, (0, 255, 0), health_bar_status_rect)

                # show crew remaining
                crew_bar_blue_rect = (x, y - 4, w, 2)
                pg.draw.rect(surface, (25, 25, 55), crew_bar_blue_rect)
                length = (self.info['crew1'][i] / self.info['crew0'][i]) * w
                crew_bar_status_rect = (x, y - 4, length, 2)
                pg.draw.rect(surface, (125, 125, 155), crew_bar_status_rect)

                if self.info['energy'][i] < 200:
                    alert_image = pg.image.load('images/alert.png').convert(32)
                    aw = alert_image.get_width()
                    alert_image.set_colorkey((0, 0, 0))
                    if self.info['energy'][i] < 30:
                        alert_image = swap_color('images/alert.png', (181, 87, 181), (255, 13, 19))
                    surface.blit(alert_image, [(x - aw), y - aw+15])
                if self.info['control_mode'][i] == 1:
                    autonomous_image = pg.image.load('images/chevron.png').convert(32)
                    aw = autonomous_image.get_width()

                    autonomous_image.set_colorkey((0, 0, 0))
                    surface.blit(autonomous_image, [(x - aw), (y - aw) + 30])

            if self.info['affects'][i].__contains__('on_fire'):
                w = self.info['img'][i].get_width()
                fire_image = self.animate_fire()
                fire_image0 = pg.transform.smoothscale(fire_image, (8, 8))
                surface.blit(fire_image0, [(x + w / 2) + 6, (y + w / 2) - 4])

                if (self.info['hull1'][i] / self.info['hull0'][i]) < 0.25:
                    fire_image3 = pg.transform.smoothscale(fire_image, (17, 17))

                    surface.blit(fire_image3, [(x + w / 2) - 20, (y + w / 2) - 13])

                if (self.info['hull1'][i] / self.info['hull0'][i]) < 0.75:
                    fire_image2 = pg.transform.flip(fire_image, True, False)
                    fire_image2 = pg.transform.smoothscale(fire_image2, (15, 15))
                    surface.blit(fire_image2, [(x + w / 2) - 14, (y + w / 2)])

                if (self.info['hull1'][i] / self.info['hull0'][i]) < 0.50:
                    fire_image4 = pg.transform.smoothscale(fire_image, (12, 12))
                    surface.blit(fire_image4, [(x + w / 2) + 6, (y + w / 2) + 2])

    def animate_fire(self):
        fire_image = pg.image.load('images/fire.png').convert(32)
        fire_image.set_colorkey((0, 0, 0))
        fire_clock = int((self.sprite_clock / (8 * self.anim_speed)) * 8)
        return fire_image.subsurface(16 * fire_clock, 0, 16, 16)

    def get_num(self):
        return len(self.info['x'])

    def get_ship_attributes(self):
        num_selected_ships = 0
        ship_attributes = {'ship_speed': 0,
                           'hull0': 0,
                           'hull1': 0,
                           'crew0': 0,
                           'crew1': 0,
                           'affects': [],
                           'kills': [],
                           'energy': 0,
                           'available_buildings': 0}

        for i in range(len(self.info['x'])):
            if self.info['selected'][i]:
                num_selected_ships += 1
                ship_attributes['ship_speed'] = self.info['speed'][i]
                ship_attributes['hull0'] = self.info['hull0'][i]
                ship_attributes['hull1'] = self.info['hull1'][i]
                ship_attributes['crew0'] = self.info['crew0'][i]
                ship_attributes['crew1'] = self.info['crew1'][i]
                ship_attributes['affects'] = self.info['affects'][i]
                ship_attributes['kills'] = self.info['kills'][i]
                ship_attributes['energy'] = self.info['energy'][i]
                ship_attributes['available_buildings'] = self.info['available_buildings'][i]

        if num_selected_ships == 1:
            return ship_attributes
        else:
            return None

    def shoot_dir(self, x, y):
        sx, sy = x, y
        for i in range(len(self.info['x'])):
            if self.info['selected'][i] and not self.info['affects'][i].__contains__('crew_dead') and self.info['energy'][i] > 5:
                w = self.info['img'][i].get_width()/2
                self.info['shoot_dir'][i] = (sx , sy )
                self.bullets['pos'].append((self.info['x'][i] + w, self.info['y'][i] + w))
                self.bullets['dest'].append((self.info['shoot_dir'][i]))
                x, y = self.info['x'][i], self.info['y'][i]
                xf, yf = self.info['shoot_dir'][i]
                kills = self.info['kills'][i]
                if kills > 0:
                    imprecision_factor = 30 / kills
                else:
                    imprecision_factor = 40
                mod_x, mod_y = np.random.randint(-imprecision_factor, imprecision_factor+1), np.random.randint(-imprecision_factor, imprecision_factor+1)
                off_x, off_y = xf+mod_x, yf+mod_y
                self.bullets['cpos'].append((rotation_movement_math(angle_find(x, y, off_x, off_y), 5)))
                self.bullets['ship_index'].append(i)
                self.bullets['damage'].append(self.info['damage'][i])
                self.info['shoot_dir'][i] = None
                self.info['energy'][i] -= 2

    def change_autonomous(self):
        for i in range(len(self.info['x'])):
            if self.info['selected'][i] and self.info['control_mode'][i] == 1:
                self.info['control_mode'][i] = 0
                self.info['d_pos'][i] = self.info['x'][i], self.info['y'][i]
            elif self.info['selected'][i]:
                self.info['control_mode'][i] = 1

    def render_shots(self, surface):

        # find any shots out of frame
        shots_out_of_frame = True

        while shots_out_of_frame:
            if len(self.bullets['pos']) > 0:
                for i in range(len(self.bullets['pos'])):
                    x, y = self.bullets['pos'][i]

                    if x < 0 or x > self.GAME_WIDTH:
                        clear_dict_at_index(self.bullets, i)
                        break

                    if y < 0 or y > self.GAME_HEIGHT:
                        clear_dict_at_index(self.bullets, i)
                        break

                    else:
                        shots_out_of_frame = False
            else:
                shots_out_of_frame = False

        for i in range(len(self.bullets['pos'])):
            x, y = self.bullets['pos'][i]
            change_x, change_y = self.bullets['cpos'][i]
            self.bullets['pos'][i] = x - change_x, y - change_y

            rectangle = (x, y, 3, 3)
            pg.draw.rect(surface, (215, 215, 40), rectangle)

    def fire(self, x0, y0, x1, y1, kills, damage):
        self.bullets['pos'].append((x0 + self.size[0], y0 + self.size[0]))

        if kills > 0:
            imprecision_factor = 30 / kills
        else:
            imprecision_factor = 40

        mod_x, mod_y = np.random.randint(-imprecision_factor, imprecision_factor), np.random.randint(-imprecision_factor, imprecision_factor)
        off_x, off_y = x1+ mod_x, y1 + mod_y
        self.bullets['dest'].append((off_x, off_y))
        self.bullets['cpos'].append((rotation_movement_math(angle_find(x0, y0, off_x, off_y), 3)))
        self.bullets['ship_index'].append(0)
        self.bullets['damage'].append(damage)

    def simple_ai(self, hostile_mobs, always_true=False, ):

        for i in range(len(self.info['x'])):

            if self.info['control_mode'][i] == 1 or always_true:
                if self.info['crew1'][i] > 0:
                    x, y = self.info['x'][i], self.info['y'][i]

                    if 100 >= randint() > 98:  # move the ship in a random direction
                        self.info['d_pos'][i] = self.place_randomly()

                    if 98 > randint() > 96:  # fire
                        score = self.GAME_WIDTH
                        sx, sy = 0, 0

                        if randint() > 30:  # fire at specific target
                            for m in range(len(hostile_mobs.info['x'])):
                                dist = pythag(x, y, hostile_mobs.info['x'][m], hostile_mobs.info['y'][m])
                                if dist < score:
                                    score = dist
                                    sx, sy = hostile_mobs.info['x'][m], hostile_mobs.info['y'][m]
                        else:  # fire at a random target
                            if len(hostile_mobs.info['x']) > 0:
                                random_target = np.random.randint(0, len(hostile_mobs.info['x']))
                                sx, sy = hostile_mobs.info['x'][random_target], hostile_mobs.info['y'][random_target]

                        if len(hostile_mobs.info['x']) > 0 and self.info['energy'][i] > 0:
                            self.info['energy'][i] -= 1
                            self.fire(x, y, sx, sy, self.info['kills'][i], self.info['damage'][i])


            else:
                pass


class Planets():
    black = (0, 0, 0)

    def __init__(self):

        self.sprite_size = 50 #*(1200/self.GAME_WIDTH)
        self.anim_speed = 0.1
        self.anim_frames = 60
        self.anim_counter = 0
        self.clear()
        self.ship_over_planet = False

    def detect_ships(self,mobs_object):
        self.ship_over_planet = False
        for i in range(len(mobs_object.info['x'])):
            for j in range(len(self.planets['pos'])):
                sx,sy, = mobs_object.info['x'][i],mobs_object.info['y'][i]
                px,py = self.planets['pos'][j]
                pw = self.planets['scale'][j]*50

                if px<sx<px+pw and py<sy<py+pw:
                    self.ship_over_planet = True
                    break
        # self.ship_over_planet = False
        # print(self.ship_over_planet)

    def spawn_planet(self, x, y):
        planet_path = './images/planets/'
        available_images = os.listdir(planet_path)
        image = pg.image.load(planet_path + available_images[np.random.randint(0, len(available_images))]).convert(32)
        image.set_colorkey(self.black)
        self.planets['pos'].append((x, y))
        self.planets['img'].append(image)
        self.planets['scale'].append(np.random.randint(1, 5))
        self.planets['anim_count'].append(0)
        self.planets['selected'].append(False)
        self.planets['population'].append(np.random.randint(10, 10000))
        # self.planets['explored'].append(False)
        # self.planets['event_ID'].append(0)

        dev_stage = np.random.randint(0, 4)
        buildings = ['power_plant', 'crew_barracks', 'ship_yard', 'engineering_complex']

        self.planets['development_stage'].append(dev_stage)
        if dev_stage == 0:
            self.planets['buildings'].append(set())
        else:
            planet_buildings = []
            for i in range(1, dev_stage):
                r_num = np.random.randint(0, len(buildings))
                planet_buildings.append(buildings[r_num])

            self.planets['buildings'].append(set(planet_buildings))

    def clear(self):
        self.planets = {'pos': [],
                        'img': [],
                        'scale': [],
                        'anim_count': [],
                        'selected': [],
                        'population': [],
                        'development_stage': [],
                        'buildings': [],}
                        # 'event_ID':[],
                        # 'explored':[]}
        # 'discovered':[],
        # 'event_ID':[]}

    def detect_clicked(self, x, y):
        for i in range(len(self.planets['selected'])):
            s = self.planets['scale'][i] * self.sprite_size
            if is_close_enough(x - s / 2, self.planets['pos'][i][0], s / 2) and is_close_enough(y - s / 2, self.planets['pos'][i][1], s / 2):
                self.planets['selected'][i] = True

    def render(self, surface):

        for i in range(len(self.planets['pos'])):
            size = self.sprite_size
            image = self.planets['img'][i]
            x, y = self.planets['pos'][i]
            anim_counter = self.planets['anim_count'][i]
            image_section = image.subsurface(size, 0, size, size)

            self.planets['anim_count'][i] += self.anim_speed
            if self.planets['anim_count'][i] >= self.anim_frames:
                self.planets['anim_count'][i] = 0

            if 5.5 >= anim_counter > 0:
                image_section = image.subsurface(size, 0, size, size)
            elif 11 >= anim_counter > 5.5:
                image_section = image.subsurface(size * 2, 0, size, size)
            elif 16.5 >= anim_counter > 11:
                image_section = image.subsurface(size * 3, 0, size, size)
            elif 22 >= anim_counter > 16.5:
                image_section = image.subsurface(size * 4, 0, size, size)
            elif 27.5 >= anim_counter > 22:
                image_section = image.subsurface(size * 5, 0, size, size)
            elif 33 >= anim_counter > 27.5:
                image_section = image.subsurface(0, size, size, size)
            elif 38.5 >= anim_counter > 33:
                image_section = image.subsurface(size, size, size, size)
            elif 44 >= anim_counter > 38.5:
                image_section = image.subsurface(size * 2, size, size, size)
            elif 49.5 >= anim_counter > 44:
                image_section = image.subsurface(size * 3, size, size, size)
            elif 55 >= anim_counter > 49.5:
                image_section = image.subsurface(size * 4, size, size, size)
            elif 60 >= anim_counter > 55:
                image_section = image.subsurface(size * 5, size, size, size)

            planet_scale = self.planets['scale'][i]
            scaled_image = pg.transform.scale(image_section, (size * planet_scale, size * planet_scale))

            surface.blit(scaled_image, [x, y])

    def deselect(self):
        for i in range(len(self.planets['selected'])):
            if self.planets['selected'][i]:
                self.planets['selected'][i] = False

    def get_num(self):
        return len(self.planets['pos'])

    def get_planet_attributes(self):
        planet_attributes = {'population': 0, 'development_stage': 0, 'buildings': set()}
        for i in range(len(self.planets['selected'])):
            if self.planets['selected'][i]:
                planet_attributes['population'] = self.planets['population'][i]
                planet_attributes['buildings'] = self.planets['buildings'][i]
                planet_attributes['development_stage'] = self.planets['development_stage'][i]

                return planet_attributes

        return None


class Universe():
    def __init__(self,GAME_HEIGHT= 800,GAME_WIDTH=1200,DIFFICULTY=2 ,GRID_SIZE = 5):
        self.GAME_HEIGHT = GAME_HEIGHT
        self.GAME_WIDTH = GAME_WIDTH
        self.DIFFICULTY = DIFFICULTY
        self.grid_size = GRID_SIZE
        self.num_grids = self.grid_size * self.grid_size
        self.clear()
        self.make_starfield()
        self.ui = Game_UI(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT)
        self.boxes = DrawBoxes()
        self.waypoints = Waypoints()
        self.current_grid_coords = (int(self.grid_size / 2), int(self.grid_size / 2))
        self.generate_universe()
        self.ui.make_starmap(self.grids)

        self.player_stats = {'currency': int(1000/self.DIFFICULTY)}


    def random_planets(self):
        val = np.random.randint(0, 4)
        return val

    def clear(self):
        self.empty_grids = {'pos': [], 'planets': [], 'mobs': [], 'enemy_mobs': [], 'starfields': [], 'discovered': []}
        self.grids = self.empty_grids

    def place_randomly(self):
        margin = 0.1
        x = np.random.randint(self.GAME_WIDTH*margin, self.GAME_WIDTH-self.GAME_WIDTH*margin)
        y = np.random.randint(self.GAME_HEIGHT*margin, self.GAME_HEIGHT-self.GAME_HEIGHT*margin)

        return x, y

    def random_enemies(self, max):
        if max > 0:
            val = np.random.randint(0, max) * 2
            val += 1
            return val
        else:
            return 0

    def random_friendlies(self):
        val = 0
        if randint() > 50:
            val = np.random.randint(0, 3)
        return val

    def generate_universe(self):

        cx, cy = self.current_grid_coords
        spawned_boss = False
        max_distance_from_center = pythag(cx,cy,0,0)

        for i in range(self.grid_size):
            for j in range(self.grid_size):


                distance_from_center = pythag(cx,cy,i,j)


                planets, mobs, enemy_mobs = Planets(), Mobs(GAME_HEIGHT=self.GAME_HEIGHT,GAME_WIDTH=self.GAME_WIDTH), Mobs(color=(200, 0, 50),GAME_HEIGHT=self.GAME_HEIGHT,GAME_WIDTH=self.GAME_WIDTH)
                self.grids['pos'].append((i, j))

                for l in range(self.random_planets()):
                    planets.spawn_planet(*self.place_randomly())

                # add a friendly ship at the start of the game
                if distance_from_center == 0:
                    for l in range(1):
                        mobs.spawn_mob(*self.place_randomly())
                else:
                    # add random friendlies
                    for l in range(self.random_friendlies()):
                        mobs.spawn_mob(*self.place_randomly())

                # add random enemies depending on distance from the center
                for l in range(self.random_enemies(int(distance_from_center*self.DIFFICULTY))):
                    enemy_mobs.spawn_mob(*self.place_randomly())

                if max_distance_from_center >= distance_from_center-1 and not spawned_boss:
                    if randint() > 0:
                        enemy_mobs.spawn_mob(*self.place_randomly(), ship_type='boss')

                        spawned_boss = True

                    elif i == self.grid_size-1 and j == self.grid_size-1 and not spawned_boss:
                        enemy_mobs.spawn_mob(*self.place_randomly(), ship_type='boss')
                        spawned_boss = True


                self.grids['planets'].append(planets)
                self.grids['mobs'].append(mobs)
                self.grids['enemy_mobs'].append(enemy_mobs)
                self.grids['starfields'].append(StarField(color=(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)),GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT))
                self.grids['discovered'].append(False)

    def make_starfield(self):
        self.white_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,num_stars=50)
        self.red_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(50, 0, 0), num_stars=25)
        self.blue_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(10, 10, 65), num_stars=25)
        self.green_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(1, 65, 15), num_stars=10)
        self.yellow_stars = StarField(GAME_WIDTH=self.GAME_WIDTH,GAME_HEIGHT=self.GAME_HEIGHT,color=(65, 65, 15), num_stars=10)

    def render_starfield(self, surface):
        self.white_stars.render(surface)
        self.red_stars.render(surface)
        self.blue_stars.render(surface)
        self.green_stars.render(surface)
        self.yellow_stars.render(surface)

    def move_grids(self, target_grid):
        destination_grid = self.load_grid(target_grid)

        moving_ships = True

        while moving_ships:
            if len(self.loaded_grid['mobs'].info['x']) == 0:
                moving_ships = False
            else:
                for i in range(len(self.loaded_grid['mobs'].info['x'])):
                    if self.loaded_grid['mobs'].info['selected'][i] and self.loaded_grid['mobs'].info['crew1'][i] > 0 and self.loaded_grid['mobs'].info['energy'][i] > 30:
                        self.loaded_grid['mobs'].info['energy'][i] -= 30
                        destination_grid['mobs'].info = append_to_dict_from_index(destination_grid['mobs'].info, self.loaded_grid['mobs'].info, i)
                        self.loaded_grid['mobs'].info = clear_dict_at_index(self.loaded_grid['mobs'].info, i)

                        break
                    elif i == len(self.loaded_grid['mobs'].info['x']) - 1:
                        moving_ships = False

        self.save_grid()
        self.current_grid_coords = target_grid
        self.load_grid()

    def handle_event(self, surface):
        surface.fill((0, 0, 0))
        self.loaded_grid = self.load_grid(self.current_grid_coords)
        mobs = self.loaded_grid['mobs']
        enemy_mobs = self.loaded_grid['enemy_mobs']
        planets = self.loaded_grid['planets']
        self.make_save = False

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                quit()
            mouse_pos = pg.mouse.get_pos()
            box_start_x, box_start_y, button_down = self.boxes.game_loop(event, surface, return_start=True)

            mobs.detect_selection(box_start_x, box_start_y, button_down)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_i:
                    mobs.spawn_mob(*mouse_pos)
                    # mobs.spawn_mob2(*mouse_pos)

                if event.key == pg.K_o:
                    enemy_mobs.spawn_mob(*mouse_pos)

                if event.key == pg.K_p:
                    planets.spawn_planet(*mouse_pos)

                if event.key == pg.K_a:
                    mobs.shoot_dir(*mouse_pos)

                if event.key == pg.K_c:
                    mobs.clear()
                    planets.clear()

                if event.key == pg.K_m:
                    self.make_save = True
                    # mobs.stop()

                if event.key == pg.K_s:
                    mobs.stop()

                if event.key == pg.K_q:
                    mobs.change_autonomous()

                if event.key == pg.K_w:
                    if self.ui.star_map_active:
                        self.ui.star_map_active = False
                    else:
                        self.ui.star_map_active = True

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2] == 1:
                mobs.move_pos(*mouse_pos)

                self.waypoints.set_move_waypoint(*mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0] == 1:

                planets.deselect()
                planets.detect_clicked(*mouse_pos)

                self.ui.detect_clicked_grid()
                grid_selection = self.ui.selected_grid

                if grid_selection != None:
                    if grid_selection != self.current_grid_coords:
                        self.move_grids(grid_selection)

                    self.current_grid_coords = grid_selection
                ui_clicked, credit_delta = self.ui.detect_if_clicked(*mouse_pos)
                self.player_stats['currency'] = self.player_stats['currency'] + credit_delta

                if not ui_clicked:
                    mobs.unselect()

                mobs.detect_clicked(*mouse_pos)

    def render_grid(self, surface):

        self.loaded_grid['starfields'].render(surface)
        self.loaded_grid['planets'].render(surface)
        self.loaded_grid['planets'].detect_ships(self.loaded_grid['mobs'])


        self.render_starfield(surface)

        self.loaded_grid['enemy_mobs'].simple_ai(self.loaded_grid['mobs'], always_true=True)
        self.loaded_grid['enemy_mobs'].move()
        self.loaded_grid['enemy_mobs'].render_shots(surface)
        self.loaded_grid['enemy_mobs'].render(surface)
        self.player_stats['currency'] += self.loaded_grid['enemy_mobs'].detect_bullet_collision(self.loaded_grid['mobs'], return_kill_credits=True)

        self.loaded_grid['mobs'].detect_available_planets(self.loaded_grid['planets'])
        self.loaded_grid['mobs'].simple_ai(self.loaded_grid['enemy_mobs'])
        self.loaded_grid['mobs'].move()
        self.loaded_grid['mobs'].render_shots(surface)
        self.loaded_grid['mobs'].render(surface)
        self.loaded_grid['mobs'].detect_bullet_collision(self.loaded_grid['enemy_mobs'])

        self.boxes.render(surface)
        self.waypoints.render(surface)

        self.ui.render_hud(surface,
                           ships=self.loaded_grid['mobs'].get_num(),
                           ship_atrributes=self.loaded_grid['mobs'].get_ship_attributes(),
                           planet_attributes=self.loaded_grid['planets'].get_planet_attributes(),
                           player_stats=self.player_stats)

    def load_grid(self, spos=None):
        loaded_grid = {'pos': None, 'planets': None, 'mobs': None, 'enemy_mobs': None}

        if spos != None:
            pos = spos
        else:
            pos = self.current_grid_coords

        index = self.grids['pos'].index(pos)
        self.grids['discovered'][index] = True

        for key in self.grids.keys():
            loaded_grid[key] = self.grids[key][index]
        loaded_grid['mobs'].xs = np.array(loaded_grid['mobs'].info['x'])
        loaded_grid['mobs'].ys = np.array(loaded_grid['mobs'].info['y'])

        if spos != None:
            return loaded_grid
        else:
            self.loaded_grid = loaded_grid

    def save_grid(self, grid=None):

        if grid != None:
            index = self.grids['pos'].index(grid['pos'])
            for key in self.grids.keys():
                self.grids[key][index] = grid[key]
            self.grids['mobs'][index].xs = np.array(grid['mobs'].info['x'])
            self.grids['mobs'][index].ys = np.array(grid['mobs'].info['y'])

        else:
            index = self.grids['pos'].index(self.current_grid_coords)
            for key in self.grids.keys():
                self.grids[key][index] = self.loaded_grid[key]


class Game_UI():

    def __init__(self,GAME_HEIGHT,GAME_WIDTH):
        # setup
        self.GAME_HEIGHT =GAME_HEIGHT
        self.GAME_WIDTH = GAME_WIDTH
        self.text_size = 16
        self.boarder_screen_offset = 3
        self.bottom_area_offset = self.GAME_HEIGHT / 6
        all_fonts = pg.font.get_fonts()
        self.player_stats = None
        if all_fonts.__contains__('helveticattc'):
            self.font = all_fonts[all_fonts.index('helveticattc')]
        else:
            self.font = all_fonts[0]

        self.pad = 25 * (self.GAME_HEIGHT / 1200)
        self.star_map_active = False
        self.grids = None

        # colors
        self.light_grey = (155, 155, 155)
        self.dark_grey = (75, 75, 75)
        self.darker_grey = (25, 25, 25)
        self.map_size = int(self.GAME_HEIGHT / 1.2)
        self.starmap_grid_screen = {'pixel_pos': [], 'grid_pos': [], 'starfields': [], 'color': []}

        # images
        self.buy_image_1 = pg.image.load('images/buy1.png').convert(32)
        self.buy_image_1.set_colorkey((0, 0, 0))
        self.buy_image_1_flipped = pg.transform.flip(self.buy_image_1, True, False)
        self.buy_image_10 = pg.image.load('images/buy10.png').convert(32)
        self.buy_image_10.set_colorkey((0, 0, 0))
        self.buy_image_10_flipped = pg.transform.flip(self.buy_image_10, True, False)

        self.buy_image_width = self.buy_image_1.get_width()
        self.buy_image_height = self.buy_image_1.get_height()

        self.buy_options = []

    def make_starmap(self, grid_info):
        self.grid_info = grid_info
        self.grid_size = math.sqrt(len(self.grid_info['pos']))
        self.selected_grid = (int(self.grid_size / 2), int(self.grid_size / 2))

        pad = 3

        self.grid_info = grid_info

        self.grid_size = (self.map_size - pad * (self.grid_size) - pad) / self.grid_size

        start_x, start_y = self.GAME_WIDTH / 2 - self.map_size / 2, self.GAME_HEIGHT / 2 - self.map_size / 2

        for i in range(len(grid_info['pos'])):
            x, y = grid_info['pos'][i]
            fx, fy = start_x + ((self.grid_size + pad) * x) + pad, start_y + ((self.grid_size + pad) * y) + pad
            self.starmap_grid_screen['pixel_pos'].append((fx, fy))
            self.starmap_grid_screen['grid_pos'].append((x, y))
            self.starmap_grid_screen['color'].append(self.grid_info['starfields'][i].color)
            self.starmap_grid_screen['starfields'].append(StarField(num_stars=25, color=self.grid_info['starfields'][i].color, pos=(fx, fy), size=self.grid_size))

    def render_starmap(self, surface):
        pad = 3
        start_x, start_y = self.GAME_WIDTH / 2 - self.map_size / 2, self.GAME_HEIGHT / 2 - self.map_size / 2
        background_rectangle = (start_x, start_y, self.map_size, self.map_size)
        selected_grid_rect = (start_x + ((self.grid_size + pad) * self.selected_grid[0]) + pad - 2, start_y + ((self.grid_size + pad) * self.selected_grid[1]) + pad - 2, self.grid_size + 4, self.grid_size + 4)

        title_rectangle = (start_x, start_y - self.pad * 2, self.map_size, self.map_size / 2)
        pg.draw.rect(surface, self.dark_grey, title_rectangle)
        pg.draw.rect(surface, self.darker_grey, background_rectangle)
        pg.draw.rect(surface, (0, 0, 255), selected_grid_rect)

        font = pg.font.SysFont(self.font, self.text_size)
        starmap_label = font.render('Starmap', 1, (200, 200, 200))
        surface.blit(starmap_label, ((self.GAME_WIDTH / 2) - starmap_label.get_width() / 2, title_rectangle[1] + self.pad / 2))

        for i in range(len(self.starmap_grid_screen['starfields'])):

            x, y = self.grid_info['pos'][i]
            fx, fy = start_x + ((self.grid_size + pad) * x) + pad, start_y + ((self.grid_size + pad) * y) + pad
            grid_rect = (fx, fy, self.grid_size, self.grid_size)
            pg.draw.rect(surface, (0, 0, 0), grid_rect)

            if self.grid_info['discovered'][i]:
                self.starmap_grid_screen['starfields'][i].color = self.starmap_grid_screen['color'][i]
                self.starmap_grid_screen['starfields'][i].render(surface)
            else:
                self.starmap_grid_screen['starfields'][i].color = (25, 25, 25)
                self.starmap_grid_screen['starfields'][i].render(surface)

    def detect_clicked_grid(self):
        if self.star_map_active:
            x, y = pg.mouse.get_pos()
            old_selected_grid = self.selected_grid
            warpable_ships = self.grid_info['mobs'][self.grid_info['pos'].index(self.selected_grid)].detect_warpable_ships()

            for i in range(len(self.starmap_grid_screen['pixel_pos'])):

                small_x, small_y = self.starmap_grid_screen['pixel_pos'][i]
                big_x, big_y = small_x + self.grid_size, small_y + self.grid_size

                if small_x < x < big_x and small_y < y < big_y:
                    self.selected_grid = self.starmap_grid_screen['grid_pos'][i]
                    ox, oy = old_selected_grid
                    nx, ny = self.selected_grid

                    if pythag(ox, oy, nx, ny) < 1.5:
                        pass
                    else:
                        self.selected_grid = old_selected_grid

                    self.star_map_active = False

            if self.grid_info['discovered'][self.grid_info['pos'].index(self.selected_grid)]:
                pass
            elif warpable_ships > 0:
                pass
            else:
                self.selected_grid = old_selected_grid

        return self.selected_grid

    def render_hud(self, surface, ships=0, ship_atrributes=None, planet_attributes=None, player_stats=None):

        self.player_stats = player_stats

        # Define rectangles for boarder
        bottom_area_top_start = 0, self.GAME_HEIGHT - self.bottom_area_offset
        bottom_area_rectangle = (*bottom_area_top_start, self.GAME_WIDTH / 4, self.GAME_HEIGHT)
        bottom_area_fill_rectangle = (*bottom_area_top_start, self.GAME_WIDTH / 4, self.GAME_HEIGHT)
        rectangle = (self.boarder_screen_offset, self.boarder_screen_offset, self.GAME_WIDTH - self.boarder_screen_offset * 2, self.GAME_HEIGHT - self.boarder_screen_offset * 2)
        rectangle2 = (0, 0, self.GAME_WIDTH, self.GAME_HEIGHT)

        # Make screen boarder
        pg.draw.rect(surface, self.dark_grey, rectangle, 5)
        pg.draw.rect(surface, self.light_grey, rectangle2, 3)
        font = pg.font.SysFont(self.font, self.text_size)

        # Configuration for top UI text

        # current grid
        first_top_text_left = self.pad, 0 + self.GAME_HEIGHT / 100
        second_top_text_left = first_top_text_left[0], first_top_text_left[1] + self.pad
        top_text_start_right = self.GAME_WIDTH * 0.88, first_top_text_left[1]

        # current player currency text
        currency_label = font.render('Credits: {}'.format(player_stats['currency']), 1, (155, 155, 76))
        surface.blit(currency_label, (first_top_text_left))

        # current sector UI text
        grid_size = math.sqrt(len(self.grid_info['pos']))
        sec_x, sec_y = int(((self.selected_grid[0]) - grid_size / 2) + 0.5), int(((self.selected_grid[1]) - grid_size / 2) + 0.5)
        sector_label = font.render('Sector: {} , {}'.format(sec_x, sec_y), 1, (115, 155, 213))
        surface.blit(sector_label, (second_top_text_left))

        # number of friendly ships in grid
        ships_label = font.render('Friendly Ships: {}'.format(ships), 1, (255, 255, 255))
        surface.blit(ships_label, (top_text_start_right))

        # Configuration for bottom UI text
        first_text_start_x, first_text_start_y = (bottom_area_top_start[0] + self.GAME_WIDTH / 100) + self.boarder_screen_offset * 2, bottom_area_top_start[1] + self.pad / 2
        second_text_start_x, second_text_start_y = first_text_start_x, first_text_start_y + self.pad
        third_text_start_x, third_text_start_y = second_text_start_x, second_text_start_y + self.pad
        fourth_text_start_x, fourth_text_start_y = third_text_start_x, third_text_start_y + self.pad
        fifth_text_start_x, fifth_text_start_y = fourth_text_start_x, fourth_text_start_y + self.pad

        last_text_start_x, last_text_start_y = fifth_text_start_x, fifth_text_start_y + self.pad

        starmap_button_rectangle = self.GAME_WIDTH - 50 - self.pad, self.GAME_HEIGHT - 50 - self.pad, 50, 50

        if ship_atrributes != None:
            pg.draw.rect(surface, self.darker_grey, bottom_area_fill_rectangle, )
            pg.draw.rect(surface, self.light_grey, bottom_area_rectangle, 5)

            ships_label = font.render('Ship Speed: {}'.format(int(round(ship_atrributes['ship_speed'], 2) * 100)), 1, (255, 255, 255))
            surface.blit(ships_label, (first_text_start_x, first_text_start_y))

            ships_label = font.render('Hull Integrity: {}/{}'.format(ship_atrributes['hull1'], ship_atrributes['hull0']), 1, (255, 255, 255))
            surface.blit(ships_label, (second_text_start_x, second_text_start_y))

            ships_label = font.render('Crew Status: {}/{}'.format(ship_atrributes['crew1'], ship_atrributes['crew0']), 1, (255, 255, 255))
            surface.blit(ships_label, (third_text_start_x, third_text_start_y))

            energy_label = font.render('Ship Energy: {}'.format(ship_atrributes['energy']), 1, (200, 200, 255))
            surface.blit(energy_label, (fourth_text_start_x, fourth_text_start_y))

            kills_label = font.render('Kills: {}'.format(ship_atrributes['kills']), 1, (255, 255, 255))
            surface.blit(kills_label, (fifth_text_start_x, fifth_text_start_y))

            right_area_rect_x_start = self.GAME_WIDTH - self.GAME_WIDTH / 8
            right_area_rect_y_start = self.GAME_HEIGHT / 4
            right_area_rect_x_width = self.GAME_WIDTH / 8
            right_area_rect_y_width = self.GAME_HEIGHT / 2

            right_area_rect = (right_area_rect_x_start, right_area_rect_y_start, right_area_rect_x_width, right_area_rect_y_width)

            index = self.grid_info['pos'].index(self.selected_grid)
            self.buy_options = []
            for i in range(len(self.grid_info['mobs'][index].info['x'])):


                if self.grid_info['planets'][index].ship_over_planet and len(self.grid_info['mobs'][index].info['available_buildings'][i])>0:

                    pg.draw.rect(surface, self.darker_grey, right_area_rect)
                    pg.draw.rect(surface, self.light_grey, right_area_rect, 3)
                    trade_label = font.render('Trade', 1, (175, 212, 175))
                    surface.blit(trade_label, [right_area_rect_x_start + right_area_rect_x_width / 2 - trade_label.get_width() / 2, right_area_rect_y_start + self.pad / 2])
                    current_buildings = list(self.grid_info['mobs'][index].info['available_buildings'][i])
                    for j, building in enumerate(current_buildings):
                        if building == 'power_plant':
                            info_text = font.render('Buy Energy', 1, (175, 212, 175))
                        elif building == 'ship_yard':
                            info_text = font.render('Strengthen Hull', 1, (175, 212, 175))
                        elif building == 'crew_barracks':
                            info_text = font.render('Hire crew', 1, (175, 212, 175))
                        elif building == 'engineering_complex':
                            info_text = font.render('Increase Speed', 1, (175, 212, 175))
                        else:
                            info_text = font.render('???', 1, (175, 212, 175))

                        b1x = (right_area_rect_x_start + right_area_rect_x_width - self.buy_image_width * 2)
                        b1y = ((right_area_rect_y_start + self.pad + trade_label.get_height()) + (j * self.buy_image_1.get_height()))
                        b10x = b1x + self.buy_image_width - 5
                        b10y = b1y

                        self.buy_options.append({building: (b1x, b1y, b1x + self.buy_image_width, b1y + self.buy_image_height)})
                        surface.blit(info_text, [right_area_rect_x_start + self.pad / 3, b1y])
                        surface.blit(self.buy_image_1, [b1x, b1y])
                        surface.blit(self.buy_image_10, [b10x, b10y])

            if ship_atrributes['affects'].__contains__('on_fire'):
                affects_label = font.render('SHIP ON FIRE!', 1, (255, 200, 200))
                surface.blit(affects_label, (last_text_start_x, last_text_start_y))
            elif ship_atrributes['affects'].__contains__('crew_dead'):
                affects_label = font.render('CREW DEAD', 1, (200, 200, 255))
                surface.blit(affects_label, (last_text_start_x, last_text_start_y))
            else:
                buildings_label = font.render('Available Buildings: {}'.format(ship_atrributes['available_buildings']), 1, (255, 255, 255))
                surface.blit(buildings_label, (last_text_start_x, last_text_start_y))


        elif planet_attributes != None:
            pg.draw.rect(surface, self.darker_grey, bottom_area_fill_rectangle, )
            pg.draw.rect(surface, self.light_grey, bottom_area_rectangle, 5)
            pop_label = font.render('Planet Population: {}'.format(planet_attributes['population']), 1, (255, 255, 255))
            surface.blit(pop_label, (first_text_start_x, first_text_start_y))

            dev_text = ['None', 'Primitive', 'modern', 'Advanced', ]
            pop_label = font.render('Current Development: {}'.format(dev_text[planet_attributes['development_stage']]), 1, (255, 255, 255))
            surface.blit(pop_label, (second_text_start_x, second_text_start_y))

            pop_label = font.render('Available Buildings: {}'.format(planet_attributes['buildings']), 1, (255, 255, 255))
            surface.blit(pop_label, (third_text_start_x, third_text_start_y))

        pg.draw.rect(surface, (50, 10, 10), starmap_button_rectangle)

        if self.star_map_active:
            self.render_starmap(surface)

    def detect_if_clicked(self, x, y):
        ui_element_clicked = False
        credit_delta = 0

        if x > self.GAME_WIDTH - self.boarder_screen_offset - 50 - self.pad and y > self.GAME_HEIGHT - self.bottom_area_offset + self.pad:
            if self.star_map_active:
                self.star_map_active = False
            else:
                ui_element_clicked = True
                self.star_map_active = True


        elif 0 < x < self.GAME_HEIGHT and self.GAME_HEIGHT - self.bottom_area_offset < y < self.GAME_HEIGHT:
            ui_element_clicked = True
        elif self.GAME_WIDTH - self.GAME_WIDTH / 8 < x < self.GAME_WIDTH and self.GAME_HEIGHT / 4 < y < self.GAME_HEIGHT / 2:
            ui_element_clicked = True

        index = self.grid_info['pos'].index(self.selected_grid)
        selected_ships = self.determine_selected_ships()
        selected_building = None
        selected_ship = 0
        buy1 = False
        buy2 = False

        for i in range(len(selected_ships)):
            for j in range(len(self.buy_options)):
                current_building_dict = self.buy_options[j]
                current_building = [*current_building_dict][0]  # this trick unpacks keys as a list
                sx, sy, bx, by = current_building_dict[current_building]
                selected_building = current_building
                selected_ship = selected_ships[i]
                if sx < x < bx and sy < y < by:
                    buy1 = True
                    break
                elif sx + self.buy_image_width < x < bx + self.buy_image_width and sy < y < by:
                    buy2 = True
                    break

        if buy1 or buy2:
            if selected_building == 'power_plant':
                if buy1 and self.player_stats['currency'] >= 10:
                    self.grid_info['mobs'][index].info['energy'][selected_ship] += 5
                    self.player_stats['currency'] -= 10
                elif buy2 and self.player_stats['currency'] >= 25:
                    self.grid_info['mobs'][index].info['energy'][selected_ship] += 50
                    self.player_stats['currency'] -= 25
            elif selected_building == 'ship_yard':
                if buy1 and self.player_stats['currency'] >= 3:
                    self.grid_info['mobs'][index].info['hull0'][selected_ship] += 1
                    self.player_stats['currency'] -= 3
                elif buy2 and self.player_stats['currency'] >= 25:
                    self.grid_info['mobs'][index].info['hull0'][selected_ship] += 10
                    self.player_stats['currency'] -= 25
            elif selected_building == 'crew_barracks':
                if buy1:
                    if self.grid_info['mobs'][index].info['crew1'][selected_ship] < self.grid_info['mobs'][index].info['crew0'][selected_ship] and self.player_stats['currency'] >= 10:
                        self.grid_info['mobs'][index].info['crew1'][selected_ship] += 1
                        self.player_stats['currency'] -= 10
                    elif self.player_stats['currency'] >= 20:
                        self.grid_info['mobs'][index].info['crew0'][selected_ship] += 1
                        self.grid_info['mobs'][index].info['crew1'][selected_ship] += 1
                        self.player_stats['currency'] -= 20
                elif buy2:
                    if self.grid_info['mobs'][index].info['crew1'][selected_ship] < self.grid_info['mobs'][index].info['crew0'][selected_ship] and self.player_stats['currency'] >= 50:
                        self.grid_info['mobs'][index].info['crew1'][selected_ship] += 5
                        self.grid_info['mobs'][index].info['crew0'][selected_ship] += 5

                        self.player_stats['currency'] -= 50
                    elif self.player_stats['currency'] >= 100:
                        self.grid_info['mobs'][index].info['crew0'][selected_ship] += 5
                        self.grid_info['mobs'][index].info['crew1'][selected_ship] += 5
                        self.player_stats['currency'] -= 100
            elif selected_building == 'engineering_complex':
                if buy1 and self.player_stats['currency'] >= 5 and self.grid_info['mobs'][index].info['speed'][selected_ship] < 2.5:
                    self.grid_info['mobs'][index].info['speed'][selected_ship] += 0.01
                    self.player_stats['currency'] -= 5

                elif buy2 and self.player_stats['currency'] >= 50 and self.grid_info['mobs'][index].info['speed'][selected_ship] < 2.5:
                    self.grid_info['mobs'][index].info['speed'][selected_ship] += 0.1
                    self.player_stats['currency'] -= 50

        return ui_element_clicked, credit_delta

    def determine_selected_ships(self):
        selected_ships = []
        index = self.grid_info['pos'].index(self.selected_grid)
        for i in range(len(self.grid_info['mobs'][index].info['selected'])):
            if self.grid_info['mobs'][index].info['selected'][i]:
                selected_ships.append(i)
        return selected_ships


class Waypoints():

    def __init__(self):
        # waypoint setup
        self.show_frame_limit = 60
        self.sprite_size = 41
        self.image_index = 0
        self.anim_frame_increment = int(30 / 7)
        self.anim_increment_counter = 0

        self.move_waypoint_pos = (0, 0)

        self.move_waypoint_img = pg.image.load('images/waypoints/move.png').convert(32)
        self.move_waypoint_img.set_colorkey((0, 0, 0))

    def set_move_waypoint(self, x, y):
        self.anim_increment_counter = 0
        self.image_index = 0
        self.move_waypoint_pos = (x, y)

    def render(self, surface):
        image_section = self.move_waypoint_img.subsurface(0, 0, self.sprite_size, self.sprite_size)

        x, y = self.move_waypoint_pos

        if self.anim_increment_counter <= self.show_frame_limit:

            if self.anim_increment_counter < self.show_frame_limit / 2:
                if self.anim_increment_counter % 10 == 0:
                    image_section = self.move_waypoint_img.subsurface(self.sprite_size * self.image_index, 0, self.sprite_size, self.sprite_size)
                    self.image_index += 1


            else:
                if self.anim_increment_counter % 10 == 0:
                    image_section = self.move_waypoint_img.subsurface(self.sprite_size * self.image_index, 0, self.sprite_size, self.sprite_size)
                    self.image_index -= 1

            scaled_img = pg.transform.scale(image_section, (self.sprite_size * 2, self.sprite_size * 2))
            surface.blit(scaled_img, [x - self.sprite_size, y - self.sprite_size])
            self.anim_increment_counter += 1
