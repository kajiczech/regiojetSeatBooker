import json


class ConfigManager:
    config_file_name = "config.json"

    default_config = {
        'username': '',
        'password': '',
        'tariff': 'regular',
        'from': 'Praha',
        'to': 'Pisek',
        'chrome_version': 75
    }

    @classmethod
    def get_config(cls):
        try:
            fp = open(cls.config_file_name, "r")
            config = json.load(fp)
            fp.close()
            return config
        except (IOError, ValueError):
            return cls.default_config

    @classmethod
    def set_config(cls, config):
        # Make sure, that all necessary keys are in the config to avoid value errors
        config = cls.merge_dicts(cls.default_config, config)
        with open(cls.config_file_name, "w+") as fp:
            json.dump(config, fp, indent=4)
            fp.close()

    @staticmethod
    def merge_dicts(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

