import os
import re
import glob
import shutil
import random
import cv2
import rasterio
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------

study_site = "YF"  # Change for other sites
src_base = (
    Path(r"E:\planetscope_lake_ice\Data\Input\Study Sites - Manual ALPOD Data")
    / f"{study_site} 50x50 km"
)

# pattern can be "Freezeup_" or "Breakup_" (or anything else)
pattern = "Breakup_"

dst_base = (
    Path(r"E:\planetscope_lake_ice\Data\Input\Machine Learning - Planet Samples for RF")
    / study_site
)
dst_water = dst_base / "_WATER"
dst_ice = dst_base / "_ICE"

for d in [dst_water, dst_ice]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# IMAGE HELPERS
# ---------------------------------------------------------------------


def load_planet_rgb(sr_path, max_side=1200):
    """Load 4‑band analytic Planet image and build scaled RGB (for display)."""
    with rasterio.open(sr_path) as src:
        data = src.read()  # (4, h, w)
        b, g, r = data[0], data[1], data[2]
        rgb = np.stack([b, g, r], axis=-1).astype(np.float32)

    # Downscale for quick viewing
    step = max(1, rgb.shape[0] // max_side)
    rgb = rgb[::step, ::step, :]

    # Simple contrast stretch
    for i in range(3):
        bnd = rgb[..., i]
        valid = bnd[bnd > 0]
        if valid.size > 0:
            p2, p98 = np.percentile(valid, (2, 98))
            if p98 > p2:
                rgb[..., i] = np.clip((bnd - p2) / (p98 - p2), 0, 1)

    rgb8 = (rgb * 255).clip(0, 255).astype(np.uint8)
    return rgb8


def find_companion_files(sr_path):
    """Return list of analytic+udm+xml if all present."""
    base = sr_path.replace("_analytic_4b_sr.tif", "")
    udm = base + "_udm2.tif"
    xml1 = base + "_analytic_4b_xml.xml"
    xml2 = base + ".xml"
    xml = xml1 if os.path.exists(xml1) else xml2 if os.path.exists(xml2) else None

    if all(os.path.exists(p) for p in [sr_path, udm]) and xml:
        return [sr_path, udm, xml]
    else:
        return None


# ---------------------------------------------------------------------
# MAIN LABELING LOOP
# ---------------------------------------------------------------------


def main():
    # collect all analytic SR files matching the pattern
    sr_files = list(Path(src_base).rglob("*_analytic_4b_sr.tif"))
    sr_files = [
        str(f)
        for f in sr_files
        if f.is_file() and pattern in f.as_posix()
    ]

    if not sr_files:
        print(f"No {pattern} analytic_4b_sr.tif files found.")
        return

    # shuffle order for random sampling
    random.shuffle(sr_files)
    print(f"Found {len(sr_files)} candidate {pattern} scenes, randomized order.")
    print("Press I = full ice, W = full water, S = skip, Q = quit")

    cv2.namedWindow("Planet Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Planet Preview", 1200, 900)

    for idx, sr_path in enumerate(sr_files, start=1):
        fileset = find_companion_files(sr_path)
        if not fileset:
            print(f"[{idx}] Missing companion files for {os.path.basename(sr_path)} → skipped.")
            continue

        try:
            img = load_planet_rgb(sr_path)
        except Exception as e:
            print(f"[{idx}] Error reading {sr_path}: {e}")
            continue

        display = cv2.resize(img, (min(img.shape[1], 1200), min(img.shape[0], 900)))
        text = f"[{idx}/{len(sr_files)}] I=ice W=water S=skip Q=quit {os.path.basename(sr_path)}"
        cv2.rectangle(display, (0, 0), (display.shape[1], 40), (40, 40, 40), -1)
        cv2.putText(display, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.imshow("Planet Preview", display)

        key = cv2.waitKey(0) & 0xFF
        if key in [ord("q"), 27]:  # Q or ESC
            print("Quitting labeling.")
            break
        elif key == ord("s"):
            print(f"Skipped {os.path.basename(sr_path)}")
            continue
        elif key == ord("i"):
            dest = dst_ice
            label = "ICE"
        elif key == ord("w"):
            dest = dst_water
            label = "WATER"
        else:
            print("Invalid key, use I/W/S/Q")
            continue

        for f in fileset:
            shutil.copy2(f, dest)

        print(f"[{idx}] Copied → {label} ({len(fileset)} files)")

    cv2.destroyAllWindows()
    print("Classification session finished.")


if __name__ == "__main__":
    main()