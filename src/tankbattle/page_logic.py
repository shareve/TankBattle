import random
import sys
import pygame

import utils
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
    next_page = None
    clock = pygame.time.Clock()

    while next_page is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    next_page = "select_chapter"
        # 绘制页面的代码
        conf.screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 36)
        if game_run_result == "lose":
            text = "YOU LOSE"
        else:
            text = "YOU WIN"

        text_render = font.render(text, True, (0, 0, 0))

        x = (conf.SCREEN_WIDTH-100) // 2
        y = (conf.SCREEN_HEIGHT) // 2

        conf.screen.blit(text_render, (x, y))

        pygame.display.flip()
        clock.tick(60)
    return next_page


# 游戏执行页面
def game_run_logic(conf, josn_name):
    # 重置精灵组:坦克，我方坦克，敌方坦克
    conf.propGroup = pygame.sprite.Group()
    conf.tankGroup = pygame.sprite.Group()
    conf.ourTankGroup = pygame.sprite.Group()
    conf.enemyTankGroup = pygame.sprite.Group()
    conf.bulletGroup = pygame.sprite.Group()
    conf.ourBulletGroup = pygame.sprite.Group()
    conf.enemyBulletGroup = pygame.sprite.Group()

    conf.start_sound.play()

    json_config = utils.load_json_conf(josn_name)

    # 设置title
    pygame.display.set_caption(json_config["title"])

    enemy_tank_seq = 1000
    bgMap = map.Map(json_config)

    our_tank1 = Tank(1, 0, 1, 0, "our", None, None, 3, 8, 22)
    conf.tankGroup.add(our_tank1)
    conf.ourTankGroup.add(our_tank1)
    ourTank2 = Tank(2, 1, 1, 0, "our", None, None, 3, 16, 22)
    conf.tankGroup.add(ourTank2)
    conf.ourTankGroup.add(ourTank2)

    # 按照位置分配敌方坦克,总数量为 3个位置*2个life_times=6个
    for i in range(3):
        enemy_tank_seq = enemy_tank_seq + 1
        enemy = Tank(enemy_tank_seq, None, 2, None, "enemy", 1, True, 3, 11 * i, 0)
        print("enemy出生位置的坐标：", enemy.x, enemy.y)
        conf.tankGroup.add(enemy)
        conf.enemyTankGroup.add(enemy)

    clock = pygame.time.Clock()

    game_run_result = None
    while game_run_result is None:
        for event in pygame.event.get():
            # 页面退出事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击位置的坐标
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("鼠标点击位置的坐标：", mouse_x, mouse_y)

            # 页面出随机道具事件
            if event.type == conf.EVENT_CREATE_PROP:
                the_prop = Prop()
                conf.propGroup.add(the_prop)
                print("EVENT_CREATE_PROP", the_prop.kind,the_prop.rect)

            # 创建我们的坦克
            if event.type == conf.EVENT_NEW_OUR_TANK:
                tank = event.tank
                if tank.player_id == 0:
                    our_tank1 = Tank(tank.id, tank.player_id, tank.life_times, 0, "our", None, None, 3, 8,22)
                    print("ourTank1.life_times", our_tank1.life_times)
                    conf.tankGroup.add(our_tank1)
                    conf.ourTankGroup.add(our_tank1)
                else:
                    ourTank2 = Tank(2, 1, 3, 0, "our", None, None, 3, 16, 22)
                    print("ourTank2.life_times", ourTank2.life_times)
                    conf.tankGroup.add(ourTank2)
                    conf.ourTankGroup.add(ourTank2)

            # 创建新的敌对坦克
            if event.type == conf.EVENT_NEW_ENEMY_TANK:
                tank = event.tank
                birth_place = random.choice([0, 1, 2])
                enemy_tank_rand = Tank(tank.id, None, tank.life_times, None, "enemy", 1, True, 3,
                                       11 * birth_place, 0)
                # 如果位置有冲突，1s后再试
                list = pygame.sprite.spritecollide(enemy_tank_rand, conf.tankGroup, False, None)
                if list:
                    enemy_tank_rand = None
                    pygame.time.set_timer(event, 1000, 1)
                else:
                    conf.tankGroup.add(enemy_tank_rand)
                    conf.enemyTankGroup.add(enemy_tank_rand)

            # 敌人全部爆
            if event.type == conf.EVENT_ALL_ENEMY_BOOM:
                for enemy_tank in conf.enemyTankGroup:
                    conf.enemyTankGroup.remove(enemy_tank)
                    conf.tankGroup.remove(enemy_tank)
                    if enemy_tank.life_times > 0:
                        enemy_tank.life_times -= 1
                        print("enemyTank.life_times", enemy_tank.id, enemy_tank.life_times)
                        # 创建一个新敌人坦克出现事件对象，并携带参数
                        event_rand_enemy = pygame.event.Event(conf.EVENT_NEW_ENEMY_TANK, tank=enemy_tank)
                        pygame.event.post(event_rand_enemy)
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
                for x, y in conf.home_near_xy:
                    bgMap.iron = map.Iron()
                    bgMap.iron.rect.left, bgMap.iron.rect.top = utils.gain_pixel(x),utils.gain_pixel(y)
                    print("bgMap.iron.rect",bgMap.iron.rect)
                    bgMap.ironGroup.add(bgMap.iron)
                pygame.time.set_timer(pygame.event.Event(conf.EVENT_NOT_IRON_HOME), 8000, 1)
            # EVENT_NOT_IRON_HOME
            if event.type == conf.EVENT_NOT_IRON_HOME:
                for this_iron in bgMap.ironGroup:
                    for this_iron.x, this_iron.y in conf.home_near_xy:
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
                print("EVENT_ADD_LIFE", event.tank.id, event.tank.life_times)

            # EVENT_NONE_LIFE
            if event.type == conf.EVENT_NONE_OUR_LIFE:
                game_run_result = "lose_page"
            # EVENT_HOME_DESTROYED
            if event.type == conf.EVENT_HOME_DESTROYED:
                bgMap.change_home_destroyed()
                game_run_result = "lose_page"
            # EVENT_NONE_ENEMY_LIFE
            if event.type == conf.EVENT_NONE_ENEMY_LIFE:
                game_run_result = "win_page"

        # 校验是否已经全部没有生命值
        utils.check_lose_win()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_j]:
            bullet = our_tank1.shoot()
            conf.bulletGroup.add(bullet)
            conf.ourBulletGroup.add(bullet)
        if key_pressed[pygame.K_w]:
            our_tank1.move_dir(bgMap, conf.tankGroup,conf.up_dir)
        elif key_pressed[pygame.K_s]:
            our_tank1.move_dir(bgMap, conf.tankGroup,conf.down_dir)
        elif key_pressed[pygame.K_a]:
            our_tank1.move_dir(bgMap, conf.tankGroup,conf.left_dir)
        elif key_pressed[pygame.K_d]:
            our_tank1.move_dir(bgMap, conf.tankGroup,conf.right_dir)



        # 对方进行的行动
        for tank in conf.enemyTankGroup:
            bullet = tank.let_ai_action(bgMap, conf.tankGroup)
            if bullet:
                conf.bulletGroup.add(bullet)
                conf.enemyBulletGroup.add(bullet)

        # 渲染地图，坦克，子弹,道具
        bgMap.this_blit(conf.screen)
        for tank in conf.tankGroup:
            tank.this_blit(conf.screen)
        for bullet in conf.bulletGroup:
            bullet.this_blit(conf.screen, bgMap)
        for this_prop in conf.propGroup:
            this_prop.this_blit(conf.screen)

        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)
    return game_run_result
