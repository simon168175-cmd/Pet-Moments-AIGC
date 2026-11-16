"""Create a local 1080px poster grid from one to nine pet photos."""
import argparse
from pathlib import Path

from local_template import render_local_template_poster
from style_presets import STYLE_PRESETS

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photos", nargs="+", type=Path)
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS), default="oil_painting")
    parser.add_argument("--output", type=Path, default=Path("pet-poster.jpg"))
    args = parser.parse_args()
    if len(args.photos) > 9 or not all(p.is_file() for p in args.photos):
        parser.error("Pass one to nine existing image files.")
    render_local_template_poster(args.photos, args.output, {"id": args.style}, "Pet Moments")
    print(args.output)
