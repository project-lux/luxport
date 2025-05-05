#!/usr/bin/env python3
"""
Example script demonstrating how to use LuxPort.
"""

import os
import sys
from luxport import ManifestExporter

def main():
    """
    Export a Yale Library IIIF manifest to a ZIP file.
    """
    # URL of a IIIF manifest to export
    manifest_url = "https://collections.library.yale.edu/manifests/16867950"
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the exporter
    exporter = ManifestExporter(manifest_url)
    
    # Get the manifest ID for the output filename
    manifest_id = exporter.downloader.get_manifest_id()
    output_file = os.path.join(output_dir, f"manifest_{manifest_id}.zip")
    
    print(f"Exporting manifest: {manifest_url}")
    print(f"Output file: {output_file}")
    
    try:
        # Export the manifest to a ZIP file
        exporter.export(output_file)
        print(f"Successfully exported manifest to: {output_file}")
        
        # Alternatively, export to a directory
        # dir_path = os.path.join(output_dir, f"manifest_{manifest_id}")
        # exporter.export_to_directory(dir_path)
        # print(f"Successfully exported manifest to directory: {dir_path}")
        
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 