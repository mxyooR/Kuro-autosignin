import main

def handler(event: dict, context: dict):
    try:
        main.sign_in()
    except Exception as e:
        print(e)
    
    return 0
