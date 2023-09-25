import random
import sys

import pygame

from tank import Tank
from prop import Prop
import map


# 选择关卡页面
def select_chapter_logic(conf):
    selected_chapter = "select_chapter"

    while selected_chapter == "select_chapter":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_1:
                    selected_chapter = "chapter1"
                elif event.key == pygame.K_2:
                    selected_chapter = "chapter2"
                elif event.key == pygame.K_3:
                    selected_chapter = "chapter3"

        conf.screen.blit(conf.background_image, (0, 0))

        # 绘制游戏关卡选项
        start_text = conf.font.render("请输入对应数字:", True, (255, 255, 255))
        conf.screen.blit(start_text, (0, 0))

        for i, chapter in enumerate(conf.game_chapters):
            mode_text = conf.font.render(chapter, True, (255, 255, 255))
            conf.screen.blit(mode_text, (conf.SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

    return selected_chapter


# 游戏结束页面
def game_end_logic(conf, game_run_result):
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    done = True
        # 绘制页面的代码
        conf.screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 36)
        if game_run_result == "lose":
            text = "YOU LOSE"
        else:
            text = "YOU WIN"

        text_render = font.render(text, True, (0, 0, 0))

        # image_rect = conf.game_over.get_rect()
        x = (conf.SCREEN_WIDTH) // 2
        y = (conf.SCREEN_HEIGHT - 36) // 2

        conf.screen.blit(text_render, (x, y))

        pygame.display.flip()
        clock.tick(60)
    return done


# 游戏执行页面
def game_run_logic(conf, josn_name):
    # 初始化 Pygame
    pygame.init()
    pygame.mixer.init()

    # 重置精灵组:坦克，我方坦克，敌方坦克
    conf.propGroup = pygame.sprite.Group()
    conf.tankGroup = pygame.sprite.Group()
    conf.ourTankGroup = pygame.sprite.Group()
    conf.enemyTankGroup = pygame.sprite.Group()
    conf.bulletGroup = pygame.sprite.Group()
    conf.ourBulletGroup = pygame.sprite.Group()
    conf.enemyBulletGroup = pygame.sprite.Group()

    # 定义屏幕宽度和高度
    SCREEN_WIDTH = 630
    SCREEN_HEIGHT = 630

    conf.start_sound.play()
    # 创建屏幕对象
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    json_config = conf.load_json_conf(josn_name)

    pygame.display.set_caption("TankBattle")

    enemy_tank_seq = 1000
    bgMap = map.Map(json_config)

    ourTank1 = Tank(1, 0, 1, 0, "our", None, None, 3, 3 + 24 * 8, 3 + 24 * 24)
    conf.tankGroup.add(ourTank1)
    conf.ourTankGroup.add(ourTank1)
    ourTank2 = Tank(2, 1, 0, 0, "our", None, None, 3, 3 + 24 * 16, 3 + 24 * 24)
    conf.tankGroup.add(ourTank2)
    conf.ourTankGroup.add(ourTank2)

    for i in range(4):
        enemy_tank_seq = enemy_tank_seq + 1
        enemyTank1 = Tank(enemy_tank_seq, None, 1, None, "enemy", 1, True, 3, 3 + i * 12 * 24, 3 + 0 * 24)
        conf.tankGroup.add(enemyTank1)
        conf.enemyTankGroup.add(enemyTank1)

    clock = pygame.time.Clock()

    game_run_result = None
    while game_run_result is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 页面出随机道具事件
            if event.type == conf.EVENT_CREATE_PROP:
                the_prop = Prop()
                conf.propGroup.add(the_prop)
                print("EVENT_CREATE_PROP", the_prop.rect)

            # 创建我们的坦克
            if event.type == conf.EVENT_NEW_OUR_TANK:
                tank = event.tank
                if tank.player_id == 0:
                    ourTank1 = Tank(tank.id, tank.player_id, tank.life_times, 0, "our", None, None, 3, 3 + 24 * 8,
                                    3 + 24 * 24)
                    print("ourTank1.life_times", ourTank1.life_times)
                    conf.tankGroup.add(ourTank1)
                    conf.ourTankGroup.add(ourTank1)
                else:
                    ourTank2 = Tank(2, 1, 3, 0, "our", None, None, 3, 3 + 24 * 16, 3 + 24 * 24)
                    print("ourTank2.life_times", ourTank2.life_times)
                    conf.tankGroup.add(ourTank2)
                    conf.ourTankGroup.add(ourTank2)

            # 创建新的敌对坦克
            if event.type == conf.EVENT_NEW_ENEMY_TANK:
                tank = event.tank
                birth_place = random.choice([0, 1, 2])
                enemyTankRand = Tank(tank.id, None, tank.life_times, None, "enemy", 1, True, 3,
                                     3 + birth_place * 12 * 24,
                                     3 + 0 * 24)
                # 如果位置有冲突，1s后再试
                list = pygame.sprite.spritecollide(enemyTankRand, conf.tankGroup, False, None)
                if list:
                    enemyTankRand = None
                    pygame.time.set_timer(event, 1000, 1)
                else:
                    conf.tankGroup.add(enemyTankRand)
                    conf.enemyTankGroup.add(enemyTankRand)

            # 敌人全部爆
            if event.type == conf.EVENT_ALL_ENEMY_BOOM:
                for enemyTank in conf.enemyTankGroup:
                    conf.enemyTankGroup.remove(enemyTank)
                    conf.tankGroup.remove(enemyTank)
            # EVENT_LOCK
            if event.type == conf.EVENT_LOCK:
                for enemyTank in conf.enemyTankGroup:
                    enemyTank.locked = True
                pygame.time.set_timer(pygame.event.Event(conf.EVENT_NOT_LOCK), 8000, 1)
            # EVENT_NOT_LOCK
            if event.type == conf.EVENT_NOT_LOCK:
                for enemyTank in conf.enemyTankGroup:
                    enemyTank.locked = False
            # EVENT_IRON_HOME
            if event.type == conf.EVENT_IRON_HOME:
                for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                    bgMap.iron = map.Iron()
                    bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                    print("bgMap.iron.rect",bgMap.iron.rect)
                    bgMap.ironGroup.add(bgMap.iron)
                pygame.time.set_timer(pygame.event.Event(conf.EVENT_NOT_IRON_HOME), 8000, 1)
            # EVENT_NOT_IRON_HOME
            if event.type == conf.EVENT_NOT_IRON_HOME:
                for this_iron in bgMap.ironGroup:
                    for this_iron.x, this_iron.y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24),
                                                     (11, 25),
                                                     (14, 25)]:
                        bgMap.ironGroup.remove(this_iron)

            # EVENT_PROTECT
            if event.type == conf.EVENT_PROTECT:
                print("EVENT_PROTECT", pygame.time.get_ticks())
                event.tank.protected = True
                pygame.time.set_timer(pygame.event.Event(conf.EVENT_NOT_PROTECT, tank=event.tank), 8000, 1)
            # EVENT_NOT_PROTECT
            if event.type == conf.EVENT_NOT_PROTECT:
                print("EVENT_NOT_PROTECT", pygame.time.get_ticks())
                event.tank.protected = False
            # 自己到star级
            if event.type == conf.EVENT_LEVEL_STAR:
                event.tank.level_up(1)
            # 自己到gun级
            if event.type == conf.EVENT_LEVEL_GUN:
                event.tank.level_up(3)
            # 加一条命
            if event.type == conf.EVENT_ADD_LIFE:
                event.tank.life_times = event.tank.life_times + 1

            # EVENT_NONE_LIFE
            if event.type == conf.EVENT_NONE_OUR_LIFE:
                game_run_result = "lose"
            # EVENT_HOME_DESTROYED
            if event.type == conf.EVENT_HOME_DESTROYED:
                bgMap.change_home_destroyed()
                game_run_result = "lose"
            # EVENT_NONE_ENEMY_LIFE
            if event.type == conf.EVENT_NONE_ENEMY_LIFE:
                game_run_result = "win"

        # 校验是否已经全部没有生命值
        conf.check_lose_win()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_j]:
            bullet = ourTank1.shoot()
            conf.bulletGroup.add(bullet)
            conf.ourBulletGroup.add(bullet)
        if key_pressed[pygame.K_w]:
            ourTank1.move_up(bgMap, conf.tankGroup)
        elif key_pressed[pygame.K_s]:
            ourTank1.move_down(bgMap, conf.tankGroup)
        elif key_pressed[pygame.K_a]:
            ourTank1.move_left(bgMap, conf.tankGroup)
        elif key_pressed[pygame.K_d]:
            ourTank1.move_right(bgMap, conf.tankGroup)

        # 对方进行的行动
        for tank in conf.enemyTankGroup:
            bullet = tank.let_ai_action(bgMap, conf.tankGroup)
            if bullet:
                conf.bulletGroup.add(bullet)
                conf.enemyBulletGroup.add(bullet)

        # 渲染地图，坦克，子弹,道具
        bgMap.this_blit(screen)
        for tank in conf.tankGroup:
            tank.this_blit(screen)
        for bullet in conf.bulletGroup:
            bullet.this_blit(screen, bgMap)
        for this_prop in conf.propGroup:
            this_prop.this_blit(screen)

        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)
    return game_run_result
