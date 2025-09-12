# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 18:39:31 2025

@author: brand
"""

import json
import sys

# Path to your existing top-level manifest
manifest_file = "manifest.json"

# Load manifest
try:
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
except FileNotFoundError:
    print(f"Error: Manifest file not found at {manifest_file}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON: {e}")
    sys.exit(1)

# Get canvases
canvases = manifest.get("sequences", [])[0].get("canvases", [])
if not canvases:
    print("Error: No canvases found in manifest.")
    sys.exit(1)

# Custom relabeling logic
new_labels = [
    "Front board", "Front Pastedown (with institutional label)", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
    "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
    "41", "42", "43", "44", "45", "46", "47", "48a", "48b", "49", "50", "51", "52", "53", "54", "Rear Pastedown"
]

# Check length match
if len(canvases) != len(new_labels):
    print(f"Warning: {len(canvases)} canvases but {len(new_labels)} labels. Extra canvases will keep original labels.")

# Apply relabeling safely
for i, canvas in enumerate(canvases):
    if "@type" not in canvas or canvas["@type"] != "sc:Canvas":
        continue  # skip non-canvas entries
    if i < len(new_labels):
        canvas["label"] = new_labels[i]
    else:
        canvas["label"] = canvas.get("label", str(i + 1))

# Save updated manifest
try:
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("Manifest labels updated successfully!")
except Exception as e:
    print(f"Error: Failed to write manifest: {e}")
    sys.exit(1)
