def parse_config():
    config = {}
    with open("config.txt") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            splited_line = line.split("=")
            if line.startswith("#"):
                continue
            if not line:
                continue
            if len(splited_line) != 2:
                return False
            key, value = splited_line
            config[key] = value
        return config

a = parse_config()
print(a)            
            
            
            