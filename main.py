import pygame
from lvl_gen import lvl_gen
import pygame_gui
import random
from typing import List

#inputs

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

#pygame init

pygame.init()
pygame.mixer.init()

#screen

screen_height = 800
screen_width = 1200

screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)

screen.fill((0,0,0))

pygame.display.set_caption("Cleric's Dungeon")

icon = pygame.image.load("textures/sleep.png")
pygame.display.set_icon(icon)

font = pygame.font.Font("Micro5-Regular.ttf", 32)
font2 = pygame.font.Font("Micro5-Regular.ttf", 36)
font3 = pygame.font.Font("Micro5-Regular.ttf", 56)
font0 = pygame.font.Font("Micro5-Regular.ttf", 24)

manager = pygame_gui.UIManager((screen_width,screen_height))

#surf

surf = pygame.Surface((100,100))

surf_center = (
    (screen_width-surf.get_width())/2,
    (screen_height-surf.get_height())/2
)

#dividers

divider_height = 200
pygame.draw.rect(screen, (50,50,50), (0, 0, screen_width, divider_height))
pygame.draw.rect(screen, (50,50,50), (0, screen_height - divider_height, screen_width, divider_height))

#left panel

left_panel_width = screen_width // 3
pygame.draw.rect(screen, (30,30,30), (0, divider_height, left_panel_width, screen_height - 2 * divider_height))

#buttons

button_width = 150
button_height = 150
button_x = 75
button_y = screen_height - divider_height + 25

button_color = (70,70,70)

outline_button_width = 150
outline_button_height = 150

button_texts = ["Sleep","Healing","Thunder","Devour","Shoot"]
button_texts_energy = []
button_texts_action = []

def is_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

button_rects = []
outline_button_rects = []
for i in range(5):
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    outline_button_rect = pygame.Rect(button_x, button_y, outline_button_width, outline_button_height)
    button_rects.append(button_rect)
    outline_button_rects.append(outline_button_rect)
    pygame.draw.rect(screen, button_color, button_rect)
    button_x += 225

#menu buttons

menu_button_y = screen_height*0.33
menu_button_rects = []
for i in range(5):
    menu_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
    pygame.draw.rect(screen, button_color, menu_button_rect)
    menu_button_rects.append(menu_button_rect)
    menu_button_y += button_height*1.5

menu_button_texts = ["Play", "Tutorial", "Scoreboard", "Settings", "Exit"]

settings_button_y = screen_height*0.25
settings_button_rects = []
for i in range(4):
    settings_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
    pygame.draw.rect(screen, button_color, settings_button_rect)
    settings_button_rects.append(settings_button_rect)
    settings_button_y += button_height*1.5

settings_button_texts = ["Music On/Off", "Music Louder", "Music Quieter", "Return"]

