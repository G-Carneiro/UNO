with open("../utils/settings.py", "r") as sett:
    with open("../model/GameMode.py", "a") as mode:
        lines = sett.readlines()
        index = -1
        for line in lines:
            split = line.replace(": bool ", "").split("=")
            mode.write(f"    @property\n"
                       f"    def {split[0].lower()}(self) -> bool:\n"
                       f"        return bool(int(self.mode[{index}]))\n"
                       f"\n")
            index -= 1
