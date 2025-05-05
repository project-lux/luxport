#!/usr/bin/env python3
"""
Tests for the LuxPort package.
"""

import os
import json
import unittest
import tempfile
import zipfile
from typing import Dict, Any

from luxport import ManifestExporter, ManifestDownloader
from luxport.utils import simplify_manifest

# Sample test manifest URL
TEST_MANIFEST_URL = "https://collections.library.yale.edu/manifests/16867950"

# Mock manifest data for testing without network
MOCK_MANIFEST = {
    "@context": ["http://iiif.io/api/presentation/3/context.json"],
    "id": "https://example.org/manifest/123",
    "type": "Manifest",
    "label": {"none": ["Test Manifest"]},
    "metadata": [
        {"label": {"en": ["Creator"]}, "value": {"none": ["Test Creator"]}},
        {"label": {"en": ["Date"]}, "value": {"none": ["2023"]}}
    ],
    "provider": [
        {"id": "https://example.org", "label": {"en": ["Test Provider"]}}
    ],
    "items": [
        {
            "type": "Canvas",
            "id": "https://example.org/canvas/1",
            "label": {"none": ["Page 1"]},
            "height": 1000,
            "width": 800,
            "items": [
                {
                    "type": "AnnotationPage",
                    "id": "https://example.org/annotations/1",
                    "items": [
                        {
                            "type": "Annotation",
                            "motivation": "painting",
                            "id": "https://example.org/annotation/1",
                            "target": "https://example.org/canvas/1",
                            "body": {
                                "type": "Image",
                                "id": "https://example.org/image/1.jpg",
                                "format": "image/jpeg",
                                "height": 1000,
                                "width": 800
                            }
                        }
                    ]
                }
            ],
            "thumbnail": [
                {
                    "type": "Image",
                    "id": "https://example.org/image/1-thumb.jpg",
                    "format": "image/jpeg",
                    "height": 100,
                    "width": 80
                }
            ]
        }
    ]
}

class TestManifestDownloader(unittest.TestCase):
    """Test the ManifestDownloader class"""
    
    def test_get_manifest_id(self):
        """Test extracting manifest ID"""
        downloader = ManifestDownloader(manifest_data=MOCK_MANIFEST)
        self.assertEqual(downloader.get_manifest_id(), "123")
    
    def test_get_images(self):
        """Test extracting images"""
        downloader = ManifestDownloader(manifest_data=MOCK_MANIFEST)
        images = downloader.get_images()
        
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0]['type'], 'full')
        self.assertEqual(images[1]['type'], 'thumbnail')

class TestSimplifyManifest(unittest.TestCase):
    """Test the simplify_manifest function"""
    
    def test_simplify(self):
        """Test simplifying a manifest"""
        simplified = simplify_manifest(MOCK_MANIFEST)
        
        self.assertEqual(simplified['title'], "Test Manifest")
        self.assertEqual(simplified['provider']['name'], "Test Provider")
        self.assertEqual(len(simplified['metadata']), 2)
        self.assertEqual(len(simplified['images']), 1)
        
        # Check image data
        image = simplified['images'][0]
        self.assertEqual(image['label'], "Page 1")
        self.assertIsNotNone(image['full_image'])
        self.assertIsNotNone(image['thumbnail'])

class TestManifestExporter(unittest.TestCase):
    """Test the ManifestExporter class"""
    
    def test_export_to_directory(self):
        """Test exporting to a directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ManifestExporter(manifest_data=MOCK_MANIFEST)
            output_dir = exporter.export_to_directory(temp_dir, show_progress=False)
            
            # Check files were created
            self.assertTrue(os.path.exists(os.path.join(output_dir, 'manifest.json')))
            self.assertTrue(os.path.exists(os.path.join(output_dir, 'manifest_simplified.json')))
            self.assertTrue(os.path.exists(os.path.join(output_dir, 'metadata.txt')))
            self.assertTrue(os.path.exists(os.path.join(output_dir, 'info.txt')))
    
    def test_export_to_zip(self):
        """Test exporting to a ZIP file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, 'test_export.zip')
            
            exporter = ManifestExporter(manifest_data=MOCK_MANIFEST)
            exporter.export(output_file, show_progress=False)
            
            # Check ZIP file was created
            self.assertTrue(os.path.exists(output_file))
            
            # Check ZIP file contents
            with zipfile.ZipFile(output_file, 'r') as zipf:
                file_list = zipf.namelist()
                self.assertIn('manifest.json', file_list)
                self.assertIn('manifest_simplified.json', file_list)
                self.assertIn('metadata.txt', file_list)
                self.assertIn('info.txt', file_list)
                
                # Check manifest content
                with zipf.open('manifest.json') as f:
                    manifest_data = json.loads(f.read().decode('utf-8'))
                    self.assertEqual(manifest_data['id'], MOCK_MANIFEST['id'])

if __name__ == '__main__':
    unittest.main() 