#!/usr/bin/env python3
"""
Example of analyzing manifest data using the simplified JSON format
"""

import os
import sys
import json
import zipfile
import argparse
from typing import Dict, Any, List, Optional

from luxport import ManifestExporter, ManifestDownloader
from luxport.utils import simplify_manifest


def load_simplified_manifest(zip_path: str) -> Dict[str, Any]:
    """
    Extract and load the simplified manifest from a ZIP file
    
    Args:
        zip_path: Path to the ZIP file
        
    Returns:
        dict: The simplified manifest data
    """
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        if 'manifest_simplified.json' in zipf.namelist():
            with zipf.open('manifest_simplified.json') as f:
                return json.loads(f.read().decode('utf-8'))
    
    # If the simplified manifest is not in the ZIP, return None
    return None

def analyze_manifest(manifest_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the simplified manifest data
    
    Args:
        manifest_data: The simplified manifest data
        
    Returns:
        dict: Analysis results
    """
    image_count = len(manifest_data.get('images', []))
    
    # Extract image dimensions
    dimensions = []
    for image in manifest_data.get('images', []):
        if image.get('full_image') and image['full_image'].get('height') and image['full_image'].get('width'):
            dimensions.append({
                'label': image.get('label', 'Unknown'),
                'height': image['full_image']['height'],
                'width': image['full_image']['width'],
                'aspect_ratio': round(image['full_image']['width'] / image['full_image']['height'], 2)
            })
    
    # Extract metadata values
    metadata_values = {}
    for item in manifest_data.get('metadata', []):
        label = item.get('label', '')
        value = item.get('value', '')
        if label:
            metadata_values[label] = value
    
    # Build analysis results
    analysis = {
        'title': manifest_data.get('title', 'Unknown'),
        'id': manifest_data.get('id', ''),
        'provider': manifest_data.get('provider', {}).get('name', 'Unknown'),
        'image_count': image_count,
        'has_thumbnails': all(img.get('thumbnail') is not None for img in manifest_data.get('images', [])),
        'dimensions': dimensions,
        'metadata': metadata_values,
        'analysis': {
            'avg_height': sum(d['height'] for d in dimensions) / len(dimensions) if dimensions else 0,
            'avg_width': sum(d['width'] for d in dimensions) / len(dimensions) if dimensions else 0,
            'avg_aspect_ratio': sum(d['aspect_ratio'] for d in dimensions) / len(dimensions) if dimensions else 0,
        }
    }
    
    return analysis

def display_analysis(analysis: Dict[str, Any]) -> None:
    """
    Display the analysis results in a readable format
    
    Args:
        analysis: Analysis results
    """
    print(f"=== Manifest Analysis: {analysis['title']} ===")
    print(f"ID: {analysis['id']}")
    print(f"Provider: {analysis['provider']}")
    print(f"Image Count: {analysis['image_count']}")
    print(f"Has Thumbnails: {'Yes' if analysis['has_thumbnails'] else 'No'}")
    print()
    
    print("=== Image Dimensions ===")
    print(f"Average Height: {analysis['analysis']['avg_height']:.2f} pixels")
    print(f"Average Width: {analysis['analysis']['avg_width']:.2f} pixels")
    print(f"Average Aspect Ratio: {analysis['analysis']['avg_aspect_ratio']:.2f}")
    print()
    
    print("=== Metadata ===")
    for key, value in analysis['metadata'].items():
        print(f"{key}: {value}")

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Analyze IIIF manifest data")
    parser.add_argument(
        "input",
        help="Path to manifest ZIP file or direct manifest URL"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save analysis results to JSON file"
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Determine if the input is a ZIP file or a URL
    if os.path.isfile(args.input) and args.input.endswith('.zip'):
        # Load from ZIP file
        print(f"Loading manifest from ZIP file: {args.input}")
        manifest_data = load_simplified_manifest(args.input)
        if not manifest_data:
            print(f"Error: Could not find simplified manifest in {args.input}", file=sys.stderr)
            return 1
    else:
        # Treat as URL
        try:
            print(f"Downloading manifest from URL: {args.input}")
            downloader = ManifestDownloader(args.input)
            manifest = downloader.download_manifest()
            manifest_data = simplify_manifest(manifest)
        except Exception as e:
            print(f"Error downloading manifest: {str(e)}", file=sys.stderr)
            return 1
    
    # Analyze the manifest
    analysis = analyze_manifest(manifest_data)
    
    # Display the analysis
    display_analysis(analysis)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"\nAnalysis saved to: {args.output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 