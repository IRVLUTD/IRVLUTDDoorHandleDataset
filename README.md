# IRVLUTD Door Handle Dataset Loader

This Python package provides a PyTorch dataset loader for the IRVLUTD Door Handle dataset, which includes:

- Images
- Depth maps
- YOLO-style labels

This package simplifies loading and using the dataset in machine learning workflows. It is a part of the [iTeach](https://irvlutd.github.io/iTeach) project.


## Dataset Structure
TODO: links coming soon...

The dataset should follow this structure:
```
data/
├── images/ (filename.png)
├── labels/ (filename.txt)
├── depth/ (filename.png)
└── obj.names  # Contains class names (e.g., Door, Handle)
```

Each sample in the dataset has the same filename (without the extension) across the images, labels, and depth directories.

- **Images**: RGB images (e.g., `image.png`)
- **Depth**: Depth images (e.g., `depth.png`)
- **Labels**: YOLO format labels (e.g., `label.txt`)
- **obj.names**: Class names (e.g., `Door`, `Handle`)

## Installation

To install the package, follow these steps:

1. Clone the repository or download the package files.
2. Navigate to the root directory where `setup.py` is located.
3. Run the following command to install the package:

```bash
pip install .
```

Make sure you have the necessary dependencies installed:

- `torch`
- `Pillow`
- `numpy`

Alternatively, you can install the dependencies via the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

Once installed, you can use the `IRVLUTDDoorHandleDataset` class to load dataset in a PyTorch-compatible format:

```python
from IRVLUTDDoorHandleDataset import IRVLUTDDoorHandleDataset

# Path to the dataset root directory
root_dir = '/path/to/the/data'

# Initialize the dataset
dataset = IRVLUTDDoorHandleDataset(root_dir=root_dir)

# Access the first sample in the dataset
sample = dataset[0]

# Access different components of the sample
image = sample['image']
depth = sample['depth']
labels = sample['labels']  # Bounding boxes in YOLO format (cx, cy, w, h)
class_labels = sample['class_labels']  # Class ID and name for each object

print(f"Image Shape: {image.size}")
print(f"Depth Shape: {depth.size}")
print(f"Labels: {labels}")
print(f"Class Labels: {class_labels}")
```

## License

This project is licensed under the MIT License.
