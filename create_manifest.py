# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 18:21:51 2025

@author: brand
"""

import os
import json

# Path to your IIIF image folders
iiif_dir = "iiif_2"

# GitHub Pages base URL
base_url = "https://brandonhurst01.github.io/Decay-of-Lying/iiif_2/"

# Prepare top-level manifest
manifest = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": base_url + "manifest.json",
    "@type": "sc:Manifest",
    "label": "Decay of Lying",
    "sequences": [
        {
            "@id": base_url + "sequence/normal",
            "@type": "sc:Sequence",
            "canvases": []
        }
    ]
}

sequence = manifest["sequences"][0]["canvases"]

def numeric_sort_key(name):
    try:
        return (0, int(name))   # numeric folders come first
    except ValueError:
        return (1, name)        # non-numeric folders come after, sorted alphabetically

for folder in sorted(os.listdir(iiif_dir), key=numeric_sort_key):
    folder_path = os.path.join(iiif_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    # Read info.json for dimensions
    info_file = os.path.join(folder_path, "info.json")
    if not os.path.exists(info_file):
        continue

    with open(info_file, 'r', encoding='utf-8') as f:
        info = json.load(f)

    canvas = {
        "@id": base_url + f"{folder}/canvas",
        "@type": "sc:Canvas",
        "label": folder,
        "height": info["height"],
        "width": info["width"],
        "images": [
            {
                "@type": "oa:Annotation",
                "motivation": "sc:painting",
                "resource": {
                    "@id": base_url + f"{folder}/full/full/0/default.jpg",
                    "@type": "dctypes:Image",
                    "format": "image/jpeg",
                    "service": {
                        "@context": "http://iiif.io/api/image/2/context.json",
                        "@id": base_url + f"{folder}",
                        "profile": "http://iiif.io/api/image/2/level2.json"
                    }
                },
                "on": base_url + f"{folder}/canvas"
            }
        ]
    }

    sequence.append(canvas)

# Write manifest to file
manifest_file = os.path.join(iiif_dir, "manifest.json")
with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest created: {manifest_file}")
