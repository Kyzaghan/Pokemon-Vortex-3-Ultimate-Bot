# -*- coding: utf-8 -*-

import requests
from Util.SettingsReader import read_authentication, read_config, config_copy
from Util.Translation import translation
from Util.Logger import logger
import os
import zipfile


class version_manager :

    def __init__(self):
        self.s = requests.session()
        self.c = read_config()
        self.a = read_authentication()
        self.tl = translation()
        self.l = logger()
        self.cd = ""

    def do_req(self, type, url, data=""):
        if (type == "post"):
            r = self.s.post(url, data, proxies=self.a["proxy"], headers={"user-agent" : self.c["UserAgent"]})
        else:
            r = self.s.get(url, proxies=self.a["proxy"], headers={"user-agent" : self.c["UserAgent"]})
        return r

    def checkVersion(self):
        version = self.getVersion()
        if version != self.c["Version"]:
            self.l.writelog(self.tl.getLanguage("Catcher", "newVersionAvaliable").format(self.c["Version"], version), "info")
            return True
        else:
            self.l.writelog(self.tl.getLanguage("Catcher", "yourVersionUpToDate").format(self.c["Version"], version), "info")
            return False

    def getVersion(self):
        r = self.do_req("get", "https://github.com/Kyzaghan/Pokemon-Vortex-3-Ultimate-Bot/releases/latest")
        tmp_url = str(r.url)
        version = tmp_url[tmp_url.rfind("/") + 1:]
        return version

    def beginUpdate(self):
        self.create_temp_directory()
        local_filename, local_file = self.download_file()
        self.extract_update_file(local_filename, local_file)
        self.retrive_config(self.cd + "\\Temp\\" + local_file)
        self.l.writelog(self.tl.getLanguage("Catcher", "updateFinished"), "info")

    def download_file(self):
        try:
            url = "https://github.com/Kyzaghan/Pokemon-Vortex-3-Ultimate-Bot/releases/download/{0}/Release.{0}.zip".format(self.getVersion())
            local_filename = url.split('/')[-1]
            local_file = local_filename
            # NOTE the stream=True parameter
            r = requests.get(url, stream=True)
            local_filename = self.cd + "\\Temp\\" + local_filename
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush() commented by recommendation from J.F.Sebastian
            return local_filename, local_file
        except Exception as e:
            self.l.writelog(str(e), "critical")
            return None

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_temp_directory(self):
        self.create_directory(self.cd + "\\Temp")

    def extract_update_file(self, local_filename, local_file):
        fh = open(local_filename, 'rb')
        z = zipfile.ZipFile(fh)
        local_file = local_file.replace(".zip", "")
        self.create_directory(self.cd + "\\Temp\\" + local_file) # Create update directory if not exists

        for name in z.namelist():
            outpath = self.cd + "\\Temp\\" + local_file
            z.extract(name, outpath)
        fh.close()

    def retrive_config(self, directory):
        directory = directory.replace(".zip", "") + "\\Config"
        for filename in os.listdir(directory):
            if("Translation" not in filename) :
                config_copy(directory + "\\" + filename, self.cd + "\\Config\\" + filename)
