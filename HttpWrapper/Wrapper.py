# -*- coding: utf-8 -*-
import time

import requests

from Util.Logger import logger
from Util.SettingsReader import read_authentication, read_config, read_map, read_legys
from Vortex.Inventory import Trainer
from Util.termcolor import cprint
import re

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class http_wrapper():
    """Http Class"""

    def __init__(self):
        self.s = requests.session()
        self.a = read_authentication()
        self.c = read_config()
        self.m = read_map()
        self.l = logger()
        self.lp = read_legys()
        self.trainer = Trainer()

    @property
    def do_login(self):
        try:
            self.l.writelog("Logining. !", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.a["Username"], "mypassword": self.a["Password"]}
            r = self.s.post(url, data)

            if "dashboard" in str(r.url) :
                self.l.writelog("Login success!", "info")
            else :
                self.l.writelog("Login unsuccess!", "error")
            return True
        except Exception as e:
            self.l.writelog(str(e), "critical")

    def start_bot(self):
        try:
            self.get_inventory()
            self.find_pokemon()
        except Exception as e:
         self.l.writelog(str(e), "critical")

    def find_pokemon(self):
        try:
            while(True):
                if self.trainer.inventory.getCurrentPokeBallCount() < self.c["PokeBallBuyList"][self.c["PokeBall"]] and self.c["AutoBuyPokeBall"] == True:
                    cprint("Pokeball is not enough, is purchasing...")
                    self.purchase_pokeball()
                    break

                self.l.writelog("Pokemon searching...", "info")
                tmp_current_map = self.m["MapList"]['' + str(self.c["CurrentMap"]) + '']
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/xml/toolbox.php?map=" + str(
                    tmp_current_map["map"]) +"&move=" + str(tmp_current_map["move"]) +"&main="+str(tmp_current_map["map"])
                r = self.s.get(url)

                if("No wild Pok" in r.text) :
                    self.l.writelog("Pokémon not found, searching...", "info")
                else:
                    #Battle form id finding
                    form_id_start = r.text.index('name="')
                    form_id_end = r.text.index(' action')
                    form_id_start = form_id_start + 6
                    form_id_end = form_id_end - 1
                    form_id = r.text[form_id_start:form_id_end]

                    #Pokemon information finding
                    pokemon_start = r.text.index("Wild")
                    pokemon_end = r.text.index("appeared.") + 9
                    self.l.writelog(r.text[pokemon_start:pokemon_end], "info")
                    pokemon = r.text[pokemon_start + 5:pokemon_end - 10]
                    if self.c["CatchOnlyLegendaryPokemon"] and self.c["IgnoreLegendaryPokemonFilter"] :
                        if pokemon in self.lp :
                            self.catch_pokemon(form_id, pokemon, True)
                            break
                    elif self.c["CatchOnlyLegendaryPokemon"] and self.c["IgnoreLegendaryPokemonFilter"] != True :
                        for legy in self.lp :
                            if self.lp[legy]["Normal"] and legy == pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                            elif self.lp[legy]["Dark"] and legy == "Dark" + pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                            elif self.lp[legy]["Metallic"] and legy == "Metallic" + pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                            elif self.lp[legy]["Mystic"] and legy == "Mystic" + pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                            elif self.lp[legy]["Shiny"] and legy == "Shiny" + pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                            elif self.lp[legy]["Shadow"] and legy == "Shadow" + pokemon :
                                self.catch_pokemon(form_id, pokemon, True)
                    elif pokemon in self.lp :
                        self.catch_pokemon(form_id, pokemon, True)
                    else:
                        self.catch_pokemon(form_id, pokemon, False)

        except Exception as e:
         self.l.writelog(str(e), "critical")
         self.do_login()

    def catch_pokemon(self, FormId, PokemonName, IsLegendary):
        try:
            self.l.writelog("Entering the battle!", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php"
            data = {"wildpoke" : "Battle", str(FormId) : "Battle!"}
            r = self.s.post(url, data)

            self.l.writelog("Entered battle!", "info")
            ph = BeautifulSoup(r.text, "html.parser")
            active_pokemon = ph.find('input', attrs={'name': 'active_pokemon', 'type': 'radio', 'checked': 'checked'})

            if active_pokemon is None:
                self.l.writelog("None pokemon selected", "error")
                self.find_pokemon()
            else:
                active_pokemon = active_pokemon["value"]


            self.l.writelog("Entering catch", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
            data = {"bat": "1", "action" : "1", "active_pokemon": str(active_pokemon), "action": "select_attack"}
            r = self.s.post(url, data)
            ph = BeautifulSoup(r.text, "html.parser")
            o1 = ph.find("input", attrs={"name":"o1"})
            o2 = ph.find("input", attrs={"name":"o2"})
            o3 = ph.find("input", attrs={"name":"o3"})
            o4 = ph.find("input", attrs={"name":"o4"})

            if(o1 is None or o2 is None or o3 is None or o4 is None):
                self.l.writelog("Pokémon attack list not found", "critical")
                self.find_pokemon()
            else:
                o1 = o1["value"]
                o2 = o2["value"]
                o3 = o3["value"]
                o4 = o4["value"]

            while(True) :
                self.l.writelog("Catch started", "info")
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                pokeBallType = self.c["PokeBall"].replace("Poke Ball", "Pokeball")

                if(IsLegendary) :
                 pokeBallType = "Master Ball"

                data = {"o1" : o1, "o2" : o2, "o3" : o3, "o4" : o4, "actionattack" : "1", "actionattack" : "1", "bat" : "1", "item" : pokeBallType ,
                        "action" : "use_item", "active_pokemon" : "1" }
                r = self.s.post(url, data)
                self.trainer.inventory.removeCurrentPokeBallCount()
                self.print_current_inventory()
                if("has been caught" in r.text) :
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    r = self.s.post(url, data)
                    time.sleep(self.c["SleepSecondsAfterBattle"])
                    self.l.writelog( PokemonName  +" caught!", "catched")
                    self.find_pokemon()
                    break
                else:
                    self.l.writelog("Catch not succcess, may be you not enough pokeball", "error")
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    r = self.s.post(url, data)

                if self.trainer.inventory.getCurrentPokeBallCount() < self.c["PokeBallBuyList"][self.c["PokeBall"]]  and self.c["AutoBuyPokeBall"] == True:
                    cprint("Pokeball is not enough, is purchasing...")
                    self.purchase_pokeball()
                    break

        except Exception as e:
         self.l.writelog(str(e), "critical")
         self.find_pokemon()

    def get_inventory(self):
        try:
            self.l.writelog("Getting Inventory Information!", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/inventory.php"
            r = self.s.get(url)
            ph = BeautifulSoup(r.text, "html.parser")
            tmp_pokeball_div = ph.find_all('div', attrs={"class":"list autowidth"})
            ph = BeautifulSoup(str(tmp_pokeball_div[1]), "html.parser")
            ph = BeautifulSoup(str(ph.find_all("tr")), "html.parser")
            i = 0
            for tdList in ph.find_all("td") :
                if(i == 3) : #Pokeball
                    self.trainer.inventory.Pokeball = int(tdList.text)
                elif(i == 10) : #Great Ball
                    self.trainer.inventory.GreatBall = int(tdList.text)
                elif (i == 17):  # Ultra Ball
                    self.trainer.inventory.UltraBall = int(tdList.text)
                elif (i == 24):  # Master Ball
                    self.trainer.inventory.MasterBall = int(tdList.text)
                i+=1
            self.print_current_inventory()
        except Exception as e:
         self.l.writelog(str(e), "critical")

    def print_current_inventory(self):
        cprint("Pokéball = " + str(self.trainer.inventory.Pokeball) + "\n"
               "Great Ball = " + str(self.trainer.inventory.GreatBall) + "\n"
               "Ultra Ball = " + str(self.trainer.inventory.UltraBall) + "\n"
               "Master Ball = " + str(self.trainer.inventory.MasterBall) + "\n",
               "blue"
               )

    def purchase_pokeball(self):
        try :
            self.l.writelog("Buying pokeballs", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/items.php"
            data = {"potion":0,
                    "superpotion":0,
                    "hyperpotion":0,
                    "pokeball":self.trainer.inventory.getPokeBallBuyCount("Poke Ball"),
                    "greatball":self.trainer.inventory.getPokeBallBuyCount("Great Ball"),
                    "ultraball":self.trainer.inventory.getPokeBallBuyCount("Ultra Ball"),
                    "masterball":self.trainer.inventory.getPokeBallBuyCount("Master Ball"),
                    "fullheal":0,
                    "antidote":0,
                    "parlyzheal":0,
                    "burnheal":0,
                    "iceheal":0,
                    "awakening":0,
                    "dawnstone":0,
                    "duskstone":0,
                    "firestone":0,
                    "leafstone":0,
                    "moonstone":0,
                    "ovalstone":0,
                    "shinystone":0,
                    "sunstone":0,
                    "thunderstone":0,
                    "waterstone":0,
                    "deepseascale":0,
                    "deepseatooth":0,
                    "dragonscale":0,
                    "dubiousdisc":0,
                    "electirizer":0,
                    "magmarizer":0,
                    "kingsrock":0,
                    "metalcoat":0,
                    "prismscale":0,
                    "protector":0,
                    "razorclaw":0,
                    "razorfang":0,
                    "reapercloth":0,
                    "upgrade":0,
                    "sachet":0,
                    "whippeddream":0,
                    "icerock":0,
                    "mossrock":0,
                    "abomasite":0,
                    "absolite":0,
                    "aerodactylite":0,
                    "aggronite":0,
                    "alakazite":0,
                    "altarianite":0,
                    "ampharosite":0,
                    "audinite":0,
                    "banettite":0,
                    "beedrillite":0,
                    "blastoisinite":0,
                    "blazikenite":0,
                    "cameruptite":0,
                    "charizarditex":0,
                    "charizarditey":0,
                    "diancite":0,
                    "galladite":0,
                    "garchompite":0,
                    "gardevoirite":0,
                    "gengarite":0,
                    "glalitite":0,
                    "gyaradosite":0,
                    "heracronite":0,
                    "houndoominite":0,
                    "kangaskhanite":0,
                    "lopunnite":0,
                    "lucarionite":0,
                    "manectite":0,
                    "mawilite":0,
                    "medichamite":0,
                    "metagrossite":0,
                    "mewtwonitex":0,
                    "mewtwonitey":0,
                    "pidgeotite":0,
                    "pinsirite":0,
                    "sablenite":0,
                    "salamencite":0,
                    "sceptilite":0,
                    "scizorite":0,
                    "sharpedonite":0,
                    "slowbronite":0,
                    "steelixite":0,
                    "swampertite":0,
                    "tyranitarite":0,
                    "venusaurite":0,
                    "buy":"Buy Items"
                    }
            r = self.s.post(url, data)
            self.l.writelog("Pokéballs buyed.", "info")
            self.get_inventory()
            self.find_pokemon()
        except Exception as e:
            self.l.writelog(str(e), "critical")