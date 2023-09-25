import conf
import page_logic


# 游戏主循环
def main_loop():
    current_page = "select_chapter"  # 初始页面为开始页面

    while True:
        if current_page == "select_chapter" or current_page is None:
            current_page = page_logic.select_chapter_logic(conf)
        elif current_page == "chapter1":
            print("开始chapter1")
            current_page = page_logic.game_run_logic(conf, "map1.json")
        elif current_page == "chapter2":
            print("开始chapter2")
            current_page = page_logic.game_run_logic(conf, "map2.json")
        elif current_page == "chapter3":
            print("开始chapter3")
            current_page = page_logic.game_run_logic(conf, "map3.json")
        elif current_page == "win_page":
            print("开始win页面")
            current_page = page_logic.game_end_logic(conf, "win")
        elif current_page == "lose_page":
            print("开始lose页面")
            current_page = page_logic.game_end_logic(conf, "lose")


# 运行游戏
main_loop()
