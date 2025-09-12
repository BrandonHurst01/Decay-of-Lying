# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 09:16:28 2025

@author: brand
"""

import json
from pathlib import Path

# Input and output files
input_file = Path("manifest_clean.json")
output_file = Path("manifest_faircopy.json")

# Base URL for your IDs (you can change this)
base_url = "https://brandonhurst01.github.io/Decay-of-Lying"

def rewrite_manifest(manifest):
    # Rewrite sequences
    for seq in manifest.get("sequences", []):
        for canvas in seq.get("canvases", []):
            # Preserve original label for URL
            canvas_label = canvas.get("label", "canvas")
            canvas["@id"] = f"{base_url}/canvas/{canvas_label}"

            for img in canvas.get("images", []):
                # Annotation ID based on canvas label
                img["@id"] = f"{base_url}/annotation/{canvas_label}-image"

                # Remove @context inside annotation if present
                img.pop("@context", None)

                # 'on' should point to the new canvas URL
                img["on"] = canvas["@id"]

    return manifest

# Load original manifest
with input_file.open("r", encoding="utf-8") as f:
    manifest_data = json.load(f)

# Rewrite manifest
new_manifest = rewrite_manifest(manifest_data)

# Save new manifest
with output_file.open("w", encoding="utf-8") as f:
    json.dump(new_manifest, f, indent=2)

print(f"Rewritten manifest saved to {output_file}")
