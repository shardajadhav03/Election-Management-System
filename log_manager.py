
def update_log(message):
    import datetime
    time=str(datetime.datetime.now())
    with open("LOG_FOR_EMS.txt","a") as log:
        log.write(f"{time}: ")
        
        log.write(message)
        
        log.write("\n")
        
def log_error(message):
    import datetime
    time=str(datetime.datetime.now())
    with open("LOG_FOR_EMS.txt","a") as log:
        
        log.write(f"{time}: ")
        
        log.write("ERROR!")
        
        log.write(message)
        
        log.write("\n") 