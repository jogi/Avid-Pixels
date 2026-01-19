#!/usr/bin/env python3
"""
Extract EXIF data from album photos and update markdown files.
Run automatically before Hugo build to keep EXIF data in sync.
"""

import os
import re
import yaml
from PIL import Image
from PIL.ExifTags import TAGS
from fractions import Fraction


# Human-readable labels for EXIF fields
EXIF_LABELS = {
    'Make': 'Make',
    'Model': 'Camera',
    'LensModel': 'Lens',
    'LensSpecification': 'Lens Specification',
    'FNumber': 'Aperture',
    'ExposureTime': 'Exposure Time',
    'ISOSpeedRatings': 'ISO Speed',
    'FocalLength': 'Focal Length',
    'FocalLengthIn35mmFilm': 'Focal Length (35mm)',
    'Flash': 'Flash',
    'WhiteBalance': 'White Balance',
    'ExposureProgram': 'Exposure Program',
    'MeteringMode': 'Metering Mode',
    'ExposureMode': 'Exposure Mode',
    'SceneCaptureType': 'Scene Capture Type',
    'Contrast': 'Contrast',
    'Saturation': 'Saturation',
    'Sharpness': 'Sharpness',
    'DateTime': 'Date and Time (Modified)',
    'DateTimeOriginal': 'Date and Time (Original)',
    'DateTimeDigitized': 'Date and Time (Digitized)',
    'Software': 'Software',
    'ExifVersion': 'Exif Version',
    'ColorSpace': 'Color Space',
    'FileSource': 'File Source',
    'SceneType': 'Scene Type',
    'CustomRendered': 'Custom Rendered',
    'DigitalZoomRatio': 'Digital Zoom Ratio',
    'FocalPlaneResolutionUnit': 'Focal Plane Resolution Unit',
    'SensitivityType': 'Sensitivity Type',
    'RecommendedExposureIndex': 'Recommended Exposure Index',
    'LightSource': 'Light Source',
    'ResolutionUnit': 'Resolution Unit',
    'XResolution': 'X-Resolution',
    'YResolution': 'Y-Resolution',
    'Orientation': 'Orientation',
    'ExifOffset': 'Exif Offset',
    'BodySerialNumber': 'Body Serial Number',
    'LensMake': 'Lens Make',
    'CFAPattern': 'CFA Pattern',
}


def get_exif_data(image_path):
    """Extract relevant EXIF data from an image."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return None, None

        # Map EXIF tags to readable names
        exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        # Extract camera info
        camera = exif.get('Model', '').strip()
        lens = exif.get('LensModel', '').strip()

        # Extract settings
        aperture = exif.get('FNumber')
        if aperture:
            aperture = f"f/{float(aperture):.1f}"

        shutter_speed = exif.get('ExposureTime')
        if shutter_speed:
            if shutter_speed < 1:
                shutter_speed = f"1/{int(1/shutter_speed)}"
            else:
                shutter_speed = f"{shutter_speed}s"

        iso = exif.get('ISOSpeedRatings')
        if iso:
            iso = str(iso)

        focal_length = exif.get('FocalLength')
        if focal_length:
            focal_length = f"{float(focal_length):.1f}mm"

        flash = exif.get('Flash')
        flash_fired = None
        if flash is not None:
            # Flash tag bit 0 indicates if flash fired
            flash_fired = bool(flash & 1)

        # Build summary EXIF
        summary = {
            'camera': camera or None,
            'lens': lens or None,
            'aperture': aperture,
            'shutter_speed': shutter_speed,
            'iso': iso,
            'focal_length': focal_length,
            'flash_fired': flash_fired
        }

        # Build complete EXIF data for "Show All"
        # Convert all values to strings and filter out unprintable data
        all_exif = {}
        for key, value in exif.items():
            # Use human-readable label if available, otherwise use the key
            readable_key = EXIF_LABELS.get(key, key)

            # Skip binary data and IFD pointers
            if isinstance(value, bytes):
                try:
                    decoded = value.decode('utf-8', errors='ignore').strip()
                    # Skip if contains unprintable characters
                    if decoded and all(c.isprintable() or c.isspace() for c in decoded):
                        all_exif[readable_key] = decoded
                except:
                    continue
            elif isinstance(value, (str, int, float)):
                str_value = str(value)
                # Skip if contains unprintable characters
                if all(c.isprintable() or c.isspace() for c in str_value):
                    all_exif[readable_key] = str_value
            elif isinstance(value, tuple):
                # Handle tuples like FNumber, ExposureTime
                if len(value) == 2:
                    all_exif[readable_key] = f"{value[0]}/{value[1]}"
                else:
                    all_exif[readable_key] = str(value)

        return summary, all_exif
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")
        return None, None


def update_album_markdown(album_path, root_path):
    """Update an album markdown file with EXIF data."""
    print(f"Processing {album_path}...")

    with open(album_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  Skipping: Invalid frontmatter")
        return

    # Parse YAML frontmatter
    frontmatter = yaml.safe_load(parts[1])
    images = frontmatter.get('images', [])

    updated = False
    for image in images:
        # Skip if EXIF data already exists (both summary and full)
        if 'exif' in image and image['exif'] and 'exif_all' in image and image['exif_all']:
            continue

        # Get path to original image
        original_path = image.get('path_original', '')
        if not original_path:
            continue

        # Convert to filesystem path
        full_path = os.path.join(root_path, 'static', original_path.lstrip('/'))

        if not os.path.exists(full_path):
            print(f"  Warning: Image not found: {full_path}")
            continue

        # Extract EXIF
        summary_data, all_exif_data = get_exif_data(full_path)
        if summary_data:
            # Remove None values from summary
            summary_data = {k: v for k, v in summary_data.items() if v is not None}
            image['exif'] = summary_data
            # Add all EXIF data
            if all_exif_data:
                image['exif_all'] = all_exif_data
            updated = True
            print(f"  ✓ Added EXIF for {os.path.basename(original_path)}")

    if updated:
        # Write back to file
        frontmatter['images'] = images
        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)

        new_content = f"---\n{new_frontmatter}---\n{parts[2]}"

        with open(album_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✓ Updated {album_path}")
    else:
        print(f"  No updates needed")


def main():
    """Process all album markdown files."""
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(script_dir)
    albums_path = os.path.join(root_path, 'content', 'albums')

    print("Extracting EXIF data from photos...\n")

    # Process each album markdown file
    for filename in os.listdir(albums_path):
        if filename.endswith('.md') and filename != '_index.md':
            album_path = os.path.join(albums_path, filename)
            update_album_markdown(album_path, root_path)

    print("\n✓ EXIF extraction complete!")


if __name__ == '__main__':
    main()
