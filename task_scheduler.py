import schedule
import time
from main import sign_in

# Schedule sign_in function to run every day at 07:00
schedule.every().day.at("07:00").do(sign_in)

while True:
    schedule.run_pending()
    time.sleep(1)
