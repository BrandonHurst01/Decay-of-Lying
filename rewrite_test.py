import json

# Input and output manifest paths
input_file = "manifest_clean.json"
output_file = "manifest_faircopy.json"

# Load the manifest
with open(input_file, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# Process sequences -> canvases -> images
for sequence in manifest.get("sequences", []):
    for canvas in sequence.get("canvases", []):
        # Process images/annotations
        for image in canvas.get("images", []):
            # Remove @context inside annotation if it exists
            if "@context" in image:
                del image["@context"]

            # Ensure the "on" points to the canvas @id
            image["on"] = canvas["@id"]

# Write out the rewritten manifest
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f"Rewritten manifest saved to {output_file}")
