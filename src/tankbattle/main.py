import conf
import page_logic

# 游戏主循环
def main_loop():
    current_page = "select_chapter"  # 初始页面为开始页面

    while True:
        if current_page == "select_chapter":
            current_page = page_logic.select_chapter_logic(conf)
        elif current_page == "chapter1":
            print("开始游戏关卡1")
            run_game("map1.json")
        elif current_page == "chapter2":
            print("开始游戏关卡2")
            run_game("map2.json")
        elif current_page == "chapter3":
            print("开始游戏关卡3")
            run_game("map3.json")

# 运行游戏
def run_game(josn_name):
    game_run_result = page_logic.game_run_logic(conf,josn_name)
    if game_run_result is not None:
        if page_logic.game_end_logic(conf,game_run_result):
            return page_logic.select_chapter_logic(conf)
    else:
        return "select_chapter"

# 运行游戏
main_loop()
