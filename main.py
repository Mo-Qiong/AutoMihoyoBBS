import time
import push
import login
import config
import random
import honkai2
import genshin
import setting
import mihoyobbs
import honkai3rd
from loghelper import log
from error import CookieError


def main():
    # 初始化，加载配置
    return_data = "\n米游社: "
    config.load_config()
    if config.config["enable"]:
        # 检测参数是否齐全，如果缺少就进行登入操作
        if config.config["account"]["login_ticket"] == "" or config.config["account"]["stuid"] == "" or \
                config.config["account"]["stoken"] == "":
            # 登入，如果没开启bbs全局没打开就无需进行登入操作
            if config.config["mihoyobbs"]["enable"]:
                login.login()
            time.sleep(random.randint(2, 8))
        # 获取要使用的BBS列表,#判断是否开启bbs_Signin_multi
        if config.config["mihoyobbs"]["checkin_multi"]:
            # 用这里的方案可以实现当让id在第一个的时候为主社区
            for i in config.config["mihoyobbs"]["checkin_multi_list"]:
                for i2 in setting.mihoyobbs_List:
                    if i == int(i2["id"]):
                        setting.mihoyobbs_List_Use.append(i2)
        else:
            # 关闭bbs_Signin_multi后只签到大别墅
            for i in setting.mihoyobbs_List:
                if int(i["id"]) == 5:
                    setting.mihoyobbs_List_Use.append(i)
        # 米游社签到
        if config.config["mihoyobbs"]["enable"]:
            bbs = mihoyobbs.Mihoyobbs()
            if bbs.Task_do["bbs_Sign"] and bbs.Task_do["bbs_Read_posts"] and bbs.Task_do["bbs_Like_posts"] and \
                    bbs.Task_do["bbs_Share"]:
                return_data += "\n" + f"今天已经全部完成了！\n" \
                                      f"一共获得{mihoyobbs.today_have_get_coins}个米游币\n目前有{mihoyobbs.Have_coins}个米游币"
                log.info(f"今天已经全部完成了！一共获得{mihoyobbs.today_have_get_coins}个米游币，目前有{mihoyobbs.Have_coins}个米游币")
            else:
                i = 0
                while mihoyobbs.today_get_coins != 0 and i < 3:
                    if i > 0:
                        bbs.refresh_list()
                    if config.config["mihoyobbs"]["checkin"]:
                        bbs.signing()
                    if config.config["mihoyobbs"]["read_posts"]:
                        bbs.read_posts()
                    if config.config["mihoyobbs"]["like_posts"]:
                        bbs.like_posts()
                    if config.config["mihoyobbs"]["share_post"]:
                        bbs.share_post()
                    bbs.get_tasks_list()
                    i += 1
                return_data += "\n" + f"今天已经获得{mihoyobbs.today_have_get_coins}个米游币\n" \
                                      f"还能获得{mihoyobbs.today_get_coins}个米游币\n目前有{mihoyobbs.Have_coins}个米游币"
                log.info(f"今天已经获得{mihoyobbs.today_have_get_coins}个米游币，"
                         f"还能获得{mihoyobbs.today_get_coins}个米游币，目前有{mihoyobbs.Have_coins}个米游币")
                time.sleep(random.randint(2, 8))
        else:
            return_data += "\n" + "米游社功能未启用！"
            log.info("米游社功能未启用！")
        # 崩坏2签到 config这里少了个n，下回config v6的时候再修复吧
        if config.config["games"]["cn"]["hokai2"]["auto_checkin"]:
            log.info("正在进行崩坏2签到")
            honkai2_help = honkai2.Honkai2()
            return_data += "\n\n" + honkai2_help.sign_account()
            time.sleep(random.randint(2, 8))
        # 崩坏3签到
        if config.config["games"]["cn"]["honkai3rd"]["auto_checkin"]:
            log.info("正在进行崩坏3签到")
            honkai3rd_help = honkai3rd.Honkai3rd()
            return_data += "\n\n" + honkai3rd_help.sign_account()
        # 原神签到
        if config.config["games"]["cn"]["genshin"]["auto_checkin"]:
            log.info("正在进行原神签到")
            genshin_help = genshin.Genshin()
            return_data += "\n\n" + genshin_help.sign_account()
            time.sleep(random.randint(2, 8))
        return 0, return_data
    elif config.config["account"]["cookie"] == "CookieError":
        raise CookieError('Cookie expires')
    else:
        log.warning("Config未启用！")
        return 1, "Config未启用！"


if __name__ == "__main__":
    try:
        status_code, message = main()
    except CookieError:
        status_code = 1
        message = "账号Cookie出错！"
        log.error("账号Cookie有问题！")
    push.push(status_code, message)
pass