scoreboard_button_rect = pygame.Rect(screen_width//2-125, 3*screen_height//4, 250, 75)

tutorial_button_rect = pygame.Rect(screen_width//2-125, 3*screen_height//4, 250, 75)

#player
    
player_character_width = 256
player_character_height = 256

sleep_img = pygame.image.load("textures/sleep.png")
healing_img = pygame.image.load("textures/healing.png")
thunder_img = pygame.image.load("textures/thunder.png")
devour_img = pygame.image.load("textures/devour.png")
shoot_img = pygame.image.load("textures/shoot.png")
default_img = pygame.image.load("textures/default.png")

sleep_surf = sleep_img.convert_alpha()
healing_surf = healing_img.convert_alpha()
thunder_surf = thunder_img.convert_alpha()
devour_surf = devour_img.convert_alpha()
shoot_surf = shoot_img.convert_alpha()
default_surf = default_img.convert_alpha()

def load_player_character(button):
    if button == "Sleep":
        return sleep_surf
    elif button == "Healing":
        return healing_surf
    elif button == "Thunder":
        return thunder_surf
    elif button == "Devour":
        return devour_surf
    elif button == "Shoot":
        return shoot_surf
    else:
        return default_surf

player_character = load_player_character("Default")

#player stats

health = 20
energy = 20
hunger = 20
power = 1
shots = 0
shot_power = 1
shooting = False
thunder = False
devouring = False

max_health = 20
max_energy = 20
max_hunger = 20

health_img = pygame.image.load("textures/life.png")
energy_img = pygame.image.load("textures/mana.png")
hunger_img = pygame.image.load("textures/starvation.png")
power_img = pygame.image.load("textures/power.png")

health_surf = health_img.convert_alpha()
energy_surf = energy_img.convert_alpha()
hunger_surf = hunger_img.convert_alpha()
power_surf = power_img.convert_alpha()

stat_orbs = [health_surf, energy_surf, hunger_surf, power_surf]

#arrow

arrow_img = pygame.image.load("textures/arrow.png")
arrow_surf = arrow_img.convert_alpha()
arrow_scaled = pygame.transform.scale(arrow_surf, (100, 50))
arrow_pos = -75

#level

lvl_x = 2
lvl_y = 10
map = lvl_gen(lvl_x, lvl_y)

level = 0
room = 0
enemy = 0

#enemies

enemy_width = 256
enemy_height = 256
enemy_x = screen_width//2-enemy_width//2
enemy_y = screen_height//2-enemy_height//2
enemyattack = False

tiles_img = pygame.image.load("textures/tiles.png")
rat_img = pygame.image.load("textures/rat.png")
snake_img = pygame.image.load("textures/snake.png")
cockroach_img = pygame.image.load("textures/cockroach.png")
sheep_img = pygame.image.load("textures/sheep.png")
goblin_img = pygame.image.load("textures/goblin.png")
phoenibat_img = pygame.image.load("textures/phoenibat.png")
baby_img = pygame.image.load("textures/baby.png")
spirit_img = pygame.image.load("textures/spirit.png")
babushka_img = pygame.image.load("textures/babushka.png")
dragon_img = pygame.image.load("textures/dragon.png")

rat_attack_img = pygame.image.load("textures/rat_attack.png")
snake_attack_img = pygame.image.load("textures/snake_attack.png")
cockroach_attack_img = pygame.image.load("textures/cockroach_attack.png")
sheep_attack_img = pygame.image.load("textures/sheep_attack.png")
goblin_attack_img = pygame.image.load("textures/goblin_attack.png")
phoenibat_attack_img = pygame.image.load("textures/phoenibat_attack.png")
baby_attack_img = pygame.image.load("textures/baby_attack.png")
spirit_attack_img = pygame.image.load("textures/spirit_attack.png")
babushka_attack_img = pygame.image.load("textures/babushka_attack.png")
dragon_attack_img = pygame.image.load("textures/dragon.png")

tiles_surf = tiles_img.convert_alpha()
rat_surf = rat_img.convert_alpha()
snake_surf = snake_img.convert_alpha()
cockroach_surf = cockroach_img.convert_alpha()
sheep_surf = sheep_img.convert_alpha()
goblin_surf = goblin_img.convert_alpha()
phoenibat_surf = phoenibat_img.convert_alpha()
baby_surf = baby_img.convert_alpha()
spirit_surf = spirit_img.convert_alpha()
babushka_surf = babushka_img.convert_alpha()
dragon_surf = dragon_img.convert_alpha()

rat_attack_surf = rat_attack_img.convert_alpha()
snake_attack_surf = snake_attack_img.convert_alpha()
cockroach_attack_surf = cockroach_attack_img.convert_alpha()
sheep_attack_surf = sheep_attack_img.convert_alpha()
goblin_attack_surf = goblin_attack_img.convert_alpha()
phoenibat_attack_surf = phoenibat_attack_img.convert_alpha()
baby_attack_surf = baby_attack_img.convert_alpha()
spirit_attack_surf = spirit_attack_img.convert_alpha()
babushka_attack_surf = babushka_attack_img.convert_alpha()
dragon_attack_surf = dragon_attack_img.convert_alpha()


enemy_surf = [
    tiles_surf,
    rat_surf,
    sheep_surf,
    snake_surf,
    cockroach_surf,
    goblin_surf,
    phoenibat_surf,
    baby_surf,
    spirit_surf,
    babushka_surf,
    dragon_surf
]

enemy_surf_attack = [
    tiles_surf,
    rat_attack_surf,
    sheep_attack_surf,
    snake_attack_surf,
    cockroach_attack_surf,
    goblin_attack_surf,
    phoenibat_attack_surf,
    baby_attack_surf,
    spirit_attack_surf,
    babushka_attack_surf,
    dragon_attack_surf
]

temp_enemy_surf = enemy_surf

enemy_name = [
    "Tiles",
    "Rat",
    "Cotteep",
    "Snanana",
    "Giant Cockroach",
    "Goblin",
    "Phoenibat",
    "Mutant Baby",
    "Water Spirit",
    "Babushka",
    "Dragon"
]

enemy_health = [
    0,
    2,
    3,
    1,
    3,
    5,
    2,
    8,
    16,
    6,
    24
]

enemy_hp = enemy_health[1]

enemy_power = [
    0,
    1,
    1,
    2,
    2,
    2,
    3,
    2,
    1,
    3,
    2
]

#sounds

sleep_sound = pygame.mixer.Sound('sounds/sleep.wav')
healing_sound = pygame.mixer.Sound('sounds/healing.wav')
devour_sound = pygame.mixer.Sound('sounds/devour.wav')
thunder_sound = pygame.mixer.Sound('sounds/thunder.wav')
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')

player_sounds = [sleep_sound, healing_sound, thunder_sound, devour_sound, shoot_sound]

upgrade_sound = pygame.mixer.Sound('sounds/upgrade.wav')

es1 = pygame.mixer.Sound('sounds/enemysound1.wav')
es2 = pygame.mixer.Sound('sounds/enemysound2.wav')
es3 = pygame.mixer.Sound('sounds/enemysound3.wav')

enemy_sounds = [es1,es2,es3]

yell_sound = pygame.mixer.Sound('sounds/yell.wav')

player_death_sound = pygame.mixer.Sound('sounds/player_death.wav')

ed1 = pygame.mixer.Sound('sounds/enemydeath1.wav')
ed2 = pygame.mixer.Sound('sounds/enemydeath2.wav')

enemy_death_sounds = [ed1,ed2]

def playsound(sounds, x):
    sound = sounds[x]
    sound.play()

def playmusic(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=-1)

playmusic('music/SeeingDouble_Loopable.wav')

#upgrade shop

pop_button_x = 0
pop_button_y = 0

def random_button_text():
    random_buttons = [
        "Power +1",
        "Health +3",
        "Mana +3",
        "Power +2, HP -3",
        "Mana +6, Hunger +3",
        "Hunger -3",
        "Shoot *2",
        "Shot Power +1",
        "HP +6, Hunger +3",
        "Hunger -6, Power -1"
    ]
    return random_buttons[random.randint(0, len(random_buttons)-1)]

def show_upgrade_popup():
    global popup, ran_but_text, ran_but_rects, rel_but_rect, popup_rect, popup_x, popup_y

    popup = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((screen_width//2, screen_height//2), (700, 200)),
        manager=manager,
        window_title="Upgrades",
        action_long_desc="Choose player upgrades:"
    )

    popup_rect = popup.get_relative_rect()

    pop_button_y = 50
    pop_button_x = 50
    popup_x = popup_rect.x
    popup_y = popup_rect.y
    ran_but = []
    ran_but_text = []
    ran_but_rects = []
    for i in range(3):
        atext = random_button_text()
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pop_button_x, pop_button_y), (150, 50)),
            text=atext,
            manager=manager,
            container=popup
        )
        rel_but_rect = pygame.Rect((pop_button_x+popup_x, 2*pop_button_y+popup_y), (150, 50))
        ran_but_rects.append(rel_but_rect)
        ran_but.append(button)
        ran_but_text.append(atext)
        pop_button_x += 200

