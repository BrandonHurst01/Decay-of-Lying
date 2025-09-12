# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 08:20:35 2025

@author: brand
"""

import json

def remove_service(obj):
    """
    Recursively remove all "service" keys from a JSON object.
    """
    if isinstance(obj, dict):
        # Remove "service" key if present
        obj.pop("service", None)
        # Recursively process all dictionary values
        for key, value in obj.items():
            remove_service(value)
    elif isinstance(obj, list):
        # Recursively process all items in the list
        for item in obj:
            remove_service(item)

# Load your JSON manifest
with open("manifest_test_updated.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Remove "service" fields
remove_service(manifest)

# Save the cleaned JSON
with open("manifest_clean.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Service fields removed and saved to manifest_clean.json")
