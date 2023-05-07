import yaml


def load_config():
    with open("config.yaml") as file:
        config = yaml.safe_load(file)
    return config
