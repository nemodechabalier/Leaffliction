#!/usr/bin/env python3
import random
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from collections import defaultdict
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
SRCS_DIR = CURRENT_DIR.parent
if str(SRCS_DIR) not in sys.path:
    sys.path.insert(0, str(SRCS_DIR))

from utils import flip, rotate, shear, crop, distortion, contrast, blur, projective, save_image, load_image, skew

def arg_parser():
    parser = argparse.ArgumentParser(description="Augment an image or balance a dataset through image augmentation")
    parser.add_argument("image", nargs="?", help="The path to the image")
    parser.add_argument("-src", help="The dataset's directory")
    parser.add_argument("-dst", default="augmented_dataset_directory", help="The destination path that receives the new augmented dataset")
    args = parser.parse_args()

    if args.src and args.image:
        parser.error("choose one behaviour only")
    if not args.src and not args.image:
        parser.error("choose one behaviour")
    return args


def augment_image(img: Image.Image, src: Path):
    AUGMENTATIONS = ("Flip", "Rotate", "Skew", "Shear", "Crop", "Distortion", "Contrast")
    augmentations_func = {
                            "Flip": flip,
                            "Rotate": lambda i: rotate(img, random.uniform(-45, 45)),
                            "Skew": lambda i: skew(img, random.uniform(0.1, 0.3)),
                            "Shear": lambda i: shear(i, random.uniform(-0.3, 0.3)),
                            "Crop": lambda i: crop(i, random.uniform(0.7, 0.9)),
                            "Distortion": lambda i: distortion(i, random.uniform(0.02, 0.06)),
                            "Contrast": lambda i: contrast(i, random.uniform(1.5, 3)),
                            "Blur": lambda i: blur(i, random.uniform(1, 4)),
                            "Projective": lambda i: projective(i, random.uniform(0.1, 0.3)),
    }
    # for name, func in augmentations_func.items():
    #     newf = src.with_stem(f"{src.stem}_{name}")
    #     save_image2(func(img), newf)

    for name, func in augmentations_func.items():
        p = Path("augmented_directory")
        newf = src.with_stem(f"{src.stem}_{name}")
        save_image(func(img), newf)
        save_image(func(img), newf.parent / p / newf.name)
    save_image(img, newf.parent / p / src.name)
    

    return



def main():
    args = arg_parser()
    if (args.src):
        print("Under Construction")
    else:
        try:
            image = load_image(args.image)
            # show_image(image,"test")
        except Exception as error:
            print(f"Erreur loag: {error}", file=sys.stderr)
            sys.exit(1)
        try:
            fpath = Path(image.filename)
            augment_image(image, fpath)
        except (OSError, ValueError) as error:
            print(f"augment Erreur : {error}", file=sys.stderr)
            sys.exit(1)
    return

if __name__ == "__main__":
    main()