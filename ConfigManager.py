import json
from json import JSONDecodeError


class ConfigManager:
    """Singleton class for config management """
    instance = None

    def __init__(self):
        if not ConfigManager.instance:
            ConfigManager.instance = ConfigManager.__ConfigManager()
        pass

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __ConfigManager:
        config_file_name = "config.json"
        config_fp = None

        default_config = {
            'username': '',
            'password': '',
            'tariff': 'regular',
            'from': 'Praha',
            'to': 'Pisek',
            'chrome_version': 75
        }

        def open_config(self):
            try:
                fp = open(self.config_file_name, "r+")
            except FileNotFoundError:
                fp = open(self.config_file_name, "w+")
            if not fp:
                raise IOError("Could not open config file " + self.config_file_name)
            return fp

        def get_config(self):
            if not self.config_fp:
                self.config_fp = self.open_config()
            self.config_fp.seek(0)
            try:
                return json.load(self.config_fp)
            except JSONDecodeError:
                return self.default_config

        def set_config(self, config):
            self.config_fp.seek(0)  # <--- should reset file position to the beginning.
            json.dump(config, self.config_fp, indent=4)
            self.config_fp.truncate()

        def close(self):
            if self.config_fp:
                self.config_fp.close()

