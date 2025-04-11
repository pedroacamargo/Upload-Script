import os
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


IMAGES_DIR = "./players"
PRIVATE_KEY = ""
CURRENCY = "solana"
OUTPUT_FILE = "upload_results.json"
MAX_THREADS = 10  # adjust based on system and network capacity
MAX_FILES = 2000

def upload_file(file_path, name):
    """Upload a file to the specified currency."""

    try:
        #irys price 119537664 -t solana -n mainnet 
        cmd = [
            "irys",
            "upload",
            file_path,
            "-n", "mainnet",
            "-t", CURRENCY,
            "-w", PRIVATE_KEY
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Failed to upload {file_path}: {result.stderr}")
            return None

        # Extract URL from result
        for line in result.stdout.splitlines():
            print("line: " + line)
            if line.startswith("Uploaded to"):
                url = line.split("Uploaded to")[-1].strip()
                return {
                    "name": name,
                    "url": url,
                }

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

results = []
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(upload_file, file["path"], file["name"]) for file in files[:MAX_FILES]]
    for future in as_completed(futures):
        results.append(future.result())


with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=4)

