#!/usr/bin/env python3
"""Create browser-friendly copies and posters without modifying source videos."""

import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Frame the paper-cup robot similarly to the whiteboard demo, keeping hands and cups visible.
CROP_FILTERS = {
    "Humanoid_Paper_Cups_2x": "crop=iw*0.75:ih*0.75:iw*0.125:ih*0.1875",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "video")
    parser.add_argument("--force", action="store_true", help="Regenerate existing videos and posters.")
    args = parser.parse_args()
    videos = ROOT / "static/videos/scdp"
    posters = ROOT / "static/images/scdp"
    videos.mkdir(parents=True, exist_ok=True)
    posters.mkdir(parents=True, exist_ok=True)
    sources = sorted(
        p for p in args.source.iterdir()
        if p.is_file() and p.suffix.lower() in {".mp4", ".mov"}
    )
    if not sources:
        parser.error(f"No MP4 or MOV videos found in {args.source}")
    if len({p.stem for p in sources}) != len(sources):
        parser.error("Source videos must have unique names, excluding extensions.")
    for source in sources:
        target = videos / f"{source.stem}.mp4"
        poster = posters / f"{source.stem}.jpg"
        encode_video = args.force or not target.exists() or target.stat().st_mtime < source.stat().st_mtime
        encode_poster = args.force or not poster.exists() or poster.stat().st_mtime < source.stat().st_mtime
        crop = CROP_FILTERS.get(source.stem)
        crop_prefix = f"{crop}," if crop else ""
        filters = ""
        color_options = []
        if encode_video or encode_poster:
            info = json.loads(subprocess.check_output([
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=color_transfer", "-of", "json", str(source),
            ]))
            transfer = info["streams"][0].get("color_transfer")
            if transfer in {"arib-std-b67", "smpte2084"}:
                # Convert HDR phone recordings to SDR for consistent browser colors.
                filters = (
                    ",zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709"
                    ",tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
                    ",format=yuv420p"
                )
                color_options = [
                    "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-colorspace", "bt709", "-color_range", "tv",
                ]
        if encode_video:
            # Write atomically, so interrupted encoding never leaves a broken MP4.
            temporary = target.with_suffix(".partial.mp4")
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(source), "-an", "-vf", crop_prefix + "scale=1280:-2" + filters,
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-threads", "2", *color_options, str(temporary),
            ], check=True)
            temporary.replace(target)
        if encode_poster:
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", "1", "-i", str(source), "-frames:v", "1",
                "-vf", crop_prefix + "scale=960:-2" + filters, "-q:v", "3", str(poster),
            ], check=True)
        print(f"Ready: {source.name} ({target.stat().st_size / 1024**2:.1f} MB)", flush=True)


if __name__ == "__main__":
    main()
