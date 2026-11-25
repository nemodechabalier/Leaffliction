#!/usr/bin/env python3
# import Distribution as db
import Augment as ag
import matplotlib.pyplot as plt
import sys
import random
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path

def show_image(img, title=""):
    plt.imshow(img)        # accepte directement une image PIL
    plt.title(title)
    plt.axis("off")
    plt.show()

def rand_between(low: float, high: float) -> float:
    return random.uniform(low, high)      # décimal, low <= x <= high

def main():
    args = ag.arg_parser()


    if (args.src):
        print("src file required")
    else:
        try:
            image = ag.load_image(args.image)
            # show_image(image,"test")
        except Exception as error:
            print(f"Erreur loag: {error}", file=sys.stderr)
            sys.exit(1)

        # #QSKEW
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.qskew(image), pdst, fpath.stem + "_qskew" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"QSKEW Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)


        # #SKEW
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.skew(image,rand_between(0.2, 0.4)), pdst, fpath.stem + "_skew" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"SKEW Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #ROTATE
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.rotate(image,rand_between(10, 80)), pdst, fpath.stem + "_rotate" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"ROTATE Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #FLIP
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.flip(image), pdst, fpath.stem + "_flip" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"FLIP Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #SHEAR
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.shear(image,rand_between(0.1, 0.6)), pdst, fpath.stem + "_shear" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)
        
        # #CROP
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.crop(image), pdst, fpath.stem + "_crop" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #DISTORTION
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.distortion(image,rand_between(0.03, 0.1)), pdst, fpath.stem + "_distortion" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #CONTRAST
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.contrast(image,rand_between(1.5, 3)), pdst, fpath.stem + "_contrast" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #BLUR
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.blur(image,rand_between(1, 4)), pdst, fpath.stem + "_blur" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"BLUR Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        # #PROJECTIVE
        # try:
        #     pdst = Path("test")
        #     fpath = Path(image.filename)
        #     ag.save_image(ag.projective(image,rand_between(0.1, 0.3)), pdst, fpath.stem + "_projective" + fpath.suffix)
        # except (OSError, ValueError) as error:
        #     print(f"PROJECTIVE Erreur : {error}", file=sys.stderr)
        #     sys.exit(1)

        try:
            pdst = Path("test")
            fpath = Path(image.filename)
            ag.augment_image(image, fpath)
        except (OSError, ValueError) as error:
            print(f"augment Erreur : {error}", file=sys.stderr)
            sys.exit(1)
    return

if __name__ == "__main__":
    main()