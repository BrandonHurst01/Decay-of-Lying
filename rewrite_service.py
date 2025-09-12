# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 08:36:08 2025

@author: brand
"""

# -*- coding: utf-8 -*-
"""
Repair IIIF manifest service blocks based on actual JPEGs in nested folders.
"""

import json
from pathlib import Path
from PIL import Image

# Path to your manifest
manifest_path = Path(r"C:\Users\brand\Desktop\DecayofLying\Decay-of-Lying\manifest_test.json")

# Path to your IIIF images root folder
iiif_root = Path(r"C:\Users\brand\Desktop\DecayofLying\Decay-of-Lying\iiif")

# Build a lookup dictionary for all JPEGs in iiif_root and subfolders
jpeg_lookup = {f.name: f for f in iiif_root.rglob("*.jpg")}

def repair_image_service(image_entry):
    """
    Repairs the 'service' block for a single image entry using actual JPEG dimensions.
    Keeps the original remote URL for IIIF zooming.
    """
    resource = image_entry.get("resource", {})
    if not resource:
        return

    # Original image URL
    image_url = resource.get("@id", "")
    if not image_url:
        return

    # Determine local JPEG path for dimension checking
    filename = Path(image_url).name
    jpeg_candidates = list(iiif_root.rglob(filename))
    if not jpeg_candidates:
        print(f"WARNING: Local JPEG not found for {filename}")
        return
    jpeg_path = jpeg_candidates[0]

    # Read actual dimensions
    with Image.open(jpeg_path) as img:
        width, height = img.size

    # Update width and height
    resource["width"] = width
    resource["height"] = height

    # Update service block using the **remote URL base**
    # For example: remove "/full/full/0/default.jpg" from image_url
    base_url = str(image_url).rsplit("/", 5)[0]

    resource["service"] = {
        "@context": "http://iiif.io/api/image/2/context.json",
        "@id": base_url,
        "profile": "http://iiif.io/api/image/2/level2.json"
    }

    image_entry["resource"] = resource
    print(f"Repaired {filename} ({width}x{height})")


# Load manifest
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Process all canvases
for canvas in manifest.get("sequences", [])[0].get("canvases", []):
    for image_entry in canvas.get("images", []):
        repair_image_service(image_entry)

# Save the updated manifest
output_path = manifest_path.parent / "manifest_repaired.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Manifest repaired and saved to {output_path}")
