import argparse
import random
import shutil
import sys
from pathlib import Path

# permet d'importer le package utils/ (qui est dans srcs/)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import augment  # noqa: E402
from utils.loader import load_image, save_image  # noqa: E402

EXTS = {".jpg", ".jpeg", ".png"}

# nom utilise dans le fichier de sortie -> fonction
TRANSFORMS = {
    "Flip": augment.flip,
    "Rotate": augment.rotate,
    "Skew": augment.skew,
    "Shear": augment.shear,
    "Crop": augment.crop,
    "Distortion": augment.distortion,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Split train/validation puis augmente le train.")
    p.add_argument("source", help="dossier contenant un dossier par classe")
    p.add_argument("-o", "--output", default="augmented_directory",
                   help="dossier de sortie (defaut: augmented_directory)")
    p.add_argument("-r", "--val-ratio", type=float, default=0.2,
                   help="part de validation par classe (defaut: 0.2)")
    p.add_argument("-s", "--seed", type=int, default=42,
                   help="graine aleatoire (defaut: 42)")
    return p.parse_args()


def list_images(class_dir: Path) -> list[Path]:
    return sorted(f for f in class_dir.iterdir()
                  if f.is_file() and f.suffix.lower() in EXTS)


def copy_files(files: list[Path], dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(f, dst_dir / f.name)


def augment_class(files: list[Path], dst_dir: Path, missing: int) -> int:
    """Genere `missing` images augmentees a partir de `files`.
    On passe transformation par transformation sur toutes les images,
    pour repartir les copies de facon homogene."""
    created = 0
    for name, func in TRANSFORMS.items():
        for f in files:
            if created >= missing:
                return created
            img = load_image(f).convert("RGB")
            new_name = f"{f.stem}_{name}{f.suffix}"
            save_image(func(img), dst_dir / new_name)
            created += 1
    return created


def main() -> None:
    args = parse_args()
    src, out = Path(args.source), Path(args.output)

    if not src.is_dir():
        sys.exit(f"{src}: not a directory")
    if out.exists():
        sys.exit(f"{out}: already exists, remove it or choose another -o")

    rng = random.Random(args.seed)
    classes = sorted(d for d in src.iterdir() if d.is_dir())
    if not classes:
        sys.exit(f"{src}: no class directory found")

    # 1. split train / validation, classe par classe
    train_files: dict[str, list[Path]] = {}
    n_val_total = 0
    for cls in classes:
        files = list_images(cls)
        rng.shuffle(files)
        n_val = max(1, round(len(files) * args.val_ratio))
        val, train = files[:n_val], files[n_val:]
        copy_files(val, out / "validation" / cls.name)
        copy_files(train, out / "train" / cls.name)
        train_files[cls.name] = train
        n_val_total += len(val)
        print(f"{cls.name}: {len(train)} train / {len(val)} validation")

    if n_val_total < 100:
        print(f"Attention: seulement {n_val_total} images en validation "
              "(le sujet en demande au moins 100)")

    # 2. equilibrage du train, par plante (prefixe avant le premier "_")
    plants: dict[str, list[str]] = {}
    for name in train_files:
        plants.setdefault(name.split("_")[0], []).append(name)

    for plant, names in plants.items():
        target = max(len(train_files[n]) for n in names)
        for name in names:
            missing = target - len(train_files[name])
            if missing <= 0:
                continue
            made = augment_class(train_files[name],
                                 out / "train" / name, missing)
            if made < missing:
                print(f"Attention: {name}: {made}/{missing} images "
                      "generees (pas assez d'images d'origine)")
            print(f"{name}: +{made} images augmentees (cible {target})")


if __name__ == "__main__":
    main()
