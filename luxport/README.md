# LuxPort

A utility for exporting IIIF manifest data to ZIP files. LuxPort is specifically designed to work with Yale Library's digital collections.

## Features

- Downloads and exports IIIF manifest data to a ZIP file
- Downloads all images in both full size and thumbnail formats
- Saves the original JSON manifest and a simplified version
- Organizes content in a structured, accessible format
- Provides a command-line interface and a Python API
- Parallel batch processing for multiple manifests

## Installation

```bash
pip install luxport
```

Or clone the repository and install locally:

```bash
git clone https://github.com/yourusername/luxport.git
cd luxport
pip install -e .
```

## Usage

### Command Line

```bash
# Export a manifest by URL
luxport export https://collections.library.yale.edu/manifests/16867950 --output-dir ./exported

# Specify a custom output filename
luxport export https://collections.library.yale.edu/manifests/16867950 --output-file yale_collection.zip

# Show help
luxport --help
luxport export --help
```

### Python API

```python
from luxport import ManifestExporter

# Export a manifest from URL to ZIP file
exporter = ManifestExporter("https://collections.library.yale.edu/manifests/16867950")
exporter.export("yale_collection.zip")

# Or export to a directory
exporter.export_to_directory("./exported")
```

## Output Structure

```
manifest_16867950.zip
├── manifest.json            # Original JSON manifest
├── manifest_simplified.json # Simplified JSON manifest 
├── images/
│   ├── full/                # Full-size images
│   │   ├── 16868023.jpg
│   │   ├── 16868024.jpg
│   │   └── ...
│   └── thumbnails/          # Thumbnail images
│       ├── 16868023.jpg
│       ├── 16868024.jpg
│       └── ...
├── metadata.txt             # Extracted metadata in readable format
└── info.txt                 # Summary information about the export
```

## Examples

Several example scripts are included in the `examples/` directory:

### Basic Export (example.py)

Simple example of exporting a manifest to a ZIP file:

```python
from luxport import ManifestExporter

# Create the exporter with a manifest URL
exporter = ManifestExporter("https://collections.library.yale.edu/manifests/16867950")

# Export to a ZIP file
exporter.export("output/manifest.zip")
```

### Batch Export (examples/batch_export.py)

Example of batch exporting multiple manifests in parallel:

```bash
# Run the example
python examples/batch_export.py

# Export specific manifests
python examples/batch_export.py -m "https://collections.library.yale.edu/manifests/16867950" "https://collections.library.yale.edu/manifests/12345678"

# Specify output directory and parallel workers
python examples/batch_export.py -o ./batch_output -w 8
```

### Manifest Analysis (examples/analyze_manifest.py)

Example of analyzing manifest data:

```bash
# Analyze a manifest from a URL
python examples/analyze_manifest.py https://collections.library.yale.edu/manifests/16867950

# Analyze a previously exported ZIP file
python examples/analyze_manifest.py output/manifest_16867950.zip

# Save analysis results to a JSON file
python examples/analyze_manifest.py output/manifest_16867950.zip -o analysis.json
```

## Development

### Running Tests

```bash
python tests.py
```

### Creating a Distribution

```bash
python -m build
```

## License

MIT 