import os
import json
import imagehash
from PIL import Image

class HashBuilder:
    def __init__(self, config_path: str = "config.json", scam_dir: str = "scams"):
        self.config_path = config_path
        self.scam_dir = scam_dir

    def build(self) -> None:
        with open(self.config_path, "r") as config_file:
            config = json.load(config_file)

        hashes = []
        for filename in sorted(os.listdir(self.scam_dir)):
            file_path = os.path.join(self.scam_dir, filename)
            if os.path.isdir(file_path):
                continue
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                with Image.open(file_path) as image:
                    hashes.append(str(imagehash.phash(image)))

        config["hashes"] = sorted(list(set(hashes)))

        with open(self.config_path, "w") as config_file:
            json.dump(config, config_file, indent=2)

if __name__ == "__main__":
    HashBuilder().build()
