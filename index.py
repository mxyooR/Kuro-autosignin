import main

def handler(event: dict, context: dict):
    try:
        main.mian()
    except Exception as e:
        print(e)
    
    return 0
