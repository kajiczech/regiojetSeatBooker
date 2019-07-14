import json


class ConfigManager:

    def __init__(self):
        pass

    instance = None
    config_file_name = "config.json"

    default_config = {
        'username': '',
        'password': '',
        'tariff': 'regular',
        'from': 'prague',
        'to': 'pisek',
        'chrome_version': 75
    }

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    @classmethod
    def open_config(cls):
        fp = open(cls.config_file_name, "r+")
        if not fp:
            raise IOError("Could not open config file " + cls.config_file_name)
        return fp

    config_fp = None

    @classmethod
    def get_config(cls):
        return cls.get_instance().__get_config()

    def __get_config(self):
        if not self.config_fp:
            self.config_fp = self.open_config()
        self.config_fp.seek(0)
        return json.load(self.config_fp) or self.default_config

    @classmethod
    def set_config(cls, config):
        return cls.get_instance().__set_config(config)

    def __set_config(self, config):
        self.config_fp.seek(0)  # <--- should reset file position to the beginning.
        json.dump(config, self.config_fp, indent=4)
        self.config_fp.truncate()

    @classmethod
    def close(cls):
        cls.get_instance().__close()
        if cls.get_instance().config_fp:
            cls.get_instance().config_fp.close()

    def __close(self):
        if self.config_fp:
            self.config_fp.close()

