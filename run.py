from Bot.CatcherBot import catcher_bot
from Bot.ExpBot import pvexpbot
from Util.VersionManager import version_manager
import sys
import os
from Util.Translation import translation

sys.setrecursionlimit(1000000000)
vm = version_manager()
tr = translation()
vm.cd = os.path.dirname(os.path.realpath(__file__))
if(vm.checkVersion()):
    print("\n")
    UpdateQuestion = input(tr.getLanguage("Catcher", "doYouWantUpdate"))
    if UpdateQuestion == "Y" or UpdateQuestion == "y":
        vm.beginUpdate()
    print("\n")
print("\n")
BotType = input(tr.getLanguage("Catcher", "expbotorCatcherBot"))
print("\n")
if BotType == "E" or BotType == "e":
    hw = pvexpbot()
    hw.do_login()
else:
    hw = catcher_bot()
    hw.do_login()


