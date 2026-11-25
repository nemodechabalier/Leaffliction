import random
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from collections import defaultdict
from pathlib import Path
 

def load_image(path: Path)-> Image.Image:
    EXTS = {".jpg", ".jpeg", ".png"}
    imgpath = Path(path)
    if imgpath.is_dir():
        raise IsADirectoryError(f"{imgpath}: not a file")
    if not imgpath.is_file():
        raise FileNotFoundError(f"{imgpath}: file doesnt exist")
    if imgpath.suffix.lower() not in EXTS:
        raise ValueError(f"{imgpath}: unsupported extension")
    return Image.open(imgpath)

def save_image(img: Image.Image, dst:Path) :
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.parent.exists():
        raise FileNotFoundError(f"{dst.parent}: no such directory")
    if not dst.parent.is_dir():
        raise NotADirectoryError(f"{dst}: is a file, expected a directory")
    try:
        img.save(str(dst.resolve()),quality=95)
    except OSError:
        dst.unlink(missing_ok=True)
        raise