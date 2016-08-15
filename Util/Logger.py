# -*- coding: utf-8 -*-
import logging
import time
from Util.Translation import translation
from colorama import init, Fore, Back, Style

init()

class logger:
    def __init__(self):
        self.l = logging
        self.p = logging
        self.tl = translation()
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',level=logging.DEBUG)
        self.p.basicConfig(filename=time.strftime("%Y-%m-%d") + 'catch.log', format='%(asctime)s %(message)s',level=logging.INFO)

    def writelog(self, message, type):
        try:
            print(Style.RESET_ALL)
            message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
            if type == "critical":
                self.l.critical(message)
                print(Fore.RED + message)
            elif type == "warning":
                self.l.warning(message)
                print(Fore.CYAN + message)
            elif type == "error":
                self.l.error(message)
                print(Fore.RED + message)
            else:
                self.l.info(message)
                print(Fore.GREEN + message)

        except Exception as e:
            print(str(e))

    def writePokemon(self, PokemonName):
        try :
            with open('catchList.log','a') as f:
                f.write("[" + time.strftime("%d-%m-%Y %H:%M %S") + "] " + self.tl.getLanguage("Catcher", "pokemonCaught").format(PokemonName) + "\n")
                f.close()
        except Exception as e:
            self.writelog(str(e), "critical")