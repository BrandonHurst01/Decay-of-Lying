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
    Repairs the 'service' block for a single image entry using actual JPEGs.
    """
    resource = image_entry.get("resource", {})
    if not resource:
        return

    # Extract the filename from @id (assumes URL ends with filename like default.jpg)
    image_url = resource.get("@id", "")
    filename = Path(image_url).name
    jpeg_path = jpeg_lookup.get(filename)

    if not jpeg_path or not jpeg_path.exists():
        print(f"WARNING: JPEG not found for {filename}")
        return

    # Get actual image dimensions
    with Image.open(jpeg_path) as img:
        width, height = img.size

    # Update width and height in resource
    resource["width"] = width
    resource["height"] = height

    # Recreate the service block
    resource["service"] = {
        "@context": "http://iiif.io/api/image/2/context.json",
        "@id": str(jpeg_path.parent).replace("\\", "/"),  # IIIF requires forward slashes
        "profile": "http://iiif.io/api/image/2/level2.json"
    }

    # Put it back in the image entry
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
