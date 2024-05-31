
import time
import datetime
import json
import schedule
from bbs import getbbsforum, getpostdetail, likeposts,shareposts,getTotalGold,mingchaosignin,bbssignin
from serverjiang import sc_send


def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")

    # 从JSON文件中读取数据
    with open('data.json', 'r') as f:
        data = json.load(f)

    # 从数据中获取用户数据列表
    users = data['users']




    for user in users:
        wechattext=""
        name= user['name']
        roleId = user['roleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode= user['devCode']

        

        data = {
            "gameId": "3",
            "serverId": "76402e5b20be2c39f095a152090afddc",
            "roleId": roleId,
            "userId": userId
        }

        
        
        #鸣潮签到
        

        print(now.strftime("%Y-%m-%d"))
        wechattext=wechattext+now.strftime("%Y-%m-%d")+" "+name+"签到\n\n"
        print(name)
        print("=====================================")
        response0=mingchaosignin(tokenraw,roleId,userId,month)
        if response0:

            print("今天的奖励为：" + response0)
            wechattext=wechattext+"今天的奖励为："+response0+"\n\n"
        else:
            print("签到失败或没有奖励")
            
        
        print("=====================================")
        time.sleep(1)



        #库街区签到

        response1 = bbssignin(tokenraw)
        wechattext=wechattext+str(response1)+"\n\n"
        print(response1)
        print("=====================================")
        time.sleep(1)
        print("签到完毕，开始点赞帖子")
        wechattext=wechattext+"签到完毕，开始点赞帖子\n\n"

        idlist=getbbsforum(tokenraw,devcode)
        post_user_pairs = [(post["postId"], post["userId"]) for post in idlist["data"]["postList"]]
        i=0
        for postid, userid in post_user_pairs:
            getpostdetail(tokenraw,devcode,postid)
            time.sleep(5)
            print("第"+str((i+1))+"个帖子"+likeposts(tokenraw,devcode,postid,userid))
            wechattext=wechattext+"第"+str((i+1))+"个帖子"+str(likeposts(tokenraw,devcode,postid,userid))+"\n\n"
            time.sleep(3)
            i+=1
            if i>4:
                break
        print("=====================================")

        #转发帖子
        print("点赞完毕，开始转发帖子")
        wechattext=wechattext+"点赞完毕，开始转发帖子\n\n"
        print(shareposts(tokenraw,devcode))
        wechattext=wechattext+shareposts(tokenraw,devcode)+"\n\n"
        print("=====================================")


        #获取金币数量
        gold=getTotalGold(tokenraw,devcode)
        goldnum=gold["data"]["goldNum"]
        print("现在剩余："+str(goldnum)+"金币")
        wechattext=wechattext+"现在剩余："+str(goldnum)+"金币\n\n"
        print(name+"签到完毕")

        # 发送微信通知
        print(sc_send(name+"签到",wechattext,key='SCT169198T4eUrinSpuBs9IxuuHRTz5BMY'))
    
        
        


# Schedule the sign_in function to run at 8 AM every day
schedule.every().day.at("08:00").do(sign_in)

while True:
    #schedule.run_pending()
    schedule.run_pending()
    time.sleep(1)
