# scripts/generate_zip_output.py
import os
import zipfile
from typing import List

def create_zip(file_paths: List[str], output_dir: str) -> str:
    """
    Zips up a list of files into a single CS4_submission.zip file in the output directory.

    Args:
        file_paths (List[str]): Full paths to CSVs (e.g., contextual and survey files)
        output_dir (str): Folder to save the ZIP file into

    Returns:
        str: Path to the created ZIP file
    """
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, "CS4_submission.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            arcname = os.path.basename(file)  # just the filename inside the zip
            zipf.write(file, arcname=arcname)

    return zip_path