#tutorial

akcje_img = pygame.image.load("textures/actions.png")
akcje_surf = akcje_img.convert_alpha()
stats_img = pygame.image.load("textures/stats.png")
stats_surf = stats_img.convert_alpha()
stats_wroga_img = pygame.image.load("textures/enemy_stats.png")
stats_wroga_surf = stats_wroga_img.convert_alpha()

tut_images = [stats_surf, stats_wroga_surf, akcje_surf]

tut_texts = [
    "Stats show resources needed in battle."+'\n'+"When health goes to 0, you lose."+'\n'+"Mana is used to do actions."+'\n'+"Power shows strength of most actions.",
    "Enemy stats show state of enemy."+'\n'+"Every enemy type has its own base health and power."+'\n'+"If enemy's health goes below half, it starts healing."+'\n'+"When you defeat all enemies in a room you go to the next one",
    "With actions you counteract enemy actions."+'\n'+"In left top corner is cost."+'\n'+"In right top corner is a resource connected to the action."+'\n'+"Costs and resources can change during battle."
]

#particles

particle_color = (255,0,0)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(particle_color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.gravity = 0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not (0 <= self.rect.x <= screen_width and 0 <= self.rect.y <= screen_height):
            self.kill()

health_particle_color = (0,255,0)

class HealingParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(health_particle_color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.gravity = -0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not (0 <= self.rect.x <= screen_width and 0 <= self.rect.y <= screen_height):
            self.kill()

thunder_ss = pygame.image.load("textures/thunder_ss.png")
devouring_ss = pygame.image.load("textures/devour_ss.png")
enemyattack_ss = pygame.image.load("textures/enemyattack.png")

def get_sprite(sprite_sheet, x, y, width, height):
    sprite = pygame.Surface((width, height))
    sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
    sprite.set_colorkey((0, 0, 0))
    return sprite

all_sprites = pygame.sprite.Group()

#tick rate

clock = pygame.time.Clock()

#game loop

buttons_active = True
running = True
menu = True
dead = False
settings = False
scoreboard = False
tutorial = False
while running:

    #menu

    while menu:

        #Settings

        while settings:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, settings_button_rect in enumerate(settings_button_rects):
                        if is_clicked(mouse_pos, settings_button_rect):
                            if settings_button_texts[i] == "Music On/Off":
                                if pygame.mixer_music.get_volume() > 0:
                                    pygame.mixer_music.set_volume(0)
                                else:
                                    pygame.mixer_music.set_volume(1)
                            if settings_button_texts[i] == "Music Louder":
                                pygame.mixer_music.set_volume(pygame.mixer_music.get_volume()+0.1)
                            if settings_button_texts[i] == "Music Quieter":
                                pygame.mixer_music.set_volume(pygame.mixer_music.get_volume()-0.1)
                            if settings_button_texts[i] == "Return":
                                settings = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        settings = False

                elif event.type == QUIT:
                    settings = False

                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            screen.fill((0,0,0))

            settings_button_rects = [pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75) for i in range(4)]

            for i, settings_button_rect in enumerate(settings_button_rects):
                settings_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
                button_color=(70,70,70)
                pygame.draw.rect(screen, button_color, settings_button_rect)

                mouse_pos = pygame.mouse.get_pos()
                if settings_button_rect.collidepoint(mouse_pos):
                    button_color = (0,0,255)
                    pygame.draw.rect(screen, button_color, settings_button_rect)
                
                text = font.render(settings_button_texts[i], True, (0,0,0))
                text_rect = text.get_rect(center=settings_button_rect.center)
                screen.blit(text, text_rect)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)

        #Scoreboard

        while scoreboard:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if is_clicked(mouse_pos, scoreboard_button_rect):
                        scoreboard = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        scoreboard = False

                elif event.type == QUIT:
                    scoreboard = False

                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            screen.fill((0,0,0))

            text = font3.render("Top Scores", True, (255,255,255))
            screen.blit(text, (screen_width//2 - 200, screen_height//4 - 125))

            #top 3 scores

            sbsort = []
            with open("scoreboard.txt","r") as file:
                for line in file:
                    sbsort.append(line.rstrip())

            sbsort.sort()

            topscores = []
            top = 0
            if len(sbsort) >= 3:
                top = 3
            else:
                top = len(sbsort)

            for i in range(1, top+1):
                topscores.append(sbsort[-i])

            for i in range(top):
                sbrect = pygame.Rect(screen_width//2-150, screen_height//4+i*100, 300, 75)
                pygame.draw.rect(screen, (0,0,0), sbrect)

                text = font.render(topscores[i], True, (255,255,255))
                text_rect = text.get_rect(center=sbrect.center)
                screen.blit(text, text_rect)
            
            scoreboard_button_rect = pygame.Rect(screen_width//2-125, 3*screen_height//4, 250, 75)
            button_color=(70,70,70)
            pygame.draw.rect(screen, button_color, scoreboard_button_rect)

            mouse_pos = pygame.mouse.get_pos()
            if scoreboard_button_rect.collidepoint(mouse_pos):
                button_color = (0,0,255)
                pygame.draw.rect(screen, button_color, scoreboard_button_rect)
                
            text = font.render("Return", True, (0,0,0))
            text_rect = text.get_rect(center=scoreboard_button_rect.center)
            screen.blit(text, text_rect)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)
        
        #tutorial

        while tutorial:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if is_clicked(mouse_pos, tutorial_button_rect):
                        tutorial = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        tutorial = False

                elif event.type == QUIT:
                    tutorial = False

                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            screen.fill((0,0,0))

            text = font3.render("How to play", True, (255,255,255))
            screen.blit(text, (screen_width//2 - 125, screen_height//4 - 125))

            for i in range(3):
                tut_text_rect = pygame.Rect(25, screen_height//5*i+200, screen_width//3, screen_height//3)
                text = font0.render(tut_texts[i], True, (255,255,255))
                screen.blit(text, tut_text_rect)

                tut_image_rect = pygame.Rect(3*screen_width//4, screen_height//5*i+200, screen_width//3, screen_height//3)
                tut_image_trans = pygame.transform.scale(tut_images[i], (screen_width//5, screen_height//6))
                screen.blit(tut_image_trans, tut_image_rect)
            

            tutorial_button_rect = pygame.Rect(screen_width//2-125, screen_height-100, 250, 75)
            button_color=(70,70,70)
            pygame.draw.rect(screen, button_color, tutorial_button_rect)

            mouse_pos = pygame.mouse.get_pos()
            if tutorial_button_rect.collidepoint(mouse_pos):
                button_color = (0,0,255)
                pygame.draw.rect(screen, button_color, tutorial_button_rect)
                
            text = font.render("Return", True, (0,0,0))
            text_rect = text.get_rect(center=tutorial_button_rect.center)
            screen.blit(text, text_rect)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)
        
        #main menu

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, menu_button_rect in enumerate(menu_button_rects):
                    if is_clicked(mouse_pos, menu_button_rect):
                        if menu_button_texts[i] == "Play":
                            menu = False
                            show_upgrade_popup()
                            playmusic('music/TitleTheme_PhoneHome_Loopable.wav')
                        elif menu_button_texts[i] == "Tutorial":
                            tutorial = True
                        elif menu_button_texts[i] == "Scoreboard":
                            scoreboard = True
                        elif menu_button_texts[i] == "Settings":
                            settings = True
                        elif menu_button_texts[i] == "Exit":
                            pygame.quit()

            #escape

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
        
            #exit

            elif event.type == QUIT:
                pygame.quit()
        
            #screen size

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

        screen.fill((0,0,0))

        text = font3.render("Cleric's Dungeon", True, (255,255,255))
        screen.blit(text, (screen_width//2 - 200, screen_height//4 - 125))

        menu_button_rects = [pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75) for i in range(5)]

        for i, menu_button_rect in enumerate(menu_button_rects):
            menu_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
            button_color=(70,70,70)
            pygame.draw.rect(screen, button_color, menu_button_rect)

            mouse_pos = pygame.mouse.get_pos()
            if menu_button_rect.collidepoint(mouse_pos):
                button_color = (0,0,255)
                pygame.draw.rect(screen, button_color, menu_button_rect)
            
            text = font.render(menu_button_texts[i], True, (0,0,0))
            text_rect = text.get_rect(center=menu_button_rect.center)
            screen.blit(text, text_rect)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(15)

    enemy_id = map[level][room][enemy]

    #events

    for event in pygame.event.get():

        #buttons clicked

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(button_rects):
                if is_clicked(mouse_pos, button_rect) and buttons_active:
                    buttons_active = False
                    button_rects[i].width += 20
                    button_rects[i].height += 20
                    button_rects[i].x -= 10
                    button_rects[i].y -= 10
                    if noenergy == False or i == 0:
                        player_character = load_player_character(button_texts[i])
                    
                    #enemy move
                    
                    if i == 0 or noenergy == False:
                        if enemy_hp > enemy_health[enemy_id]//2:
                            playsound(enemy_sounds, random.randint(0, 2))
                            enemyattack = True
                        else:
                            enemy_hp += enemy_power[enemy_id]
                            if enemy_id == 7:
                                yell_sound.play()
                                energy -= enemy_power[enemy_id]
                            else:
                                healing_sound.play()
                            for j in range(enemy_power[enemy_id]):
                                particle = HealingParticle(screen_width//2, screen_height//2)
                                all_sprites.add(particle)

                    temp_enemy_surf[i] = enemy_surf[i]

                    #player move

                    playsound(player_sounds, i)
                    if button_texts[i] == "Sleep":
                        energy += 2
                        hunger -= 1
                        buttons_active = True
                    elif noenergy == False:
                        if button_texts[i] == "Healing":
                            health += power
                            energy -= enemy_power[enemy_id]
                            hunger -= 1
                            for j in range(power):
                                particle = HealingParticle(left_panel_width//2, screen_height//2)
                                all_sprites.add(particle)
                            buttons_active = True
                        elif button_texts[i] == "Thunder":
                            thunder = True
                            energy -= 1
                        elif button_texts[i] == "Devour":
                            energy -= enemy_hp
                            devouring = True
                        elif button_texts[i] == "Shoot":
                            energy -= len(map[level][room]) - enemy
                            enemy_hp -= shot_power
                            shots += 1
                            arrow_pos = -100
                            shooting = True
                            for j in range(len(map[level][room])-enemy):
                                for k in range(shot_power):
                                    particle = Particle(screen_width//2+j*200, screen_height//2)
                                    all_sprites.add(particle)
                    elif noenergy == True:
                        buttons_active = True

                
        

            #upgrades
            
            
            popup_x = popup_rect.x
            popup_y = popup_rect.y
            pop_button_x = 50
            pop_button_y = 50
            ran_but_rects = []
            for i in range(3):
                rel_but_rect = pygame.Rect((pop_button_x+popup_x, 2*pop_button_y+popup_y), (150, 50))
                ran_but_rects.append(rel_but_rect)
                pop_button_x += 200
            ran_but_rects: List[pygame.Rect] = ran_but_rects
            for i, rel_but_rect in enumerate(ran_but_rects):
                if is_clicked(mouse_pos, rel_but_rect):
                    upgrade_sound.play()
                    if ran_but_text[i] == "Power +1":
                        power += 1
                        popup.kill()
                    elif ran_but_text[i] == "Health +3":
                        healing_sound.play()
                        max_health += 3
                        health += 3
                        for j in range(3):
                            particle = HealingParticle(left_panel_width//2, screen_height//2)
                            all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Mana +3":
                        max_energy += 3
                        energy += 3
                        popup.kill()
                    elif ran_but_text[i] == "Power +2, HP -3":
                        health -= 3
                        max_health -= 3
                        power += 2
                        for j in range(3):
                            particle = Particle(left_panel_width // 2, screen_height // 2)
                            all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Mana +6, Hunger +3":
                        max_energy += 6
                        energy += 6
                        max_hunger += 3
                        popup.kill()
                    elif ran_but_text[i] == "Hunger -3":
                        max_hunger -= 3
                        popup.kill()
                    elif ran_but_text[i] == "Shoot *2":
                        shoot_sound.play()
                        shots += 2
                        enemy_hp -= 2*shot_power
                        arrow_pos = -100
                        shooting = True
                        for j in range(2*(len(map[level][room])-enemy)):
                            for k in range(shot_power):
                                particle = Particle(screen_width//2+j*200, screen_height//2)
                                all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Shot Power +1":
                        shot_power += 1
                        popup.kill()
                    elif ran_but_text[i] == "HP +6, Hunger +3":
                        healing_sound.play()
                        health += 6
                        max_health += 6
                        max_hunger += 3
                        for j in range(6):
                            particle = HealingParticle(left_panel_width // 2, screen_height // 2)
                            all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Hunger -6, Power -1":
                        max_hunger -= 6
                        power -= 1
                        popup.kill()

        else:
            button_rects = [pygame.Rect(75 + 225 * i, button_y, 150, 150) for i in range(5)]


        #escape

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                death_text = "You ran away"
                dead = True
        
        #exit

        elif event.type == QUIT:
            death_text = "You ran away"
            dead = True
        
        #screen size

        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    #next enemy

    if enemy_hp <= 0:
        playsound(enemy_death_sounds, random.randint(0, 1))
        map[level][room][enemy] = 0
        if enemy == len(map[level][room])-1:
            if room == len(map[level])-1:
                if level == len(map)-1:
                    death_text = "Victory!!!"
                    dead = True
                else:
                    level += 1
                    show_upgrade_popup()
                room = 0
            else:
                room += 1
            shots = 0
            enemy = 0
        else:
            enemy += 1
            enemy_id = map[level][room][enemy]
            enemy_hp = enemy_health[enemy_id]
            if shots > 0:
                enemy_hp -= shots*shot_power
        
    #enemy action

    if enemy_hp > enemy_health[enemy_id]//2:
        next_enemy_action = "Attack"
    else:
        if enemy_id != 7 and enemy_id != 8:
            next_enemy_action = "Healing"
        else:
            next_enemy_action = "Cry"

    #death and max stats
    
    if hunger < 0:
        hunger += 1
        health -= 1

    if hunger > max_hunger:
        hunger -= 1
        health += 1

    if energy < 0:
        energy += 1
        hunger -= 1
    
    if energy > max_energy:
        energy -= 1
        health -= 1

    if health <= 0:
        player_death_sound.play()
        death_text = "Death from "+str(enemy_name[enemy_id])
        dead = True
    
    if health > max_health:
        health -= 1

    if energy <= 0:
        noenergy = True
    else:
        noenergy = False
    

    #screen update
    
    #dividers

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (50,50,50), (0, 0, screen_width, divider_height))
    pygame.draw.rect(screen, (50,50,50), (0, screen_height - divider_height, screen_width, divider_height))
    pygame.draw.rect(screen, (30,30,30), (0, divider_height, left_panel_width, screen_height - 2 * divider_height))
    
    #buttons

    button_y = screen_height - divider_height + 25

    for i, button_rect in enumerate(button_rects):
        button_rect = pygame.Rect(75 + 225 * i, button_y, 150, 150)
        button_color=(70,70,70)
        pygame.draw.rect(screen, button_color, button_rect)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos) and buttons_active and (noenergy == False or i == 0):
            button_color = (0,0,255)
            pygame.draw.rect(screen, button_color, button_rect)
        
        text = font.render(button_texts[i], True, (0,0,0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        

    outline_button_rects: List[pygame.Rect] = outline_button_rects

    for i, outline_button_rect in enumerate(outline_button_rects):
        outline_button_rect = pygame.Rect(75 + 225 * i, button_y, outline_button_width, outline_button_height)

        energy_surf_scaled = pygame.transform.scale(energy_surf, (75, 75))
        screen.blit(energy_surf_scaled, energy_surf_scaled.get_rect(center=outline_button_rect.topleft))

        button_texts_energy = ["0",str(enemy_power[enemy_id]),"1",str(enemy_hp),str(len(map[level][room])-enemy)]
        text = font.render(button_texts_energy[i], True, (0,0,0))
        text2 = font2.render(button_texts_energy[i], True, (255,255,255))
        button_energy_text_rect = text.get_rect(center=outline_button_rect.topleft)
        screen.blit(text2, button_energy_text_rect)
        screen.blit(text, button_energy_text_rect)

        action_surfs = [energy_surf, health_surf, power_surf, power_surf, power_surf]
        action_surf = action_surfs[i]
        action_surf_scaled = pygame.transform.scale(action_surf, (75, 75))
        screen.blit(action_surf_scaled, energy_surf_scaled.get_rect(center=outline_button_rect.topright))

        button_texts_action = ["2",str(power),str(power),str(power+1),str(shot_power)+"*"+str(len(map[level][room])-enemy)]
        text = font.render(button_texts_action[i], True, (0,0,0))
        text2 = font2.render(button_texts_action[i], True, (255,255,255))
        button_action_text_rect = text.get_rect(center=outline_button_rect.topright)
        screen.blit(text2, button_action_text_rect)
        screen.blit(text, button_action_text_rect)
        
    #player

    player_character_scaled = pygame.transform.scale(player_character, (player_character_width, player_character_height))
    screen.blit(player_character_scaled, (left_panel_width // 2 - player_character_width // 2, screen_height // 2 - player_character_height // 2))
    
    #enemies

    enemy_x = screen_width//2-enemy_width//2
    enemy_y = screen_height//2-enemy_height//2
    for i in range(0, len(map[level][room])-enemy):
        if next_enemy_action == "Attack":
            if i == 0:
                temp_enemy_surf = enemy_surf_attack
        enemy_character_scaled = pygame.transform.scale(temp_enemy_surf[map[level][room][enemy+i]], (enemy_width, enemy_height))
        screen.blit(enemy_character_scaled, (enemy_x, enemy_y))
        temp_enemy_surf = enemy_surf
        enemy_x += 200

    #upper text
        
    for i in range(4):
        orb = pygame.transform.scale(stat_orbs[i], (50,50))
        screen.blit(orb, (0,i*40))

    health_text = font.render("Health: "+str(health)+"/"+str(max_health), True, (255,255,255))
    energy_text = font.render("Mana: "+str(energy)+"/"+str(max_energy), True, (255,255,255))
    hunger_text = font.render("Hunger: "+str(hunger)+"/"+str(max_hunger), True, (255,255,255))
    power_text = font.render("Power: "+str(power), True, (255,255,255))

    screen.blit(health_text, (50, 10))
    screen.blit(energy_text, (50, 50))
    screen.blit(hunger_text, (50, 90))
    screen.blit(power_text, (50, 130))

    enemy_name_text = font.render("Enemy: "+str(enemy_name[enemy_id]), True, (255,255,255))
    enemy_health_text = font.render("Enemy Health: "+str(enemy_hp)+"/"+str(enemy_health[enemy_id]), True, (255,255,255))
    enemy_power_text = font.render("Enemy Power: "+str(enemy_power[enemy_id]), True, (255,255,255))
    enemy_action_text = font.render("Enemy Action: "+next_enemy_action, True, (255,255,255))

    screen.blit(enemy_name_text, (screen_width*2//3+10, 10))
    screen.blit(enemy_health_text, (screen_width*2//3+10, 50))
    screen.blit(enemy_power_text, (screen_width*2//3+10, 90))
    screen.blit(enemy_action_text, (screen_width*2//3+10, 130))

    level_text = font.render("Level: "+str(level), True, (255,255,255))
    room_text = font.render("Room: "+str(room), True, (255,255,255))
    enemy_text = font.render("Enemy: "+str(enemy), True, (255,255,255))

    screen.blit(level_text, (screen_width//3+10, 10))
    screen.blit(room_text, (screen_width//3+10, 50))
    screen.blit(enemy_text, (screen_width//3+10, 90))

    #arrow

    if shooting:
        screen.blit(arrow_scaled, (screen_width//3+arrow_pos, screen_height//2-50))
        arrow_pos += 80
        if arrow_pos > screen_width:
            shooting = False
            buttons_active = True

    #update particles
            
    all_sprites.update()
    all_sprites.draw(screen)
    
    #attack vfx

    if enemyattack:
        sprite = get_sprite(enemyattack_ss, eframe, 0, 48, 48)
        sprite = pygame.transform.scale(sprite, (256, 256))
        sprite = pygame.transform.flip(sprite, -1, False)
        screen.blit(sprite, (left_panel_width//2-128, screen_height//2-128))
        eframe = eframe + 48
    else:
        eframe = 0
    if eframe >= 240:
        enemyattack = False
        buttons_active = True
        health -= enemy_power[enemy_id]
        for i in range(enemy_power[enemy_id]):
            particle = Particle(left_panel_width//2, screen_height//2)
            all_sprites.add(particle)

    if thunder:
        sprite = get_sprite(thunder_ss, frame, 0, 64, 88)
        sprite = pygame.transform.scale(sprite, (256, 352))
        screen.blit(sprite, (screen_width//2-128, screen_height//2-176))
        frame = frame + 64
    else:
        frame = 0
    if frame >= 704:
        thunder = False
        buttons_active = True
        enemy_hp -= power
        for i in range(power):
            particle = Particle(screen_width//2, screen_height//2)
            all_sprites.add(particle)
    
    if devouring:
        sprite = get_sprite(devouring_ss, aframe, 0, 48, 64)
        sprite = pygame.transform.scale(sprite, (256, 341))
        screen.blit(sprite, (screen_width//2-128, screen_height//2-170))
        aframe = aframe + 48
    else:
        aframe = 0
    if aframe >= 15*48:
        devouring = False
        buttons_active = True
        if enemy_hp > power + 1:
            hunger += power+1
        else:
            hunger += enemy_hp*2
        enemy_hp -= power + 1
        for i in range(power+1):
            particle = Particle(screen_width//2, screen_height//2)
            all_sprites.add(particle)

    #manager

    manager.process_events(event)
    manager.update(60)
    manager.draw_ui(screen)

    #screen

    pygame.display.update()
    pygame.display.flip()
    clock.tick(15)
    
    #game over

    if dead:

        pygame.mixer_music.stop()
        popup.kill()

        end_text = font.render("Game Over :)", True, (255,255,255))
        death_text = font.render(death_text, True, (255,255,255))
        level_count_text = font.render("You went to room "+str(room)+" level "+str(level)+"!", True, (255,255,255))
        screen.fill((0,0,0))
        screen.blit(level_count_text, (screen_width//2-level_count_text.get_width()//2,screen_height//2))
        screen.blit(death_text, (screen_width//2-death_text.get_width()//2,screen_height//2-25))
        screen.blit(end_text, (screen_width//2-end_text.get_width()//2,screen_height//2-50))

        #score save

        score = "l"+str(level)+"r"+str(room)
        with open("scoreboard.txt","r") as file:
            hs = ""
            hs_text = ""
            pr = file.readlines()
            if pr != "":
                for i in range(len(pr)):
                    if pr[i] > hs:
                        hs = pr[i]
                if score > hs:
                    hs_text = font.render("High Score!!!", True, (255,255,255))
                    screen.blit(hs_text, (screen_width//2-end_text.get_width()//2,screen_height//2-75))
            else:
                hs_text = font.render("High Score!!!", True, (255,255,255))
                screen.blit(hs_text, (screen_width//2-end_text.get_width()//2,screen_height//2-75))
        if len(pr) > 0:
            with open("scoreboard.txt","a") as file:
                file.write(str(score)+'\n')
        else:
            with open("scoreboard.txt","w") as file:
                file.write(str(score)+'\n')
        
        health = 20
        energy = 20
        hunger = 20
        power = 1
        shots = 0
        shot_power = 1
        shooting = False
        thunder = False
        devouring = False

        max_health = 20
        max_energy = 20
        max_hunger = 20

        map = lvl_gen(lvl_x, lvl_y)

        level = 0
        room = 0
        enemy = 0

        pygame.display.flip()
        pygame.time.delay(6000)
        death_text = ""
        menu = True
        dead = False
        buttons_active = True
        playmusic('music/SeeingDouble_Loopable.wav')


pygame.quit()