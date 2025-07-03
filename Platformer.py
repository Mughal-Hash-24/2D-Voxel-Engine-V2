import pygame, sys, os, random
import data.engine as e
from perlin_noise import PerlinNoise
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('2D Voxel Engine V2')

WINDOW_SIZE = (1200,800)

seed = random.randint(1,1000000000000000000)
print(seed)

CHUNK_SIZE = 8

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

# def generate_enemies():
#     if enemies == None:
#         for i in range(1):
#             enemies.append([0,e.entity(random.randint(0,600)-300, 100, 13, 13, 'enemy')])

def generate_chunk(x, y):
    chunk_data = []

    noise = PerlinNoise(octaves=6, seed=seed)  # Adjust the number of octaves for smoother terrain
    scale = 0.015
      # Adjust the scale for smoother terrain

    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos

            height = int(noise([target_x * scale, target_y * scale])*13)
            # print(height)

            tile_type = 0
            if target_y > 10 + height:
                tile_type = 2
            elif target_y == 10 + height:
                tile_type = 1
            elif target_y == 9 + height:
                if random.randint(1, 5) == 1:
                    tile_type = 3
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
            # generate_enemies()
            # print("chunk generated")
    return chunk_data

# class jumper_obj():
#     def __init__(self, loc):
#         self.loc = loc

#     def render(self, surf, scroll):
#         surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1]- scroll[1]))

#     def get_rect(self):
#         return pygame.Rect(self.loc[0], self.loc[1], 8, 9)
    
#     def collision_test(self,rect):
#         jumper_rect = self.get_rect()
#         return jumper_rect.colliderect(rect)

        
e.load_animations('data/images/entities/')

game_map = {}

grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
plant_img = pygame.image.load('data/images/plant.png').convert()
plant_img.set_colorkey((255,255,255))
jumper_img = pygame.image.load('data/images/jumper.png').convert()
jumper_img.set_colorkey((255,255,255))

tile_index = {
    1:grass_img,
    2:dirt_img,
    3:plant_img
}

jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'),pygame.mixer.Sound('data/audio/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

kill_sound = pygame.mixer.Sound('data/audio/kill_sound.mp3')
kill_sound.set_volume(0.1)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

grass_sound_timer = 0

player = e.entity(100,100,16,16,'player')

enemies = []
for i in range(5):
    enemies.append([0,e.entity(200, 100, 16, 16, 'enemy')])

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

bosses = []
for i in range(1):
    bosses.append([0 ,e.entity(200, 100, 40, 40, 'boss')])

fire_balls = []

# jumper_objects = []
# for i in range(5):
#     jumper_objects.append(jumper_obj((random.randint(0,600)-300, 80)))

hp_value = 70

count = 1

enemy_visible = True

enemy_hp = 50

last_click_time = 0

cooldown = 500

KNOCKBACK_FORCE = 50

kills = 0
boss_kills = 0

font = pygame.font.SysFont('calibri', 15, True)

kills_text = font.render("Kills: " + str(kills), True, (10,10,10))

boss_hp = 200

boss_visible = True
fire_visible = True

facing_left = False
facing_right = False

fire_count = 0
fire_facing_l = False
fire_facing_r = True

