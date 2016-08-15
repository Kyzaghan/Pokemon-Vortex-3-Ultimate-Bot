from Bot.CatcherBot import http_wrapper
from Bot.ExpBot import pvexpbot
BotType = input("ExpBot or Catcher (E/C)")
if(BotType == "E") :
    hw = pvexpbot()
    hw.do_login()
else:
    hw = http_wrapper()
    hw.do_login()


