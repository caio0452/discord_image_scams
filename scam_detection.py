import io
import json
import imagehash
from PIL import Image

class ScamDetector:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        self.max_visual_difference: int = config["max_visual_difference"]
        self.bad_hashes = [imagehash.hex_to_hash(hash_str) for hash_str in config["hashes"]]

    def is_scam(self, image_bytes: bytes) -> bool:
        with Image.open(io.BytesIO(image_bytes)) as image:
            img_hash = imagehash.phash(image)
            for bad_hash in self.bad_hashes:
                if (img_hash - bad_hash) <= self.max_visual_difference:
                    return True
        return False
