import json
import uuid

# Input and output manifest paths
input_file = "manifest_clean.json"
output_file = "manifest_faircopy.json"

# Load the manifest
with open(input_file, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# Function to generate a new UUID URL for @id
def new_uuid_url():
    return f"http://{str(uuid.uuid4())}"

# Process sequences -> canvases -> images
for sequence in manifest.get("sequences", []):
    for canvas in sequence.get("canvases", []):
        # Generate a UUID URL for canvas @id
        canvas["@id"] = new_uuid_url()

        # Process images/annotations
        for image in canvas.get("images", []):
            # Generate a UUID URL for annotation @id
            image["@id"] = new_uuid_url()

            # Remove @context inside annotation
            if "@context" in image:
                del image["@context"]

            # Make sure the "on" points to the canvas @id
            image["on"] = canvas["@id"]

# Write out the rewritten manifest
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f"Rewritten manifest saved to {output_file}")
