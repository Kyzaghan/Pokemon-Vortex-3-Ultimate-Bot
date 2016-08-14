# -*- coding: utf-8 -*-

from Util.SettingsReader import  read_config
from Util.Logger import logger

class Inventory:
    def __init__(self):
        self.c = read_config()
        self.Pokeball = 0
        self.GreatBall = 0
        self.UltraBall = 0
        self.MasterBall = 0
        self.l = logger()

    def getCurrentPokeBallCount(self):
        if self.c["PokeBall"] == "Poke Ball":
            return self.Pokeball
        elif (self.c["PokeBall"] == "Great Ball"):
            return self.GreatBall
        elif (self.c["PokeBall"] == "Ultra Ball"):
            return self.UltraBall
        else:
            return self.MasterBall

    def removeCurrentPokeBallCount(self, IsLegend):
        if(IsLegend) :
            self.MasterBall -= 1
        else :
            if self.c["PokeBall"] == "Poke Ball":
                self.Pokeball -= 1
            elif (self.c["PokeBall"] == "Great Ball"):
                self.GreatBall -= 1
            elif (self.c["PokeBall"] == "Ultra Ball"):
                self.UltraBall -= 1
            else:
                self.MasterBall -= 1

    def getPokeBallBuyCount(self, type):
        try :
            if(type == "Poke Ball" and self.c["PokeBallBuyList"]["" + type +""] > 0) :
             PokeBallDiff = self.c["PokeBallBuyList"]["" + type +""] - self.Pokeball
            elif(type == "Great Ball" and self.c["PokeBallBuyList"]["" + type +""] > 0):
             PokeBallDiff = self.c["PokeBallBuyList"]["" + type +""] - self.GreatBall
            elif (type == "Ultra Ball" and self.c["PokeBallBuyList"]["" + type +""] > 0):
             PokeBallDiff = self.c["PokeBallBuyList"]["" + type +""] - self.UltraBall
            elif (type == "Master Ball" and self.c["PokeBallBuyList"]["" + type +""] > 0):
             PokeBallDiff = self.c["PokeBallBuyList"]["" + type +""] - self.MasterBall
            else:
             PokeBallDiff = 0

            if(PokeBallDiff <= 0) :
                return 0
            else:
                return 100
            #elif PokeBallDiff >= 100 or PokeBallDiff > 50:
                #   return 100
                #elif PokeBallDiff > 25 and PokeBallDiff <= 50 :
                #    return 50 * 2
                #elif PokeBallDiff > 10 and PokeBallDiff <= 25:
                #    return 25 * 2
                #elif PokeBallDiff > 5 and PokeBallDiff <= 10:
                #    return 10 * 2
                #else:
                #    return 5 * 2
        except Exception as e:
            self.l.writelog(str(e), "critical")

class Trainer:
    def __init__(self):
        self.inventory = Inventory()


