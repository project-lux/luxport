#!/usr/bin/env python
"""
Example script demonstrating how to use LuxPort with Lux and Linked Art URLs
"""

import os
import argparse
from luxport import ManifestExporter, process_lux_url

def parse_args():
    parser = argparse.ArgumentParser(description="Export IIIF manifests from Lux or Linked Art URLs")
    parser.add_argument(
        "url",
        help="Lux or Linked Art URL to process (e.g., https://lux.collections.yale.edu/data/object/4ec7e7d5-c81b-453e-90a6-88a73e9a0171)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["lux", "la"],
        default="lux",
        help="API format to use (lux or la for Linked Art)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="output",
        help="Directory to save the exported files"
    )
    parser.add_argument(
        "--list-only", "-l",
        action="store_true",
        help="Only list the IIIF manifest URLs without downloading"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Processing URL: {args.url}")
    
    if args.list_only:
        # Just list the IIIF manifest URLs
        manifest_urls = process_lux_url(args.url, args.format)
        print("\nIIIF Manifest URLs found:")
        for i, url in enumerate(manifest_urls, 1):
            print(f"{i}. {url}")
    else:
        # Export all manifests
        try:
            manifest_urls = process_lux_url(args.url, args.format)
            
            if not manifest_urls:
                print("No IIIF manifests found for this URL.")
                return
            
            print(f"Found {len(manifest_urls)} IIIF manifest(s).")
            
            for i, manifest_url in enumerate(manifest_urls, 1):
                print(f"\nExporting manifest {i}/{len(manifest_urls)}: {manifest_url}")
                
                # Create an exporter for this manifest URL
                exporter = ManifestExporter(manifest_url)
                
                # Get a suitable filename from the manifest ID
                manifest_id = exporter.downloader.get_manifest_id()
                output_file = os.path.join(args.output_dir, f"manifest_{manifest_id}.zip")
                
                # Export the manifest to a ZIP file
                exporter.export(output_file)
                
                print(f"Successfully exported to: {output_file}")
        
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 