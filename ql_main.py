from main import SignInManager, CONFIG_DIR, load_push_config
import notify

def ql_push(message):
    notify.send("库街区签到", message)

if __name__ == "__main__":
    manager = SignInManager(CONFIG_DIR)
    messages = manager.run()  # messages 是一个列表
    push_settings = load_push_config()
    if push_settings and push_settings["enable"]:
        push_level = push_settings["push_level"]
        final_message = ""
        if push_level == 1:
            # 只推送总结信息（最后一条消息）
            final_message = messages[-1]
        elif push_level == 2:
            # 推送所有人的详细信息合并为一条消息
            final_message = "\n".join(messages)
        elif push_level == 3:
            # 分条推送，每条消息分别发送
            for msg in messages:
                ql_push(msg)
        else:
            # 默认合并所有消息
            final_message = "\n".join(messages)
        if final_message:
            ql_push(final_message)
    else:
        print("推送服务未启用")
