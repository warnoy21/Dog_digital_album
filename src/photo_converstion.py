"""
Details : This script converts images in a specified directory to PNG format, resizes them, 
and generates corresponding header files for use in an Arduino Preoject - Digital Dog Album
to display the pictures in a 2.8 inch round LDC.

DATE: June 17 2025          BY: Aaron Gumba         Initial Version
VERSION: 1.0

"""

import os
import subprocess
from PIL import Image, UnidentifiedImageError

# Config
input_dir = "photos"
output_dir = "headers"
image_size = (240, 240)

os.makedirs(output_dir, exist_ok=True)

# Supported extensions
supported_exts = [".jpg", ".jpeg", ".png", ".webp", ".avif"]

def is_supported(filename):
    return any(filename.lower().endswith(ext) for ext in supported_exts)

def convert_to_png(input_path, output_png):
    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".avif":
        # Always use ffmpeg for AVIF
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-vf", f"scale={image_size[0]}:{image_size[1]}",
            output_png
        ])
        return

    try:
        with Image.open(input_path) as img:
            img = img.convert("RGBA")
            img = img.resize(image_size)
            img.save(output_png, "PNG")
    except UnidentifiedImageError:
        print(f"⚠️  Pillow failed on {input_path}, using ffmpeg fallback...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-vf", f"scale={image_size[0]}:{image_size[1]}",
            output_png
        ])

def png_to_header(png_path, header_path, array_name):
    with open(header_path, "w") as f:
        # Generate xxd output
        result = subprocess.run(["xxd", "-i", png_path], capture_output=True, text=True)
        code = result.stdout

        # Rename default array to photoX
        code = code.replace(os.path.basename(png_path).replace('.', '_') + "_png", array_name)
        code = code.replace(os.path.basename(png_path).replace('.', '_') + "_png_len", array_name + "_len")

        f.write(code)

def main():
    files = sorted([f for f in os.listdir(input_dir) if is_supported(f)])

    for idx, filename in enumerate(files, start=1):
        input_path = os.path.join(input_dir, filename)
        output_png = os.path.join(output_dir, f"photo{idx}.png")
        header_path = os.path.join(output_dir, f"photo{idx}.h")

        print(f"[{idx}] Converting {filename} → {header_path}")
        convert_to_png(input_path, output_png)
        png_to_header(output_png, header_path, f"photo{idx}")

    print("\n✅ All done. Header files are in 'headers/'.")

if __name__ == "__main__":
    main()