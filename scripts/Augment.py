#!/usr/bin/env python3
import random
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from collections import defaultdict
from pathlib import Path

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

# def save_image(img: Image.Image, dst:Path, fname) :
# 	dst.parent.mkdir(parents=True, exist_ok=True)
# 	if not dst.exists():
# 		raise FileNotFoundError(f"{dst}: no such directory")
# 	if not dst.is_dir():
# 		raise NotADirectoryError(f"{dst}: is a file, expected a directory")
# 	try:
# 		img.save(dst.joinpath(fname),quality=95)
# 	except OSError:
# 		dst.unlink(missing_ok=True)
# 		raise

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
	
def flip(img: Image.Image)->Image.Image:
	return ImageOps.mirror(img)

def rotate(img: Image.Image, angle: float=24.12) -> Image.Image :
	# return img.rotate(angle, resample = Image.BICUBIC, expand = False, fillcolor=(255, 255, 255))
	rotated = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
	return rotated.resize(img.size, Image.Resampling.BICUBIC)


#QUAD SKEW
def qskew(img: Image.Image) ->Image.Image:
	width, height = img.size
	distortion = int(width * 0.7)
	data = (-distortion, 0, 0, height, width, height, width + height, 0)
	return img.transform(img.size, Image.Transform.QUAD, data,
							resample=Image.Resampling.BICUBIC, fillcolor=(255, 255, 255))

def perspective_coeffs(dst, src):
    """dst = où vont les 4 coins, src = coins d'origine. Ordre : HG, HD, BD, BG."""
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(m, dtype=float),
                           np.array(src, dtype=float).reshape(8))


def skew(img: Image.Image, factor: float = 0.2) -> Image.Image:
    w, h = img.size
    d = int (w * factor)
    coins = [(0, 0), (w, 0), (w, h), (0, h)]
    penche = [(d, 0), (w - d, 0), (w, h), (0, h)]
    coeffs = perspective_coeffs(penche, coins)
    return img.transform((w, h), Image.Transform.PERSPECTIVE, coeffs,
                         Image.Resampling.BICUBIC,
                         fillcolor=(255, 255, 255))

def shear(img: Image.Image, factor: float = 0.2) -> Image.Image:
	w, h = img.size
	data = (1, factor, -factor * h / 2, 0, 1, 0)
	return img.transform((w, h), Image.Transform.AFFINE, data,
						resample=Image.Resampling.BICUBIC,
						fillcolor=(255, 255, 255))

def crop(img: Image.Image, ratio: float = 0.8) -> Image.Image:
	w, h = img.size
	cw, ch = int(w * ratio), int(h * ratio)
	left, top = (w - cw) // 2, (h - ch) // 2
	return img.crop((left, top, left + cw, top + ch)).resize(
		(w, h), Image.Resampling.BICUBIC)

def distortion(img: Image.Image, amplitude: float = 0.03) -> Image.Image:
	arr = np.asarray(img)
	h, w = arr.shape[:2]
	yy, xx = np.indices((h, w))
	amp_x, amp_y = w * amplitude, h * amplitude
	src_x = xx + amp_x * np.sin(2 * np.pi * yy / (h / 2))
	src_y = yy + amp_y * np.sin(2 * np.pi * xx / (w / 2))
	src_x = src_x.clip(0, w - 1).astype(int)
	src_y = src_y.clip(0, h - 1).astype(int)
	return Image.fromarray(arr[src_y, src_x])

def contrast(img: Image.Image, factor: float = 1.5) -> Image.Image:
	return ImageEnhance.Contrast(img).enhance(factor)

def blur(img: Image.Image, radius: float = 2) -> Image.Image:
	return img.filter(ImageFilter.GaussianBlur(radius))

def projective(img: Image.Image, factor: float = 0.2) -> Image.Image:
	w, h = img.size
	dx, dy = int(w * factor), int(h * factor)
	coins = [(0, 0), (w, 0), (w, h), (0, h)]
	projete = [(dx, dy), (w, 0), (w - dx, h - dy), (0, h)]
	coeffs = perspective_coeffs(projete, coins)
	return img.transform((w, h), Image.Transform.PERSPECTIVE, coeffs,
						Image.Resampling.BICUBIC,
						fillcolor=(255, 255, 255))

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
	# 	newf = src.with_stem(f"{src.stem}_{name}")
	# 	save_image2(func(img), newf)

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