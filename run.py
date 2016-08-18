from Bot.CatcherBot import http_wrapper
from Bot.ExpBot import pvexpbot
from Util.VersionManager import version_manager
import sys
sys.setrecursionlimit(1000000000)
vm = version_manager()
vm.checkVersion()
print("\n")
BotType = input("ExpBot or Catcher (E/C)")
print("\n")
if(BotType == "E") :
    hw = pvexpbot()
    hw.do_login()
else:
    hw = http_wrapper()
    hw.do_login()


