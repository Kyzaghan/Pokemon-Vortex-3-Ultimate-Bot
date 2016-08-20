# -*- coding: utf-8 -*-
import os
import zipfile

from Util.HttpWrapper import http_wrapper
from Util.Logger import logger
from Util.SettingsReader import read_authentication, read_config, config_copy
from Util.Translation import translation


class version_manager:
    def __init__(self):
        self.s = http_wrapper()
        self.c = read_config()
        self.a = read_authentication()
        self.tl = translation()
        self.l = logger()
        self.cd = ""

    def check_version(self):
        """
        Check version is up-to-date
        :return: Bool
        """
        version = self.get_version()
        if version != self.c["Version"]:
            self.l.writelog(self.tl.get_language("Catcher", "newVersionAvaliable").format(self.c["Version"], version),
                            "info")
            return True
        else:
            self.l.writelog(self.tl.get_language("Catcher", "yourVersionUpToDate").format(self.c["Version"], version),
                            "info")
            return False

    def get_version(self):
        """
        Get version number
        :return: version number
        """
        r = self.s.do_request("https://github.com/Kyzaghan/Pokemon-Vortex-3-Ultimate-Bot/releases/latest")
        tmp_url = str(r.url)
        version = tmp_url[tmp_url.rfind("/") + 1:]
        return version

    def begin_update(self):
        # Create update directory
        """
        Update to current version.
        """
        self.create_temp_directory()

        # download file
        local_filename, local_file = self.download_file()

        # Extract file
        self.extract_update_file(local_filename, local_file)

        # Copy config files
        self.retrieve_config(self.cd + "\\Temp\\" + local_file)
        self.l.writelog(self.tl.get_language("Catcher", "updateFinished"), "info")

    def download_file(self):
        """
        Download new version file
        :return:  File path and name
        """
        try:
            url = "https://github.com/Kyzaghan/Pokemon-Vortex-3-Ultimate-Bot/releases/download/{0}/Release.{0}.zip" \
                .format(self.get_version())
            local_filename = url.split('/')[-1]
            local_file = local_filename
            r = self.s.download_file(url)
            local_filename = self.cd + "\\Temp\\" + local_filename
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return local_filename, local_file
        except Exception as e:
            self.l.writelog(str(e), "critical")
            return None

    @staticmethod
    def create_directory(path):
        """
        Create path method
        :param path: to create folder
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def create_temp_directory(self):
        """
        Create temp directory
        """
        self.create_directory(self.cd + "\\Temp")

    def extract_update_file(self, local_filename, local_file):
        """
        Extract zip file
        :param local_filename:  Zip file
        :param local_file: Extract directory
        """
        fh = open(local_filename, 'rb')
        z = zipfile.ZipFile(fh)
        local_file = local_file.replace(".zip", "")
        self.create_directory(self.cd + "\\Temp\\" + local_file)  # Create update directory if not exists

        for name in z.namelist():
            outpath = self.cd + "\\Temp\\" + local_file
            z.extract(name, outpath)
        fh.close()

    def retrieve_config(self, directory):
        """
        Build new configs
        :param directory: Updated directory
        """
        directory = directory.replace(".zip", "") + "\\Config"
        for filename in os.listdir(directory):
            if "Translation" not in filename:
                config_copy(directory + "\\" + filename, self.cd + "\\Config\\" + filename)
