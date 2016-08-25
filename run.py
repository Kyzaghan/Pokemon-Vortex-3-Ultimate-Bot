from Bot.CatcherBot import catcher_bot
from Bot.ExpBot import pvexpbot
from Bot.GymBot import gym_bot
from Util.VersionManager import version_manager
import sys
import os
from Util.Translation import translation

sys.setrecursionlimit(1000000000)
vm = version_manager()
tr = translation()
vm.cd = os.path.dirname(os.path.realpath(__file__))
if(vm.check_version()):
    print("\n")
    UpdateQuestion = input(tr.get_language("Catcher", "doYouWantUpdate"))
    if UpdateQuestion == "Y" or UpdateQuestion == "y":
        vm.begin_update()
    print("\n")
print("\n")
BotType = input(tr.get_language("Catcher", "expbotorCatcherBot"))
print("\n")
if BotType == "E" or BotType == "e":
    hw = pvexpbot()
    hw.do_login()
elif BotType == "C" or BotType == "c":
    hw = catcher_bot()
    hw.do_login()
elif BotType == "G" or BotType == "g":
    hw = gym_bot()
    hw.do_login()