while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    kills_text = font.render("Kills: " + str(kills), True, (10,10,10))

    true_scroll[0] += (player.x-true_scroll[0]-152)/20
    true_scroll[1] += (player.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(20,170,150),obj_rect)
        else:
            pygame.draw.rect(display,(15,76,73),obj_rect)

    tile_rects = []
    for y in range(4):
        for x in range(4):
            target_x = x-1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y-1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            # In the game loop where you draw the tiles
            for tile in game_map[target_chunk]:
                if tile[1] == 3:  # Plant tile
                # Position the plant tile on top of the terrain
                    display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                else:
                    # Draw other tiles normally
                    display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))



    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    current_time = pygame.time.get_ticks()

    attack = pygame.mouse.get_pressed()[0]
    fired = pygame.mouse.get_pressed()[2]

    if fired:
        # print(fire_facing_l)
        # print(fire_facing_r)
        if facing_left:
            fire_facing_l = facing_left
            fire_facing_r = False
        elif facing_right:
            fire_facing_r = facing_right
            fire_facing_l = False
        fire_count+=1
        if fire_count > 1:
            fire_count = 1
        if fire_count == 1:
            fire_balls.append(e.entity(player.x, player.y, 12, 8, 'fire_ball'))
            fire_count = 0
    
    fire_balls_to_remove = []
    display_r = pygame.Rect(scroll[0], scroll[1], 300, 200)
    
    fire_movement = [0,0]
    for fire in fire_balls:
        if fire_facing_l:
            fire_movement[0] = -5
            fire.set_flip(True)
            fire.set_action('idle')
        elif fire_facing_r:
            fire_movement[0] = 5
            fire.set_flip(False)
            fire.set_action('idle')
        else:
            fire_movement[0] = 0

        collisions_types = fire.move(fire_movement, tile_rects)

        if collisions_types['bottom'] == True:
            # fire_visible = False
            fire_balls_to_remove.append(fire)
        if collisions_types['left'] == True:
            # fire_visible = False
            fire_balls_to_remove.append(fire)
        if collisions_types['right'] == True:
            # fire_visible = False
            fire_balls_to_remove.append(fire)
    
        if fire_visible:
            fire.change_frame(1)
            fire.display(display,scroll)
            fire_visible = True

        if enemy[1].obj.rect.colliderect(fire.obj.rect):
            enemy_hp -= 10
            fire_balls_to_remove.append(fire)
            print(enemy_hp)

            if enemy_hp <= 0:   
                enemies_to_remove.append(enemy)
                enemy_hp = 50
                hp_value = 70
                kills += 1
                # fire_visible = False
                

        # if not display_r.colliderect(fire.obj.rect):
        #     fire_balls_to_remove.append(fire)
        #     fire_visible = False

    for fires in fire_balls_to_remove:
        fire_balls.remove(fires)

    if player_movement[0] == 0 and not attack:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action('run')
    
    enemies_to_remove = []

    bosses_to_remove = []

    for enemy in enemies:
        # pygame.draw.rect(display, (255,0,0), pygame.Rect(enemy[1].x + 3, enemy[1].y - 2, 7, 1))
        if attack and current_time - last_click_time > cooldown and player.obj.rect.colliderect(enemy[1].obj.rect):
            # Perform actions when the player attacks an enemy
            player.set_action('attack', True)

            kill_sound.play()

            last_click_time = current_time
            # Add the enemy to the removal list
            enemy_hp -= 25 
            print(enemy_hp)

            dx = enemy[1].x - player.x
            dy = enemy[1].y - player.y
            distance = (dx**2 + dy**2)**0.5

            if distance != 0:
                dx /= distance
                dy /= distance

            # Apply knockback force to the enemy in the opposite direction from the player
                enemy[1].x += dx * KNOCKBACK_FORCE
                enemy[1].y += dy * KNOCKBACK_FORCE

            if enemy_hp <= 0:   
                enemies_to_remove.append(enemy)
                enemy_hp = 50
                hp_value = 70
                kills += 1

                if kills >= 3 and kills % 2 == 0:
                    for i in range(2):
                        enemies.append([0,e.entity(random.randint(0,600)-300, 100, 16, 16, 'enemy')])

    
    # Remove the collided enemies from the main list
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    display_r = pygame.Rect(scroll[0], scroll[1], 300, 200)

    if kills >= 10:
        for boss in bosses:
            if display_r.colliderect(boss[1].obj.rect):
                boss[0] += 0.2
                if boss[0] > 3:
                    boss[0] = 3
                boss_movement = [0, boss[0]]
                if player.x > boss[1].x + 40:
                    boss_movement[0] = 1
                if player.x < boss[1].x -40:
                    boss_movement[0] = -1

                collisions_types = boss[1].move(boss_movement, tile_rects)
                if collisions_types['bottom'] == True:
                    boss[0] = 0
                if collisions_types['left'] == True:
                    boss[0] = -2

                if collisions_types['right'] == True:
                    boss[0] = -2
                
                # enemy[1].display(display, scroll)

                
                if player.obj.rect.colliderect(boss[1].obj.rect):
                    count -= 1
                    if count == 0:
                        hp_value -= 10
                        count = 20
                        boss[1].set_action('attack', True)

                if boss_movement[0] > 0:
                    boss[1].set_flip(False)
                    boss[1].set_action('run')
                if boss_movement[0] < 0:
                    boss[1].set_flip(True)
                    boss[1].set_action('run')
                if boss_movement[0] == 0 and not player.obj.rect.colliderect(boss[1].obj.rect):
                    boss[1].set_action('idle')
    
        if boss_visible:
            boss[1].change_frame(1)
            boss[1].display(display,scroll)


    for boss in bosses:
        if attack and current_time - last_click_time > cooldown and player.obj.rect.colliderect(boss[1].obj.rect):
            player.set_action('attack', True)

            kill_sound.play()

            last_click_time = current_time
            # Add the enemy to the removal list
            boss_hp -= 25 
            print(boss_hp)

            if boss_hp == 0:   
                bosses_to_remove.append(boss)
                boss_hp = 50
                hp_value = 70
                boss_kills += 1
                boss_visible = False

    for boss in bosses_to_remove:
        bosses.remove(boss)

    collisions_types = player.move(player_movement,tile_rects)

    if collisions_types['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display,scroll)

    # for jumper in jumper_objects:
    #     jumper.render(display, scroll)
    #     if jumper.collision_test(player.obj.rect):
    #         vertical_momentum = -8

    display_r = pygame.Rect(scroll[0], scroll[1], 300, 200)

    for enemy in enemies:
        if display_r.colliderect(enemy[1].obj.rect):   
            enemy[0] += 0.2
            if enemy[0] > 3:
                enemy[0] = 3
            enemy_movement = [0,enemy[0]]
            if player.x > enemy[1].x + 4:
                enemy_movement[0] = 1
                # enemy.set_action('run')
            if player.x < enemy[1].x - 4:
                enemy_movement[0] = -1
                # enemy.set_action('run')
            collisions_types = enemy[1].move(enemy_movement, tile_rects)
            if collisions_types['bottom'] == True:
                enemy[0] = 0
            if collisions_types['left'] == True:
                enemy[0] = -2

            if collisions_types['right'] == True:
                enemy[0] = -2
            
            # enemy[1].display(display, scroll)

            
            if player.obj.rect.colliderect(enemy[1].obj.rect):
                count -= 1
                if count == 0:
                    hp_value -= 5
                    count = 20
                    enemy[1].set_action('attack', True)

            if enemy_movement[0] > 0:
                enemy[1].set_flip(False)
                enemy[1].set_action('run')
            if enemy_movement[0] < 0:
                enemy[1].set_flip(True)
                enemy[1].set_action('run')
            if enemy_movement[0] == 0 and not player.obj.rect.colliderect(enemy[1].obj.rect):
                enemy[1].set_action('idle')

        if enemy_visible:
            enemy[1].change_frame(1)
            enemy[1].display(display,scroll)


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_RIGHT:
                moving_right = True
                facing_right = True
                facing_left = False
            if event.key == K_LEFT:
                moving_left = True
                facing_left = True
                facing_right = False
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_SPACE:
                player.set_action('attack')
    

    player_hp = pygame.Rect(5, 5, hp_value, 7)

    pygame.draw.rect(display,(255, 0, 0) ,player_hp)

    if hp_value == 0:
        pygame.quit()
        sys.exit()

    display.blit(kills_text, (244,3))
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)