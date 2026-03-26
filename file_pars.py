def parse_config(ffile: str):
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    config = {}
    
    try:
        with open(ffile, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                if "=" not in line:
                    raise ValueError(f"Line {line_num}: Invalid format. Use KEY=VALUE")
                
                parts = line.split("=", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                
                if not value:
                    raise ValueError(f"Line {line_num}: Key '{key}' has no value")
                
                config[key] = value

        for key in mandatory:
            if key not in config:
                raise ValueError(f"Missing mandatory key: {key}")

        conf = {}
        conf["WIDTH"] = int(config["WIDTH"])
        conf["HEIGHT"] = int(config["HEIGHT"])
        conf["OUTPUT_FILE"] = config["OUTPUT_FILE"]
        perfect_value = config["PERFECT"].lower()
        if perfect_value == "true":
            conf["PERFECT"] = True
        elif perfect_value == "false":
            conf["PERFECT"] = False
        else:
            raise ValueError("PERFECT must be either 'True' or 'False'")

        
        for k in ["ENTRY", "EXIT"]:
            coords = config[k].split(',')
            if len(coords) != 2:
                raise ValueError(f"{k} must be 'x,y' format")
            conf[f"{k}_X"] = int(coords[0].strip())
            conf[f"{k}_Y"] = int(coords[1].strip())
        
        if conf["ENTRY_X"] == conf["EXIT_X"] and conf["ENTRY_Y"] == conf["EXIT_Y"]:
            raise ValueError("ENTRY and EXIT cannot be the same point!")
        if conf["WIDTH"] < 5 or conf["HEIGHT"] < 5:
            raise ValueError("Maze dimensions too small (min 5x5)")
            
        if not (0 <= conf["ENTRY_X"] < conf["WIDTH"] and 0 <= conf["ENTRY_Y"] < conf["HEIGHT"]):
            raise ValueError("ENTRY coordinates are outside the maze")
            
        if not (0 <= conf["EXIT_X"] < conf["WIDTH"] and 0 <= conf["EXIT_Y"] < conf["HEIGHT"]):
            raise ValueError("EXIT coordinates are outside the maze")

        return conf

    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{ffile}' not found.")
    except ValueError as e:
        raise ValueError(f"Config Error: {e}")