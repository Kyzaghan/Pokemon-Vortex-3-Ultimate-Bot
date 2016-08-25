# -*- coding: utf-8 -*-
import sys
import time
import ast

from Util.HttpWrapper import http_wrapper
from Util.Logger import logger
from Util.SettingsReader import read_authentication, read_config, read_gyms
from Util.Translation import translation
from Vortex.Battle import battle

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
sys.setrecursionlimit(1000000000)


class gym_bot:
    """Http Class"""

    def __init__(self):
        self.s = http_wrapper()
        self.a = read_authentication()
        self.c = read_config()
        self.l = logger()
        self.tr = None  # For Trainer
        self.tl = translation()
        self.bt = battle()
        self.g = read_gyms()

    def do_login(self):
        """
        Login class
        :return:
        """
        try:
            self.l.writelog(self.tl.get_language("ExpBot", "logining"))
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.a["Username"], "mypassword": self.a["Password"]}
            r = self.s.do_request(url, "post", data)
            if "dashboard" in str(r.url):
                self.l.writelog(self.tl.get_language("ExpBot", "loginSuccess"), "success")
                self.start_bot()
            else:
                self.l.writelog(self.tl.get_language("ExpBot", "loginFailed"), "error")
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(5)
            self.do_login()
            return None

    def start_bot(self):
        """
        Start ExpBot
        :return:
        """
        try:
            self.get_gym_status()
            for city_name, city_value in self.g["Gym"].items():
                for gym_name, gym_value in dict(city_value).items():
                    if not gym_value["Status"]:
                        active_pokemon, no_js_check = self.select_battle(gym_name)
                        self.start_battle(active_pokemon, no_js_check)
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(5)
            #self.do_login()
            return None

    def get_gym_status(self):
        """
        Getting current gym status
        :return:
        """
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/your_profile.php"
            r = self.s.do_request(url)
            for city_name, city_value in self.g["Gym"].items():
                for gym_name, gym_value in dict(city_value).items():
                    if gym_value["Badge"] == "Badge" or gym_value["Badge"] == "Champion":
                        if gym_name in r.text:
                            gym_value["Status"] = True
                        else:
                            gym_value["Status"] = False
                    elif(gym_value["Badge"] in r.text):
                        gym_value["Status"] = True
                    else:
                        gym_value["Status"] = False
        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None

    def select_battle(self, gym):
        """
        Select Trainer Battle
        :return:
        """
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?gymleader={0}".format(gym)
            r = self.s.do_request(url)
            self.l.writelog(self.tl.get_language("ExpBot", "battleSelected"))
            active_pokemon, nojscheck = self.get_active_pokemon(r.text)
            return str(active_pokemon), str(nojscheck)
        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None

    def get_active_pokemon(self, response):
        """
        Get active pokémon
        :param response: html response
        :return:
        """
        try:
            ph = BeautifulSoup(response, "html.parser")

            active_pokemon = ph.find('input', attrs={'name': 'active_pokemon', 'type': 'radio', 'checked': 'checked'})

            if active_pokemon is None:
                self.l.writelog(self.tl.get_language("ExpBot", "nonePokemonSelected"), "error")
            else:
                active_pokemon = active_pokemon["value"]

            self.l.writelog("Active pokemon : " + active_pokemon, "info", False)
            nojssolvea = ph.find('input', attrs={'id': 'nojs-solve-a'})
            nojssolveb = ph.find('input', attrs={'id': 'nojs-solve-b'})
            nojscheck = None
            if nojssolvea is not None and nojssolveb is not None:
                self.l.writelog("no-js-solve-a : " + nojssolvea["value"], "info", False)
                self.l.writelog("no-js-solve-b : " + nojssolveb["value"], "info", False)
                nojscheck = int(nojssolvea["value"]) + int(nojssolveb["value"])
                self.l.writelog("no-js-check : " + str(nojscheck), "info", False)
            return active_pokemon, nojscheck
        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None

    def start_battle(self, active_pokemon, no_js_check):
        """
        Start Battle
        :return:
        """
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
            if len(no_js_check) > 1:
                data = {"active_pokemon": active_pokemon, "action": "select_attack", "": "", "": "",
                        "nojs-check": no_js_check}
            else:
                data = {"active_pokemon": active_pokemon, "action": "select_attack"}

            r = self.s.do_request(url, "post", data)
            self.l.writelog(self.tl.get_language("ExpBot", "battleStarted"))
            while True:
                if "has fainted" in self.bt.enemy_status:
                    data = {"choose": "pokechu"}
                    r = self.s.do_request(url, "post", data)
                    self.l.writelog(self.tl.get_language("ExpBot", "won"), "catch")
                    if "You won the battle" not in r.text:
                        url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
                        data = {"active_pokemon": self.get_active_pokemon(r.text), "action": "select_attack"}
                        r = self.s.do_request(url, "post", data)
                        self.l.writelog(self.tl.get_language("ExpBot", "reselectPokemon"))
                elif "has fainted" in self.bt.your_status:
                    data = {"choose": "pokechu"}
                    r = self.s.do_request(url, "post", data)
                    self.l.writelog(self.tl.get_language("ExpBot", "notWon"))
                    if "you lost the battle" in r.text:
                        self.l.writelog(self.tl.get_language("ExpBot", "youLost"), "warning")
                        self.start_bot()
                        break
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
                    data = {"active_pokemon": self.get_active_pokemon(r.text), "action": "select_attack"}
                    r = self.s.do_request(url, "post", data)
                    self.l.writelog(self.tl.get_language("ExpBot", "reselectPokemon"))
                elif "you lost the battle" in r.text:
                    self.l.writelog(self.tl.get_language("ExpBot", "youLost"), "warning")
                    self.start_bot()
                    break
                else:
                    time.sleep(self.c["ExpBot"]["SleepSecondsAfterBattle"])
                    if "You won the battle" in r.text:
                        self.l.writelog(self.tl.get_language("ExpBot", "battleWon"), "success")
                        time.sleep(self.c["ExpBot"]["SleepSecondsAfterAttack"])
                        self.start_bot()
                        break
                    else:
                        # Get war status from response
                        self.bt.get_war_status(r.text)

                        # Use potions
                        if int(float(self.bt.your_hp)) <= self.c["ExpBot"]["UseWhenHPBelow"] and \
                                not "regained" in self.bt.your_status:
                            self.l.writelog(self.tl.get_language("ExpBot", "hpIsLowUsingPotion")
                                            .format(self.c["ExpBot"]["PotionToUse"]))
                            data = {"item": self.c["ExpBot"]["PotionToUse"]}
                            r = self.s.do_request(url, "post", data)

                        # Attack
                        else:
                            data = {"attack": self.c["ExpBot"]["AttackToUse"], "action": "attack"}
                            r = self.s.do_request(url, "post", data)

                # Get war status from response
                self.bt.get_war_status(r.text)
                # Print war status
                self.bt.print_war_status()

        except Exception as e:
            self.l.writelog(str(e), "critical")
            self.do_login()
            return None
