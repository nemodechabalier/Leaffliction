#!/usr/bin/env python3
import random
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from collections import defaultdict
from pathlib import Path
from plantcv import plantcv as pcv   # TOUT passe par cet objet « pcv »
import cv2 
import Augment as ag

def show_all(images: dict):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    for ax, (title, im) in zip(axes.flat, images.items()):
        if im.ndim == 3:
            ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        else:
            ax.imshow(im, cmap="gray")            # masque / gris
        ax.set_title(title)
    plt.tight_layout()
    plt.show()



def main():
	args = ag.arg_parser()

	#TRansform all the folder
	if (args.src):
		print("src file required")
		
	#transform and display only the entry
	else :
		transfo = defaultdict(Image.Image)

		img, path, filename = pcv.readimage(args.image, mode='gray')
		transfo["gray"] = img
		print(f"PATH: {path}, FILENANE: {filename}")
		img2, path2, filename2 = pcv.readimage(args.image, mode='rgb')
		transfo["rgb"] = img2
		sat = pcv.rgb2gray_hsv(img2, "s")   # saturation : feuille colorée, fond gris
		blue = pcv.rgb2gray_lab(img2, "b")   # LAB b : axe bleu ↔ jaune
		s_thresh = pcv.threshold.binary(sat, 60, "light")
		b_thresh = pcv.threshold.binary(blue,135, "light")
		mask = pcv.logical_or(bin_img1=s_thresh, bin_img2=b_thresh)  # union des deux
		# mask = pcv.fill(bin_img=mask, size=200)     # supprime les taches blanches < 200 px
		# mask = pcv.fill_holes(bin_img=mask)         # bouche les trous noirs dans la feuille


		# a = pcv.visualize.colorspaces(img2)
		a = pcv.gaussian_blur(img2,(11,11),0)
		d = pcv.gaussian_blur(sat,(11,11),0)
		masked = pcv.apply_mask(img2,mask,"white")
		transfo['sat'] = sat
		transfo['blue'] = blue
		# transfo['a'] = a
		# transfo['d'] = d
		transfo['masked'] = masked
		# np.shape(transfo['a'])
		# pcv.plot_image(transfo['a'])
		# pcv.print_image(transfo['a'])
		show_all(transfo)
		print("Transform and display the transformations")
	return

if __name__ == "__main__":
	main()