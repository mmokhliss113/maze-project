def parse_config(ffile: str):
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    config = {}
    with open(ffile) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if not line:
                continue
            splited_line = line.split("=")
            if len(splited_line) != 2:
                raise ValueError("invalid config it must be KEY=Value")
            key = splited_line[0].strip()
            value = splited_line[1].strip()
            config[key] = value
    conf = {}
    for k, v in config.items():
        if k in mandatory:
            mandatory.remove(k)
        if k == "WIDTH" or k == "HEIGHT":
            conf[k] = int(v)
        elif k == "ENTRY" or k == "EXIT":
            if ',' not in v:
                raise ValueError("ENTRY and EXIT must be in format x,y")
            x_y = v.split(',')
            if k == "ENTRY":
                conf["ENTRY_X"] = int(x_y[0])
                conf["ENTRY_Y"] = int(x_y[1])
            else:
                conf["EXIT_X"] = int(x_y[0])
                conf["EXIT_Y"] = int(x_y[1])
        elif k == "PERFECT":
            if v == "True":
                conf[k] = True
            elif v == "False":
                conf[k] = False
            else:
                raise ValueError("PERFECT must be True or False")
        elif k == "OUTPUT_FILE":
            conf[k] = v
    if mandatory:
        raise ValueError("missing mandatory keys")
    if not (0 <= conf["ENTRY_X"] < conf["WIDTH"]\
            and 0 <= conf["ENTRY_Y"] < conf["HEIGHT"]):
        raise ValueError("ENTRY is not logical")
    if not (0 <= conf["EXIT_X"] < conf["WIDTH"]\
            and 0 <= conf["EXIT_Y"] < conf["HEIGHT"]):
        raise ValueError("EXIT is not logical")
    return conf
