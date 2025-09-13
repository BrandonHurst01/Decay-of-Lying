# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 09:37:48 2025

@author: brand
"""
import json
import os
from urllib.parse import quote

# Paths
input_manifest = "manifest.json"  # your current manifest file
output_manifest = "FC_manifest.json"    # the new manifest

# Base URL for generating resolvable IDs
base_canvas_url = "https://brandonhurst01.github.io/Decay-of-Lying/canvas/"
base_annotation_url = "https://brandonhurst01.github.io/Decay-of-Lying/annotation/"

# Load your existing manifest
with open(input_manifest, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Iterate over sequences -> canvases
for seq in manifest.get("sequences", []):
    for canvas in seq.get("canvases", []):
        # Generate new canvas URL
        canvas_label = quote(canvas.get("label", "canvas"))
        canvas["@id"] = base_canvas_url + canvas_label
        
        for image in canvas.get("images", []):
            # Remove '@context' from annotation
            image.pop("@context", None)
            
            # Remove 'service' block if present
            resource = image.get("resource", {})
            resource.pop("service", None)
            
            # Generate new annotation URL
            annotation_id = base_annotation_url + canvas_label
            image["@id"] = annotation_id
            
            # Fix 'on' to point to new canvas URL
            image["on"] = canvas["@id"]

# Save the new manifest
with open(output_manifest, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4, ensure_ascii=False)

print(f"Manifest rewritten and saved as '{output_manifest}'.")
