"""
FE9.1 - Duplicate / Similar Image Detection
Only compares images in the current contest and digital archive folders.
Does not search the Internet.
"""
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import imagehash

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def calculate_phash(image_path):
    try:
        with Image.open(image_path) as image:
            return imagehash.phash(image.convert("RGB"))
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Cannot read image: {image_path}") from exc


def get_images(folder):
    folder = Path(folder)
    if not folder.exists():
        return
    if not folder.is_dir():
        raise NotADirectoryError(folder)

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def detect_duplicates(submitted_image, current_contest_folder,
                      archive_folder, threshold=0.90):
    """
    threshold is between 0 and 1.
    Example: 0.90 means return images with pHash similarity >= 90%.
    This is a configurable prototype threshold, not an official SRS value.
    """
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    submitted_image = Path(submitted_image).resolve()
    if not submitted_image.is_file():
        raise FileNotFoundError(submitted_image)

    submitted_hash = calculate_phash(submitted_image)
    matches = []
    scanned_count = 0

    folders = [
        ("current_contest", current_contest_folder),
        ("digital_archive", archive_folder)
    ]

    for source_name, folder in folders:
        for candidate in get_images(folder):
            if candidate.resolve() == submitted_image:
                continue

            try:
                candidate_hash = calculate_phash(candidate)
            except ValueError:
                continue

            scanned_count += 1
            distance = submitted_hash - candidate_hash
            total_bits = submitted_hash.hash.size
            similarity = 1 - distance / total_bits

            if similarity >= threshold:
                matches.append({
                    "matched_image": str(candidate.resolve()),
                    "source": source_name,
                    "similarity_score": round(similarity * 100, 2),
                    "hash_distance": int(distance)
                })

    matches.sort(key=lambda item: item["similarity_score"], reverse=True)

    return {
        "feature": "FE9.1",
        "submitted_image": str(submitted_image),
        "scanned_local_images": scanned_count,
        "threshold": threshold,
        "similar_image_found": len(matches) > 0,
        "matches": matches,
        "note": "Only local contest/archive folders were checked. No Internet search."
    }
