from main import sign_in
import notify
def ql_push(message,split):
    if split:
        messages=message.split("=====================================") 
        for msg in messages:
            if msg.strip():
                notify.send(msg)
    else:
        notify.send(message)

if __name__ == "__main__":
    msg,split,checkpush=sign_in()
    if checkpush:
        ql_push(msg,split)
