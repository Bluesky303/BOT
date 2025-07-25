import yaml

config = yaml.safe_load(open("./config.yaml", "r", encoding="utf-8"))
HTTP_PORT = config["HTTP_PORT"]