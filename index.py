import os
from main import SignInManager, CONFIG_DIR, load_push_config
import push

def handler(event: dict, context: dict):
    try:
        # 执行签到任务
        manager = SignInManager(CONFIG_DIR)
        messages = manager.run()
        
        # 根据 push 配置发送推送通知
        push_settings = load_push_config()
        if push_settings and push_settings["enable"]:
            push_level = push_settings["push_level"]
            final_message = ""
            if push_level == 1:
                final_message = messages[-1]
            elif push_level == 2:
                final_message = "\n".join(messages)
            elif push_level == 3:
                # 分条推送，每条分别发送
                for msg in messages:
                    push.push("库街区签到", msg)
            else:
                final_message = "\n".join(messages)
            if final_message:
                push.push("库街区签到", final_message)
        else:
            print("推送服务未启用")
    except Exception as e:
        print(f"Error during sign-in: {e}")
        return {"status": 500, "message": str(e)}
    return {"status": 200, "message": "签到任务完成"}
