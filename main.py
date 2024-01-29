import pygame
from lvl_gen import lvl_gen
import pygame_gui
import random
from typing import List

#inputy

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

#rozpoczęcie pygame

pygame.init()
pygame.mixer.init()

#screen

screen_height = 800
screen_width = 1200

screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)

screen.fill((0,0,0))

pygame.display.set_caption("Cleric's Dungeon")

icon = pygame.image.load("textures/spanko.png")
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

#dividery

divider_height = 200
pygame.draw.rect(screen, (50,50,50), (0, 0, screen_width, divider_height))
pygame.draw.rect(screen, (50,50,50), (0, screen_height - divider_height, screen_width, divider_height))

#lewy panel

left_panel_width = screen_width // 3
pygame.draw.rect(screen, (30,30,30), (0, divider_height, left_panel_width, screen_height - 2 * divider_height))

#przyciski

button_width = 150
button_height = 150
button_x = 75
button_y = screen_height - divider_height + 25

button_color = (70,70,70)

outline_button_width = 150
outline_button_height = 150

button_texts = ["Spanko","Leczenie","Zaklęcie","Pochłoń","Strzał"]
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

#przyciski w menu

menu_button_y = screen_height*0.33
menu_button_rects = []
for i in range(5):
    menu_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
    pygame.draw.rect(screen, button_color, menu_button_rect)
    menu_button_rects.append(menu_button_rect)
    menu_button_y += button_height*1.5

menu_button_texts = ["Graj", "Tutorial", "Tabela Wyników", "Ustawienia", "Wyjdź"]

