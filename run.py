from Bot.PVBot import http_wrapper
from Bot.PVExpBot import pvexpbot
BotType = input("ExpBot or Catcher (E/C)")
if(BotType == "E") :
    hw = pvexpbot()
    hw.do_login()
else:
    hw = http_wrapper()
    hw.do_login()


