# -*- coding: utf-8 -*-
import sys
import time

from Util.HttpWrapper import http_wrapper
from Util.Logger import logger
from Util.SettingsReader import read_authentication, read_config, read_map, read_legys, read_pokys
from Util.Translation import translation
from Vortex.Trainer import Trainer

sys.setrecursionlimit(1000000000)

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class catcher_bot:
    """Http Class"""

    def __init__(self):
        self.s = http_wrapper()
        self.a = read_authentication()
        self.c = read_config()
        self.m = read_map()
        self.l = logger()
        self.lp = read_legys()
        self.tr = None
        self.pk = read_pokys()
        self.tl = translation()

    def do_login(self):
        """
        Login the game
        :return:
        """
        try:
            self.l.writelog(self.tl.get_language("Catcher", "logining"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.a["Username"], "mypassword": self.a["Password"]}
            r = self.s.do_request(url, "post", data)
            if "dashboard" in str(r.url):
                self.l.writelog(self.tl.get_language("Catcher", "loginSuccess"), "success")
                self.tr = Trainer(self.s)
                self.init_settings()
                self.start_bot()
            else:
                self.l.writelog(self.tl.get_language("Catcher", "loginFailed"), "error")
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(10)
            self.do_login()
            return None

    def init_settings(self):
        """
        Change map type
        """
        if self.c["Catcher"]["DayOrNight"] == "Night":
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/tabs/options.php?maps=night&ajax"
            data = {"maps" : "night"}
        else:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/tabs/options.php?maps=day&ajax"
            data = {"maps" : "day"}
        self.s.do_request(url, "post", data)

    def start_bot(self):
        """
        Bot main class
        :rtype: object
        """
        try:
            self.tr.inventory.get_inventory()
            self.find_pokemon()
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(5)
            self.do_login()
            return None

    def find_pokemon(self):
        """
        Find pokémon class
        :rtype: object
        """
        try:
            while True:
                if self.tr.inventory.get_current_ball_count < int(
                        self.c["Catcher"]["PokeBallBuyList"][self.c["Catcher"]["PokeBall"]]) and \
                        self.c["Catcher"]["AutoBuyPokeBall"]:
                    self.l.writelog(self.tl.get_language("Catcher", "pokeballIsNotEnough"), "error")
                    self.tr.inventory.purchase_pokeball()
                self.l.writelog(self.tl.get_language("Catcher", "pokemonSearching"), "info")
                tmp_current_map = self.m["MapList"]['' + str(self.c["Catcher"]["CurrentMap"]) + '']
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/xml/toolbox.php?map=" + str(
                    tmp_current_map["map"]) + \
                      "&move=" + str(tmp_current_map["move"]) + "&main=" + str(self.c["Catcher"]["CurrentMap"])
                r = self.s.do_request(url)

                # Pokémon not found
                if ("No wild Pok" in r.text):
                    if not self.c["Catcher"]["DontPrintNoPokemonFoundText"]:
                        self.l.writelog(self.tl.get_language("Catcher", "pokemonNotFound"), "info")

                # Pokémon found
                elif "appeared" in r.text:

                    # Battle form id finding
                    form_id_start = r.text.index('name="')
                    if form_id_start > 0:
                        form_id_end = r.text.index(' action')
                        form_id_start += 6
                        form_id_end -= 1
                        form_id = r.text[form_id_start:form_id_end]

                        # Pokemon information finding
                        pokemon_start = r.text.index("Wild")
                        pokemon_end = r.text.index("appeared.") + 9
                        pokemon = r.text[pokemon_start + 5:pokemon_end - 10]
                        self.l.writelog(self.tl.get_language("Catcher", "pokemonFound").format(pokemon), "info")
                        self.filter_pokemon(form_id, pokemon, r.text)
        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None

    # Remove pokémon types in name
    @staticmethod
    def remove_pokemon_type(name):
        name = name.replace("Dark ", "")
        name = name.replace("Metallic ", "")
        name = name.replace("Mystic ", "")
        name = name.replace("Shiny ", "")
        name = name.replace("Shadow ", "")
        return name

    # Check pokémon types method
    @staticmethod
    def check_pokemon(poke_dic, pokemon):
        for poke in poke_dic:
            if poke_dic[poke]["Normal"] and poke == pokemon:
                return True
            elif poke_dic[poke]["Dark"] and "Dark " + poke == pokemon:
                return True
            elif poke_dic[poke]["Metallic"] and "Metallic " + poke == pokemon:
                return True
            elif poke_dic[poke]["Mystic"] and "Mystic " + poke == pokemon:
                return True
            elif poke_dic[poke]["Shiny"] and "Shiny " + poke == pokemon:
                return True
            elif poke_dic[poke]["Shadow"] and "Shadow " + poke == pokemon:
                return True
            else:
                return False

    # Filter pokémon method, It's check parameters
    def filter_pokemon(self, form_id, pokemon, result):
        try:
            # Remove pokémon types
            tmp_pokemon = self.remove_pokemon_type(pokemon)

            # Catch pokémons if not in Pokédex
            if self.c["Catcher"]["CatchPokemonNotInPokedex"]:
                if "pb.gif" not in result:
                    if tmp_pokemon in self.lp:
                        self.catch_pokemon(form_id, pokemon, True)
                    else:
                        self.catch_pokemon(form_id, pokemon, False)
                else:
                    self.l.writelog(self.tl.get_language("Catcher", "catchPokemonNotInPokedexInformation"), "info")
            else:
                # Check catch only legendary pokémons parameter
                if self.c["Catcher"]["CatchOnlyLegendaryPokemon"]:

                    # Check catch only legengary pokémon ignore types, if true catch all legy pokémons
                    if self.c["Catcher"]["CatchOnlyLegendaryPokemonIgnoreTypes"]:
                        if tmp_pokemon in self.lp:
                            self.catch_pokemon(form_id, pokemon, True)

                    # Check catch only legengary pokémon ignore types, if false catch only true type legy pokémons
                    else:
                        if self.check_pokemon(self.lp, pokemon):
                            self.catch_pokemon(form_id, pokemon, True)

                # Check catch only with pokémon filter parameter, if it's true only catch in poky.json pokémons
                elif self.c["Catcher"]["CatchOnlyWithPokemonFilter"]:

                    # Check Ignore Types parameter, if it's true catch all types
                    if self.c["Catcher"]["CatchOnlyWithPokemonFilterIgnoreTypes"]:
                        if tmp_pokemon in self.pk:
                            self.catch_pokemon(form_id, pokemon, False)

                        # Check Catch legy with pokémon filter, if it's true if bot found legy, catch it
                        elif tmp_pokemon in self.lp and self.c["Catcher"]["CatchLegyWithPokemonFilter"]:
                            self.catch_pokemon(form_id, pokemon, True)

                    # Check Ignore Types parameter, if it's false catch with type parameter
                    else:
                        if self.check_pokemon(self.pk, pokemon):
                            self.catch_pokemon(form_id, pokemon, False)
                        elif self.check_pokemon(self.lp, pokemon) and self.c["Catcher"]["CatchLegyWithPokemonFilter"]:
                            self.catch_pokemon(form_id, pokemon, True)
                else:
                    self.catch_pokemon(form_id, pokemon, tmp_pokemon in self.lp)
        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None

    def catch_pokemon(self, form_id, pokemon_name, is_legendary):
        """
        Catch pokémon class, it's final class
        :param form_id: require for battle
        :param pokemon_name: pokemon name information
        :param is_legendary: if it's legy poké, set true
        :return:
        """
        try:
            self.l.writelog(self.tl.get_language("Catcher", "enteringBattle"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php"
            data = {"wildpoke": "Battle", str(form_id): "Battle!"}
            r = self.s.do_request(url, "post", data)

            self.l.writelog(self.tl.get_language("Catcher", "enteredBattle"), "info")
            ph = BeautifulSoup(r.text, "html.parser")
            active_pokemon = ph.find('input', attrs={'name': 'active_pokemon', 'type': 'radio', 'checked': 'checked'})

            # If not pokémon in battle, return find pokémon
            if active_pokemon is None:
                self.l.writelog(self.tl.get_language("Catcher", "nonePokemonSelected"), "info")
                self.find_pokemon()
            else:
                active_pokemon = active_pokemon["value"]

            self.l.writelog(self.tl.get_language("Catcher", "enteringCatch"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
            data = {"bat": "1", "action": "1", "active_pokemon": str(active_pokemon), "action": "select_attack"}
            r = self.s.do_request(url, "post", data)
            ph = BeautifulSoup(r.text, "html.parser")
            o1 = ph.find("input", attrs={"name": "o1"})
            o2 = ph.find("input", attrs={"name": "o2"})
            o3 = ph.find("input", attrs={"name": "o3"})
            o4 = ph.find("input", attrs={"name": "o4"})

            if o1 is None or o2 is None or o3 is None or o4 is None:
                self.l.writelog(self.tl.get_language("Catcher", "pokemonAttackListNotFound"), "info")
                self.find_pokemon()
            else:
                o1 = o1["value"]
                o2 = o2["value"]
                o3 = o3["value"]
                o4 = o4["value"]

            while True:
                self.l.writelog(self.tl.get_language("Catcher", "catchStarted"), "info")
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                poke_ball_type = self.c["Catcher"]["PokeBall"].replace("Poke Ball", "Pokeball")

                if (is_legendary):
                    poke_ball_type = "Master Ball"

                data = {"o1": o1, "o2": o2, "o3": o3, "o4": o4, "actionattack": "1", "actionattack": "1", "bat": "1",
                        "item": poke_ball_type,
                        "action": "use_item", "active_pokemon": "1"}
                r = self.s.do_request(url, "post", data)
                self.tr.inventory.remove_current_ball(is_legendary)
                self.tr.inventory.print_current_inventory()
                if ("has been caught" in r.text):
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    self.s.do_request(url, "post", data)

                    # Sleep after battle
                    time.sleep(int(self.c["Catcher"]["SleepSecondsAfterBattle"]))
                    self.l.writelog(self.tl.get_language("Catcher", "pokemonCaught").format(pokemon_name), "catched")
                    self.l.write_pokemon(pokemon_name)
                    self.find_pokemon()
                    break
                else:
                    self.l.writelog(self.tl.get_language("Catcher", "pokemonCaughtNotSuccess").format(pokemon_name),
                                    "error")
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    r = self.s.do_request(url, "post", data)
                if self.tr.inventory.get_current_ball_count < int(self.c["Catcher"]["PokeBallBuyList"][
                                                                      self.c["Catcher"]["PokeBall"]]) and \
                        self.c["Catcher"]["AutoBuyPokeBall"]:
                    self.l.writelog(self.tl.get_language("Catcher", "pokeballIsNotEnough").format(pokemon_name), "error")
                    self.tr.inventory.purchase_pokeball()
                    break

        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None
