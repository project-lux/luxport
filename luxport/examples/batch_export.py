#!/usr/bin/env python3
"""
Example of batch exporting multiple manifests
"""

import os
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import List

from luxport import ManifestExporter

# Sample list of Yale Library manifests to export
SAMPLE_MANIFESTS = [
    "https://collections.library.yale.edu/manifests/16867950",
    # Add more manifest URLs here
]

def export_manifest(manifest_url: str, output_dir: str) -> str:
    """
    Export a single manifest to a ZIP file
    
    Args:
        manifest_url: URL to the manifest
        output_dir: Directory to save the ZIP file
        
    Returns:
        str: Path to the created ZIP file
    """
    try:
        print(f"Exporting manifest: {manifest_url}")
        exporter = ManifestExporter(manifest_url)
        manifest_id = exporter.downloader.get_manifest_id()
        output_file = os.path.join(output_dir, f"manifest_{manifest_id}.zip")
        
        exporter.export(output_file)
        print(f"Successfully exported manifest to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error exporting {manifest_url}: {str(e)}", file=sys.stderr)
        return None

def batch_export(manifest_urls: List[str], output_dir: str, max_workers: int = 4) -> List[str]:
    """
    Export multiple manifests in parallel
    
    Args:
        manifest_urls: List of manifest URLs to export
        output_dir: Directory to save the ZIP files
        max_workers: Maximum number of parallel workers
        
    Returns:
        list: List of paths to the created ZIP files
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(export_manifest, url, output_dir) for url in manifest_urls]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    
    return results

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Batch export IIIF manifests")
    parser.add_argument(
        "--manifests", "-m",
        nargs="+",
        help="List of manifest URLs to export (if not specified, uses sample list)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./output",
        help="Directory to save the exported files (default: ./output)"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=4,
        help="Maximum number of parallel workers (default: 4)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Use provided manifest URLs or default to sample list
    manifest_urls = args.manifests or SAMPLE_MANIFESTS
    
    print(f"Exporting {len(manifest_urls)} manifests to {args.output_dir}")
    print(f"Using {args.workers} parallel workers")
    
    exported_files = batch_export(manifest_urls, args.output_dir, args.workers)
    
    print(f"\nExport complete. Exported {len(exported_files)} of {len(manifest_urls)} manifests.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 