import os
import zipfile
from typing import List

def create_zip(file_paths: List[str], output_dir: str) -> str:
    print("📦 Zipping output files...")
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, "CS4_submission.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file, arcname=os.path.basename(file))

    return zip_path
