import random
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from collections import defaultdict
from pathlib import Path


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