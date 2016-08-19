# -*- coding: utf-8 -*-
import logging
import time

from colorama import init, Fore, Style

from Util.Translation import translation

init()


class logger:
    def __init__(self):
        self.l = logging
        self.p = logging
        self.tl = translation()
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',
                           level=logging.DEBUG)
        self.p.basicConfig(filename=time.strftime("%Y-%m-%d") + 'catch.log', format='%(asctime)s %(message)s',
                           level=logging.INFO)

    def writelog(self, message, type="info", doprint=True):
        try:
            print(Style.RESET_ALL)
            message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
            if type == "critical":
                self.l.critical(message)
                if doprint:
                    print(Fore.RED + Style.BRIGHT + message)
            elif type == "warning":
                self.l.warning(message)
                if doprint:
                    print(Fore.YELLOW + message)
            elif type == "error":
                self.l.error(message)
                if doprint:
                    print(Fore.RED + message)
            elif type == "info":
                self.l.info(message)
                if doprint:
                    print(Fore.WHITE + message)
            elif type == "success":
                self.l.info(message)
                if doprint:
                    print(Fore.GREEN + message)
            elif type == "catch":
                self.l.info(message)
                if doprint:
                    print(Fore.BLUE + message)
        except Exception as e:
            print(str(e))

    def writePokemon(self, PokemonName):
        try:
            with open('catchList.log', 'a') as f:
                f.write("[" + time.strftime("%d-%m-%Y %H:%M %S") + "] " + self.tl.getLanguage("Catcher",
                                                                                              "pokemonCaught").format(
                    PokemonName) + "\n")
                f.close()
        except Exception as e:
            self.writelog(str(e), "critical")
