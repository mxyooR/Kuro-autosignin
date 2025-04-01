import schedule
import time
import random
from main import main

def sign_in_with_random_delay():
    delay = random.randint(0, 600)  
    time.sleep(delay)
    main()

# 每天7点到7点10分之间开始
schedule.every().day.at("07:00").do(sign_in_with_random_delay)

while True:
    schedule.run_pending()
    time.sleep(1)
