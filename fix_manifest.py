# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 07:23:22 2025

@author: brand
"""

import json
import requests
from PIL import Image
from io import BytesIO

manifest_path = "manifest_test.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

updated = False
for seq in manifest.get("sequences", []):
    for canvas in seq.get("canvases", []):
        for img_anno in canvas.get("images", []):
            resource = img_anno.get("resource", {})
            img_url = resource.get("@id")

            if img_url and img_url.endswith(".jpg"):
                try:
                    response = requests.get(img_url, timeout=10)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        width, height = image.size

                        # Update canvas + resource dimensions
                        canvas["width"] = width
                        canvas["height"] = height
                        resource["width"] = width
                        resource["height"] = height
                        updated = True
                except Exception as e:
                    print(f"Error fetching {img_url}: {e}")

if updated:
    with open("manifest_test_updated.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✅ Updated manifest written to manifest_test_updated.json")
else:
    print("⚠️ No updates made")
