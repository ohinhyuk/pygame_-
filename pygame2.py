import pygame
import os

from pygame import image
from pygame import event
from pygame.constants import K_SPACE

pygame.init()

#초기 설정 모드

#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 제목 설정
pygame.display.set_caption("공 쪼개기 게임")

#FPS
clock = pygame.time.Clock()

############################################################################

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path,"image2")

# 1.사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
# 배경 만들기

background = pygame.image.load(os.path.join(image_path,"background.png"))
background_size = background.get_rect().size
background_width = background_size[0]
background_height = background_size[1]

# stage 만들기

stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 만들기

character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width /2 -character_width/2
character_y_pos = screen_height - character_height - stage_height
character_x_speed = 10

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

weapons = []

weapon_speed = 5

weapon_to_remove = -1

#공 만들기

#공이미지
ball_image = [
    pygame.image.load(os.path.join(image_path,"ball1.png")),
    pygame.image.load(os.path.join(image_path,"ball2.png")),
    pygame.image.load(os.path.join(image_path,"ball3.png")),
    pygame.image.load(os.path.join(image_path,"ball4.png"))
]
#공 최초 속도
ball_init_y_speed = [-18 ,-15 ,-12,-9]

#공 속성들
balls = []
balls.append({
    "x_pos" : 50,
    "y_pos" : 50,
    "x_to" : 3,
    "y_to" : -6,
    "img_idx" : 0,
    "init_y_speed" : ball_init_y_speed[0]
})


#이동 방향
x_to = 0

ball_to_remove = -1
###################################################
running = True
# 게임 이벤트 처리
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_to -= character_x_speed
            elif event.key ==pygame.K_RIGHT:
                x_to += character_x_speed
            if event.key == K_SPACE:
                weapon_x_pos = character_x_pos +character_width/2 - weapon_width
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        elif event.type ==pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                x_to =0
        

#####################################################
#게임 캐릭터 위치 정의

    character_x_pos += x_to
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

#무기 위치 정의

    weapons = [ [w[0] , w[1]- weapon_speed]  for w in weapons]
    weapons = [ [w[0],w[1]] for w in weapons if w[1] >0]

# 공 위치 정의

    for idx , val in enumerate(balls):
        ball_x_pos = val["x_pos"]
        ball_y_pos = val["y_pos"]
        ball_idx_img = val["img_idx"]

        ball_size = ball_image[ball_idx_img].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_x_pos <0 or ball_x_pos > screen_width - ball_width:
            val["x_to"] = val["x_to"] * -1
        if ball_y_pos > screen_height - stage_height - ball_height:
            val["y_to"] = val["init_y_speed"]
        else:
            val["y_to"] +=0.5
        val["x_pos"] += val["x_to"]
        val["y_pos"] += val["y_to"]
        
############################################################################
#충돌 처리

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for idx , val in enumerate(balls):
        ball_idx_img = val["img_idx"]
        ball_rect = ball_image[ball_idx_img].get_rect()
        ball_x_pos = val["x_pos"]
        ball_y_pos = val["y_pos"]
        ball_rect.left = ball_x_pos
        ball_rect.top = ball_y_pos
        
        if character_rect.colliderect(ball_rect):
            running = False
            break


        for weapon_idx , weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = idx

                if ball_idx_img < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_image[ball_idx_img + 1].get_rect()
                    small_ball_rect_width = small_ball_rect.size[0]
                    small_ball_rect_height = small_ball_rect.size[1]
                    balls.append({
                        "x_pos" : ball_x_pos + ball_width/2 -small_ball_rect_width/2,
                        "y_pos" : ball_y_pos + ball_height/2 - small_ball_rect_height/2,
                        "x_to" : -3,
                        "y_to" : -6,
                        "img_idx" : ball_idx_img + 1,
                        "init_y_speed" : ball_init_y_speed[ball_idx_img + 1]
                    })

                    balls.append({
                        "x_pos" : ball_x_pos + ball_width/2 -small_ball_rect_width/2,
                        "y_pos" : ball_y_pos + ball_height/2 - small_ball_rect_height/2,
                        "x_to" : 3,
                        "y_to" : -6,
                        "img_idx" : ball_idx_img + 1,
                        "init_y_speed" : ball_init_y_speed[ball_idx_img + 1]
                    })
                break 
    if ball_to_remove > -1:
        print(ball_to_remove)
        del balls[ball_to_remove]
        ball_to_remove = -1   
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1    
        

##############################################################################
    screen.blit(background,(0,0))
    for weapon_x_pos , weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    for idx , val in enumerate(balls):
        ball_x_pos = val["x_pos"]
        ball_y_pos = val["y_pos"]
        ball_idx_img = val["img_idx"]
        screen.blit(ball_image[ball_idx_img],(ball_x_pos,ball_y_pos))


    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    
    pygame.display.update()

pygame.quit()