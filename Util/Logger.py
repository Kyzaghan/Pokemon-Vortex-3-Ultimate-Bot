# -*- coding: utf-8 -*-
import logging
import time
from Util.termcolor import cprint
from Util.Translation import translation

class logger:
    def __init__(self):
        self.l = logging
        self.p = logging
        self.tl = translation()
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',level=logging.DEBUG)
        self.p.basicConfig(filename=time.strftime("%Y-%m-%d") + 'catch.log', format='%(asctime)s %(message)s',level=logging.INFO)

    def writelog(self, message, type):
        try:
            message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
            if type == "critical":
                cprint(message, 'red', attrs=['bold'])
                self.l.critical(message)
            elif type == "warning":
                cprint(message, 'cyan')
                self.l.warning(message)
            elif type == "error":
                cprint(message, 'red')
                self.l.error(message)
            else:
                self.l.info(message)
                if type == "catched" :
                    cprint(message, "green", attrs=['bold', 'dark'])
                elif(type == "green") :
                    cprint(message, "green")
                else :
                    cprint(message)
        except Exception as e:
            print(str(e))

    def writePokemon(self, PokemonName):
        try :
            with open('catchList.log','a') as f:
                f.write("[" + time.strftime("%d-%m-%Y %H:%M %S") + "] " + self.tl.getLanguage("pokemonCaught").format(PokemonName) + "\n")
                f.close()
        except Exception as e:
            self.writelog(str(e), "critical")