settings_button_y = screen_height*0.25
settings_button_rects = []
for i in range(4):
    settings_button_rect = pygame.Rect(screen_width//2-125, screen_height//4 + 100*i, 250, 75)
    pygame.draw.rect(screen, button_color, settings_button_rect)
    settings_button_rects.append(settings_button_rect)
    settings_button_y += button_height*1.5

settings_button_texts = ["Muzyka On/Off", "Muzyka Głośniej", "Muzyka Ciszej", "Powrót"]

scoreboard_button_rect = pygame.Rect(screen_width//2-125, 3*screen_height//4, 250, 75)

tutorial_button_rect = pygame.Rect(screen_width//2-125, 3*screen_height//4, 250, 75)

#gracz
    
player_character_width = 256
player_character_height = 256

spanko_img = pygame.image.load("textures/spanko.png")
leczenie_img = pygame.image.load("textures/leczenie.png")
zaklecie_img = pygame.image.load("textures/zaklecie.png")
jedzenie_img = pygame.image.load("textures/jedzenie.png")
strzal_img = pygame.image.load("textures/strzal.png")
default_img = pygame.image.load("textures/default.png")

spanko_surf = spanko_img.convert_alpha()
leczenie_surf = leczenie_img.convert_alpha()
zaklecie_surf = zaklecie_img.convert_alpha()
jedzenie_surf = jedzenie_img.convert_alpha()
strzal_surf = strzal_img.convert_alpha()
default_surf = default_img.convert_alpha()

def load_player_character(button):
    if button == "Spanko":
        return spanko_surf
    elif button == "Leczenie":
        return leczenie_surf
    elif button == "Zaklęcie":
        return zaklecie_surf
    elif button == "Pochłoń":
        return jedzenie_surf
    elif button == "Strzał":
        return strzal_surf
    else:
        return default_surf

player_character = load_player_character("Default")

#statystyki gracza

health = 20
energy = 20
hunger = 20
power = 1
shots = 0
shot_power = 1
shooting = False
zaklecie = False
pochloniecie = False

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

#strzała

arrow_img = pygame.image.load("textures/arrow.png")
arrow_surf = arrow_img.convert_alpha()
arrow_scaled = pygame.transform.scale(arrow_surf, (100, 50))
arrow_pos = -75

#level

lvl_x = 2
lvl_y = 10
mapa = lvl_gen(lvl_x, lvl_y)

level = 0
room = 0
enemy = 0

#wrogowie

enemy_width = 256
enemy_height = 256
enemy_x = screen_width//2-enemy_width//2
enemy_y = screen_height//2-enemy_height//2
enemyattack = False

plytki_img = pygame.image.load("textures/plytki.png")
szczur_img = pygame.image.load("textures/szczur.png")
wezowiec_img = pygame.image.load("textures/wezowiec.png")
karaluch_img = pygame.image.load("textures/karaluch.png")
baowca_img = pygame.image.load("textures/baowca.png")
goblin_img = pygame.image.load("textures/goblin.png")
feniksoperz_img = pygame.image.load("textures/feniksoperz.png")
dziecko_img = pygame.image.load("textures/dziecko.png")
woduch_img = pygame.image.load("textures/woduch.png")
babushka_img = pygame.image.load("textures/babushka.png")
smok_img = pygame.image.load("textures/smok.png")

szczur_atak_img = pygame.image.load("textures/szczur_atak.png")
wezowiec_atak_img = pygame.image.load("textures/wezowiec_atak.png")
karaluch_atak_img = pygame.image.load("textures/karaluch_atak.png")
baowca_atak_img = pygame.image.load("textures/baowca_atak.png")
goblin_atak_img = pygame.image.load("textures/goblin_atak.png")
feniksoperz_atak_img = pygame.image.load("textures/feniksoperz_atak.png")
dziecko_atak_img = pygame.image.load("textures/dziecko_atak.png")
woduch_atak_img = pygame.image.load("textures/woduch_atak.png")
babushka_atak_img = pygame.image.load("textures/babushka_atak.png")
smok_atak_img = pygame.image.load("textures/smok.png")

plytki_surf = plytki_img.convert_alpha()
szczur_surf = szczur_img.convert_alpha()
wezowiec_surf = wezowiec_img.convert_alpha()
karaluch_surf = karaluch_img.convert_alpha()
baowca_surf = baowca_img.convert_alpha()
goblin_surf = goblin_img.convert_alpha()
feniksoperz_surf = feniksoperz_img.convert_alpha()
dziecko_surf = dziecko_img.convert_alpha()
woduch_surf = woduch_img.convert_alpha()
babushka_surf = babushka_img.convert_alpha()
smok_surf = smok_img.convert_alpha()

szczur_atak_surf = szczur_atak_img.convert_alpha()
wezowiec_atak_surf = wezowiec_atak_img.convert_alpha()
karaluch_atak_surf = karaluch_atak_img.convert_alpha()
baowca_atak_surf = baowca_atak_img.convert_alpha()
goblin_atak_surf = goblin_atak_img.convert_alpha()
feniksoperz_atak_surf = feniksoperz_atak_img.convert_alpha()
dziecko_atak_surf = dziecko_atak_img.convert_alpha()
woduch_atak_surf = woduch_atak_img.convert_alpha()
babushka_atak_surf = babushka_atak_img.convert_alpha()
smok_atak_surf = smok_atak_img.convert_alpha()


enemy_surf = [
    plytki_surf,
    szczur_surf,
    baowca_surf,
    wezowiec_surf,
    karaluch_surf,
    goblin_surf,
    feniksoperz_surf,
    dziecko_surf,
    woduch_surf,
    babushka_surf,
    smok_surf
]

enemy_surf_attack = [
    plytki_surf,
    szczur_atak_surf,
    baowca_atak_surf,
    wezowiec_atak_surf,
    karaluch_atak_surf,
    goblin_atak_surf,
    feniksoperz_atak_surf,
    dziecko_atak_surf,
    woduch_atak_surf,
    babushka_atak_surf,
    smok_atak_surf
]

temp_enemy_surf = enemy_surf

enemy_name = [
    "Płytki Podłogowe",
    "Szczur",
    "Baowca",
    "Wąż Bananowy",
    "Giga Karaluch",
    "Goblin",
    "Feniksoperz",
    "Dziecko Mutant",
    "Woduch",
    "Babushka",
    "Smok"
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

#dźwięki

spanko_sound = pygame.mixer.Sound('sounds/spanko.wav')
leczenie_sound = pygame.mixer.Sound('sounds/leczenie.wav')
jedzenie_sound = pygame.mixer.Sound('sounds/jedzenie.wav')
zaklecie_sound = pygame.mixer.Sound('sounds/zaklecie.wav')
strzal_sound = pygame.mixer.Sound('sounds/strzal.wav')

player_sounds = [spanko_sound, leczenie_sound, zaklecie_sound, jedzenie_sound, strzal_sound]

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
        "Moc +1",
        "Zdrowie +3",
        "Mana +3",
        "Moc +2, HP -3",
        "Mana +6, Głód +3",
        "Głód -3",
        "Strzał *2",
        "Moc Strzału +1",
        "HP +6, Głód +3",
        "Głód -6, Moc -1"
    ]
    return random_buttons[random.randint(0, len(random_buttons)-1)]

def show_upgrade_popup():
    global popup, ran_but, ran_but_text, ran_but_rects, rel_but_rect, popup_rect, popup_x, popup_y

    popup = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((screen_width//2, screen_height//2), (700, 200)),
        manager=manager,
        window_title="Ulepszenia",
        action_long_desc="Wybierz ulepszenia postaci:",
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

show_upgrade_popup()
popup.kill()

#tutorial

akcje_img = pygame.image.load("textures/akcje.png")
akcje_surf = akcje_img.convert_alpha()
statsy_img = pygame.image.load("textures/statsy.png")
statsy_surf = statsy_img.convert_alpha()
statsy_wroga_img = pygame.image.load("textures/statsy_wroga.png")
statsy_wroga_surf = statsy_wroga_img.convert_alpha()

tut_images = [statsy_surf, statsy_wroga_surf, akcje_surf]

tut_texts = [
    "Statystyki pokazują surowce potrzebne w walce."+'\n'+"Jeśli zdrowie dojdzie do zera, przegrywasz."+'\n'+"Mana służy do wyjonywania akcji."+'\n'+"Moc oznacza siłę większości akcji.",
    "Statystyki wroga pokazują stan przeciwnika."+'\n'+"Każdy rodzaj wroga ma taką samą siłę i zdrowie."+'\n'+"Jeśli zdrowie wroga spadnie poniżej połowy to rozpoczyna leczenie."+'\n'+"Jeśli pokonasz wszystkich wrogów w pokoju, idziesz dalej",
    "Akcjami odpowiadasz na ruchy wroga."+'\n'+"W lewym górnym rogu jest koszt."+'\n'+"W prawym górnym rogu jest surowiec powiązany z akcją."+'\n'+"Koszty i surowce mogą się zmieniać w trakcie walki."
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

zaklecie_ss = pygame.image.load("textures/zaklecie_ss.png")
pochloniecie_ss = pygame.image.load("textures/pochłonięcie_ss.png")
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

popup_open = False
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

        #ustawienia

        while settings:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, settings_button_rect in enumerate(settings_button_rects):
                        if is_clicked(mouse_pos, settings_button_rect):
                            if settings_button_texts[i] == "Muzyka On/Off":
                                if pygame.mixer_music.get_volume() > 0:
                                    pygame.mixer_music.set_volume(0)
                                else:
                                    pygame.mixer_music.set_volume(1)
                            if settings_button_texts[i] == "Muzyka Głośniej":
                                pygame.mixer_music.set_volume(pygame.mixer_music.get_volume()+0.1)
                            if settings_button_texts[i] == "Muzyka Ciszej":
                                pygame.mixer_music.set_volume(pygame.mixer_music.get_volume()-0.1)
                            if settings_button_texts[i] == "Powrót":
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
            
            manager.process_events(event)
            manager.update(0.2)
            manager.draw_ui(screen)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)

        #tabela wyników

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

            text = font3.render("Najlepsze Wyniki", True, (255,255,255))
            screen.blit(text, (screen_width//2 - 200, screen_height//4 - 125))

            #top 3 wyników

            sbsort = []
            with open("scoreboard.txt","r") as plik:
                for linia in plik:
                    sbsort.append(linia.rstrip())

            sbsort.sort()

            topscores = []

            for i in range(1, 4):
                topscores.append(sbsort[-i])

            for i in range(3):
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
                
            text = font.render("Powrót", True, (0,0,0))
            text_rect = text.get_rect(center=scoreboard_button_rect.center)
            screen.blit(text, text_rect)
            
            manager.process_events(event)
            manager.update(0.2)
            manager.draw_ui(screen)

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

            text = font3.render("Jak grać", True, (255,255,255))
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
                
            text = font.render("Powrót", True, (0,0,0))
            text_rect = text.get_rect(center=tutorial_button_rect.center)
            screen.blit(text, text_rect)
            
            manager.process_events(event)
            manager.update(0.2)
            manager.draw_ui(screen)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)
        
        #main menu

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, menu_button_rect in enumerate(menu_button_rects):
                    if is_clicked(mouse_pos, menu_button_rect):
                        if menu_button_texts[i] == "Graj":
                            menu = False
                            playmusic('music/TitleTheme_PhoneHome_Loopable.wav')
                        elif menu_button_texts[i] == "Tutorial":
                            tutorial = True
                        elif menu_button_texts[i] == "Tabela Wyników":
                            scoreboard = True
                        elif menu_button_texts[i] == "Ustawienia":
                            settings = True
                        elif menu_button_texts[i] == "Wyjdź":
                            pygame.quit()

            #escape

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
        
            #exit

            elif event.type == QUIT:
                pygame.quit()
        
            #wielkość ekranu

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
        
        manager.process_events(event)
        manager.update(0.2)
        manager.draw_ui(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(15)

    enemy_id = mapa[level][room][enemy]

    #eventy

    for event in pygame.event.get():

        #przyciski kliknięte

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
                    
                    #ruch wroga
                    
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
                                leczenie_sound.play()
                            for j in range(enemy_power[enemy_id]):
                                particle = HealingParticle(screen_width//2, screen_height//2)
                                all_sprites.add(particle)

                    temp_enemy_surf[i] = enemy_surf[i]

                    #ruch gracza

                    playsound(player_sounds, i)
                    if button_texts[i] == "Spanko":
                        energy += 2
                        hunger -= 1
                        buttons_active = True
                    elif noenergy == False:
                        if button_texts[i] == "Leczenie":
                            health += power
                            energy -= enemy_power[enemy_id]
                            hunger -= 1
                            for j in range(power):
                                particle = HealingParticle(left_panel_width//2, screen_height//2)
                                all_sprites.add(particle)
                            buttons_active = True
                        elif button_texts[i] == "Zaklęcie":
                            zaklecie = True
                            energy -= 1
                        elif button_texts[i] == "Pochłoń":
                            energy -= enemy_hp
                            pochloniecie = True
                        elif button_texts[i] == "Strzał":
                            energy -= len(mapa[level][room]) - enemy
                            enemy_hp -= shot_power
                            shots += 1
                            arrow_pos = -100
                            shooting = True
                            for j in range(len(mapa[level][room])-enemy):
                                for k in range(shot_power):
                                    particle = Particle(screen_width//2+j*200, screen_height//2)
                                    all_sprites.add(particle)
                    elif noenergy == True:
                        buttons_active = True

                
        

            #ulepszenia
            
            
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
                    if ran_but_text[i] == "Moc +1":
                        power += 1
                        popup.kill()
                    elif ran_but_text[i] == "Zdrowie +3":
                        leczenie_sound.play()
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
                    elif ran_but_text[i] == "Moc +2, HP -3":
                        health -= 3
                        max_health -= 3
                        power += 2
                        for j in range(3):
                            particle = Particle(left_panel_width // 2, screen_height // 2)
                            all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Mana +6, Głód +3":
                        max_energy += 6
                        energy += 6
                        max_hunger += 3
                        popup.kill()
                    elif ran_but_text[i] == "Głód -3":
                        max_hunger -= 3
                        popup.kill()
                    elif ran_but_text[i] == "Strzał *2":
                        strzal_sound.play()
                        shots += 2
                        enemy_hp -= 2*shot_power
                        arrow_pos = -100
                        shooting = True
                        for j in range(2*(len(mapa[level][room])-enemy)):
                            for k in range(shot_power):
                                particle = Particle(screen_width//2+j*200, screen_height//2)
                                all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Moc Strzału +1":
                        shot_power += 1
                        popup.kill()
                    elif ran_but_text[i] == "HP +6, Głód +3":
                        leczenie_sound.play()
                        health += 6
                        max_health += 6
                        max_hunger += 3
                        for j in range(6):
                            particle = HealingParticle(left_panel_width // 2, screen_height // 2)
                            all_sprites.add(particle)
                        popup.kill()
                    elif ran_but_text[i] == "Głód -6, Moc -1":
                        max_hunger -= 6
                        power -= 1
                        popup.kill()

        else:
            button_rects = [pygame.Rect(75 + 225 * i, button_y, 150, 150) for i in range(5)]


        #escape

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                death_text = "Popełniłeś Sudoku"
                dead = True
        
        #exit

        elif event.type == QUIT:
            death_text = "Popełniłeś Sudoku"
            dead = True
        
        #wielkość ekranu

        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    #następny wróg

    if enemy_hp <= 0:
        playsound(enemy_death_sounds, random.randint(0, 1))
        mapa[level][room][enemy] = 0
        if enemy == len(mapa[level][room])-1:
            if room == len(mapa[level])-1:
                if level == len(mapa)-1:
                    death_text = "Wygrana!!!"
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
            enemy_id = mapa[level][room][enemy]
            enemy_hp = enemy_health[enemy_id]
            if shots > 0:
                enemy_hp -= shots*shot_power
        
    #akcja wroga

    if enemy_hp > enemy_health[enemy_id]//2:
        next_enemy_action = "Atak"
    else:
        if enemy_id != 7 and enemy_id != 8:
            next_enemy_action = "Leczenie"
        else:
            next_enemy_action = "Rozpacz"

    #śmierć i max statystyki
    
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
        death_text = "Smierć z rąk "+str(enemy_name[enemy_id])
        dead = True
    
    if health > max_health:
        health -= 1

    if energy <= 0:
        noenergy = True
    else:
        noenergy = False
    

    #update ekranu gry
    
    #dividery

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (50,50,50), (0, 0, screen_width, divider_height))
    pygame.draw.rect(screen, (50,50,50), (0, screen_height - divider_height, screen_width, divider_height))
    pygame.draw.rect(screen, (30,30,30), (0, divider_height, left_panel_width, screen_height - 2 * divider_height))
    
    #przyciski

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

        button_texts_energy = ["0",str(enemy_power[enemy_id]),"1",str(enemy_hp),str(len(mapa[level][room])-enemy)]
        text = font.render(button_texts_energy[i], True, (0,0,0))
        text2 = font2.render(button_texts_energy[i], True, (255,255,255))
        button_energy_text_rect = text.get_rect(center=outline_button_rect.topleft)
        screen.blit(text2, button_energy_text_rect)
        screen.blit(text, button_energy_text_rect)

        action_surfs = [energy_surf, health_surf, power_surf, power_surf, power_surf]
        action_surf = action_surfs[i]
        action_surf_scaled = pygame.transform.scale(action_surf, (75, 75))
        screen.blit(action_surf_scaled, energy_surf_scaled.get_rect(center=outline_button_rect.topright))

        button_texts_action = ["2",str(power),str(power),str(power+1),str(shot_power)+"*"+str(len(mapa[level][room])-enemy)]
        text = font.render(button_texts_action[i], True, (0,0,0))
        text2 = font2.render(button_texts_action[i], True, (255,255,255))
        button_action_text_rect = text.get_rect(center=outline_button_rect.topright)
        screen.blit(text2, button_action_text_rect)
        screen.blit(text, button_action_text_rect)
        
    #gracz

    player_character_scaled = pygame.transform.scale(player_character, (player_character_width, player_character_height))
    screen.blit(player_character_scaled, (left_panel_width // 2 - player_character_width // 2, screen_height // 2 - player_character_height // 2))
    
    #wrogowie

    enemy_x = screen_width//2-enemy_width//2
    enemy_y = screen_height//2-enemy_height//2
    for i in range(0, len(mapa[level][room])-enemy):
        if next_enemy_action == "Atak":
            if i == 0:
                temp_enemy_surf = enemy_surf_attack
        enemy_character_scaled = pygame.transform.scale(temp_enemy_surf[mapa[level][room][enemy+i]], (enemy_width, enemy_height))
        screen.blit(enemy_character_scaled, (enemy_x, enemy_y))
        temp_enemy_surf = enemy_surf
        enemy_x += 200

    #tekst górny
        
    for i in range(4):
        orb = pygame.transform.scale(stat_orbs[i], (50,50))
        screen.blit(orb, (0,i*40))

    health_text = font.render("Zdrowie: "+str(health)+"/"+str(max_health), True, (255,255,255))
    energy_text = font.render("Mana: "+str(energy)+"/"+str(max_energy), True, (255,255,255))
    hunger_text = font.render("Nasycenie: "+str(hunger)+"/"+str(max_hunger), True, (255,255,255))
    power_text = font.render("Moc: "+str(power), True, (255,255,255))

    screen.blit(health_text, (50, 10))
    screen.blit(energy_text, (50, 50))
    screen.blit(hunger_text, (50, 90))
    screen.blit(power_text, (50, 130))

    enemy_name_text = font.render("Wróg: "+str(enemy_name[enemy_id]), True, (255,255,255))
    enemy_health_text = font.render("Zdrowie Wroga: "+str(enemy_hp)+"/"+str(enemy_health[enemy_id]), True, (255,255,255))
    enemy_power_text = font.render("Moc Wroga: "+str(enemy_power[enemy_id]), True, (255,255,255))
    enemy_action_text = font.render("Ruch Wroga: "+next_enemy_action, True, (255,255,255))

    screen.blit(enemy_name_text, (screen_width*2//3+10, 10))
    screen.blit(enemy_health_text, (screen_width*2//3+10, 50))
    screen.blit(enemy_power_text, (screen_width*2//3+10, 90))
    screen.blit(enemy_action_text, (screen_width*2//3+10, 130))

    level_text = font.render("Poziom: "+str(level), True, (255,255,255))
    room_text = font.render("Pokój: "+str(room), True, (255,255,255))
    enemy_text = font.render("Wróg: "+str(enemy), True, (255,255,255))

    screen.blit(level_text, (screen_width//3+10, 10))
    screen.blit(room_text, (screen_width//3+10, 50))
    screen.blit(enemy_text, (screen_width//3+10, 90))

    #strzała

    if shooting:
        screen.blit(arrow_scaled, (screen_width//3+arrow_pos, screen_height//2-50))
        arrow_pos += 80
        if arrow_pos > screen_width:
            shooting = False
            buttons_active = True

    #update particlesów
            
    all_sprites.update()
    all_sprites.draw(screen)
    
    #vfx ataku

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

    if zaklecie:
        sprite = get_sprite(zaklecie_ss, frame, 0, 64, 88)
        sprite = pygame.transform.scale(sprite, (256, 352))
        screen.blit(sprite, (screen_width//2-128, screen_height//2-176))
        frame = frame + 64
    else:
        frame = 0
    if frame >= 704:
        zaklecie = False
        buttons_active = True
        enemy_hp -= power
        for i in range(power):
            particle = Particle(screen_width//2, screen_height//2)
            all_sprites.add(particle)
    
    if pochloniecie:
        sprite = get_sprite(pochloniecie_ss, aframe, 0, 48, 64)
        sprite = pygame.transform.scale(sprite, (256, 341))
        screen.blit(sprite, (screen_width//2-128, screen_height//2-170))
        aframe = aframe + 48
    else:
        aframe = 0
    if aframe >= 15*48:
        pochloniecie = False
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

    manager = pygame_gui.UIManager((screen_width,screen_height))
    manager.process_events(event)
    manager.update(0.2)
    manager.draw_ui(screen)

    #ekran

    pygame.display.update()
    pygame.display.flip()
    clock.tick(15)
    
    #koniec gry

    if dead:

        pygame.mixer_music.stop()

        end_text = font.render("Game Over :)", True, (255,255,255))
        death_text = font.render(death_text, True, (255,255,255))
        level_count_text = font.render("Udało ci się dotrzeć do "+str(room)+" pokoju "+str(level)+" poziomu!", True, (255,255,255))
        screen.fill((0,0,0))
        screen.blit(level_count_text, (screen_width//2-level_count_text.get_width()//2,screen_height//2))
        screen.blit(death_text, (screen_width//2-death_text.get_width()//2,screen_height//2-25))
        screen.blit(end_text, (screen_width//2-end_text.get_width()//2,screen_height//2-50))

        #zapis rozgrywki

        rekord = "l"+str(level)+"r"+str(room)
        with open("scoreboard.txt","r") as plik:
            hs = ""
            hs_text = ""
            pr = plik.readlines()
            for i in range(len(pr)):
                if pr[i] > hs:
                    hs = pr[i]
            if rekord > hs:
                hs_text = font.render("High Score!!!", True, (255,255,255))
                screen.blit(hs_text, (screen_width//2-end_text.get_width()//2,screen_height//2-75))
        if len(pr) > 0:
            with open("scoreboard.txt","a") as plik:
                plik.write(str(rekord)+'\n')
        else:
            with open("scoreboard.txt","w") as plik:
                plik.write(str(rekord)+'\n')
        
        health = 20
        energy = 20
        hunger = 20
        power = 1
        shots = 0
        shot_power = 1
        shooting = False
        zaklecie = False
        pochloniecie = False

        max_health = 20
        max_energy = 20
        max_hunger = 20

        mapa = lvl_gen(lvl_x, lvl_y)

        level = 0
        room = 0
        enemy = 0

        pygame.display.flip()
        pygame.time.delay(6000)
        death_text = ""
        menu = True
        dead = False
        popup_open = False
        buttons_active = True
        playmusic('music/SeeingDouble_Loopable.wav')


pygame.quit()