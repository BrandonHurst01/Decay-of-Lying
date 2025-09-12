import json
import requests
from PIL import Image
from io import BytesIO

manifest_path = "manifest_test.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

updated = False

def get_true_dimensions(img_url):
    """Check both info.json and JPEG, trust JPEG if they disagree."""
    w_info = h_info = None
    w_jpeg = h_jpeg = None

    # Try info.json
    info_url = img_url.replace("/full/full/0/default.jpg", "") + "/info.json"
    try:
        resp = requests.get(info_url, timeout=10)
        if resp.status_code == 200:
            info = resp.json()
            w_info, h_info = info.get("width"), info.get("height")
    except Exception as e:
        print(f"⚠️ Info.json failed for {img_url}: {e}")

    # Try JPEG
    try:
        resp = requests.get(img_url, timeout=10)
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content))
            w_jpeg, h_jpeg = img.size
    except Exception as e:
        print(f"❌ JPEG fetch failed for {img_url}: {e}")

    # Decide which to trust
    if w_jpeg and h_jpeg:
        if (w_info, h_info) != (w_jpeg, h_jpeg):
            print(f"⚠️ Dimension mismatch for {img_url}: info.json={w_info}x{h_info}, JPEG={w_jpeg}x{h_jpeg}. Using JPEG.")
        return w_jpeg, h_jpeg
    elif w_info and h_info:
        return int(w_info), int(h_info)
    else:
        return None, None

for seq in manifest.get("sequences", []):
    for canvas in seq.get("canvases", []):
        for img_anno in canvas.get("images", []):
            resource = img_anno.get("resource", {})
            img_url = resource.get("@id")

            if img_url and img_url.endswith(".jpg"):
                width, height = get_true_dimensions(img_url)
                if width and height:
                    # Update Canvas
                    canvas["width"] = width
                    canvas["height"] = height

                    # Remove resource dimensions
                    resource.pop("width", None)
                    resource.pop("height", None)

                    print(f"✅ {canvas.get('label','[no label]')} set to {width} x {height}")
                    updated = True
                else:
                    print(f"⚠️ Skipped {canvas.get('label','[no label]')} (no dimensions found)")

if updated:
    with open("manifest_test_updated.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✅ Updated manifest written to manifest_test_updated.json")
else:
    print("⚠️ No updates made")
