import os
import json
import subprocess

# === CONFIGURATION ===
IMAGES_DIR = "./players"
WALLET_PATH = "../../w.json"
CURRENCY = "solana"
OUTPUT_FILE = "upload_results.json"

def upload_file(file_path):
    """Upload a file to the specified currency."""

    try:
        #irys price 119537664 -t solana -n mainnet 
        cmd = [
            "irys",
            "price",
            "119537664",
            "-t", CURRENCY,
            "-n", "mainnet",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Failed to upload {file_path}: {result.stderr}")
            return None

        # Extract URL from result
        for line in result.stdout.splitlines():
            print(line)
            if line.startswith("Bundle URI:"):
                url = line.split("Bundle URI:")[-1].strip()
                return url

        return None

        
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return "Error"

files = []

for name in os.listdir(IMAGES_DIR):
    image_path = os.path.join(IMAGES_DIR, name, name + ".png")
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    files.append({
        "path": image_path,
        "name": name,
    })

print(f"Found {len(files)} images to upload.")

response = []

num = 0
MAX_FILES = 2

for file in files:
    if num >= MAX_FILES:
        break

    response.append({
        "name": file["name"],
        "response": upload_file(file["path"]),
    })
    num += 1


with open(OUTPUT_FILE, "w") as f:
    json.dump(response, f, indent=4)

