#!/usr/bin/env python3
import argparse
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description="Dataset Analysis")
parser.add_argument("dataset_path", help="Path to dataset")
args = parser.parse_args()
p = Path(args.dataset_path)
if not p.exists() or not p.is_dir():
	print("Wrong path")
	sys.exit(1)
directory_list = [x for x in p.iterdir() if x.is_dir()]

EXTS = {".jpg", ".jpeg", ".png"}

fruitdict = defaultdict(dict)
countImagesByDirectory = defaultdict(dict)


for directory in directory_list:
	fruit, _, disease = directory.name.partition('_')
	images = [f for f in directory.iterdir()
			if f.is_file() and f.suffix.lower() in EXTS]
	fruitdict[fruit][disease] = images
	countImagesByDirectory[directory.name] = len(images)


#figure 2, 2 graph seulement, un pie et un bar. count de chaque dossier du dataset par rapport aux autres
names = list(countImagesByDirectory)
counts = list(countImagesByDirectory.values())

if not counts:
	print("no subdirectory")
	sys.exit(1)
if sum(counts) == 0:
	print("no image in subdirectories")
	sys.exit(1)

fig2, (axbar, axpie) = plt.subplots(1,2)
print(counts)
colors = plt.cm.tab20.colors[:len(names)]
axpie.pie(counts, labels=names, autopct="%1.1f%%", colors=colors)
axbar.bar(names, counts, color=colors)
axbar.tick_params(axis="x", labelrotation=315)
plt.setp(axbar.get_xticklabels(), ha="left", rotation_mode="anchor")
plt.show()



# testdict = defaultdict(dict)
# for fruit, diseases in fruitdict.items():
# 	names = list(diseases)
# 	counts = [len(imgs) for imgs in diseases.values()]
# 	print(fruit, names, counts)
# 	testdict[fruit]=dict(zip(names,counts))

# print(testdict)




# #figure 1, un set par fruit, decoupé en noms de maladies et pas en noms de dossiers
# n = len(testdict)
# fig, axes = plt.subplots(n,2)
# for (axbar, axpie), (fruit, disease) in zip(axes, testdict.items()):
# 	names = list(disease)
# 	counts = list(disease.values())
# 	colors = plt.cm.tab20.colors[:len(names)]

# 	axpie.pie(counts, labels=names, autopct="%1.1f%%", colors=colors)
# 	axpie.set_title(fruit + " pie")

# 	axbar.bar(names, counts, color=colors)
# 	axbar.set_title(fruit + " bar")
