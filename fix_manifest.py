import json
import requests

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
                # Build info.json URL
                info_url = img_url.replace("/full/full/0/default.jpg", "") + "/info.json"
                width = height = None

                try:
                    resp = requests.get(info_url, timeout=10)
                    if resp.status_code == 200:
                        info = resp.json()
                        width = info.get("width")
                        height = info.get("height")
                        print(f"✅ {canvas['label']} → {width} x {height}")
                except Exception as e:
                    print(f"⚠️ Could not fetch info.json for {img_url}: {e}")

                if width and height:
                    # Update Canvas only
                    canvas["width"] = width
                    canvas["height"] = height

                    # Remove width/height from resource if they exist
                    resource.pop("width", None)
                    resource.pop("height", None)

                    updated = True

if updated:
    with open("manifest_test_updated.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✅ Updated manifest written to manifest_test_updated.json")
else:
    print("⚠️ No updates made")
