#----------------------------------------------------------------------------------------------------
# Work done while being at the Intelligent Robotics and Vision Lab at the University of Texas, Dallas
# Please check the licenses of the respective works utilized here before using this script.
# 🖋️ Jishnu Jaykumar Padalunkal (2024) (Thanks to OpenAI ChatGPT for a bit of assistance! 😜)
#----------------------------------------------------------------------------------------------------

import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np

class IRVLUTDDoorHandleDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images, labels, and depth files.
            transform (callable, optional): Optional transform to be applied on an image sample.
        """
        self.root_dir = root_dir
        self.images_dir = os.path.join(root_dir, 'images')
        self.labels_dir = os.path.join(root_dir, 'labels')
        self.depth_dir = os.path.join(root_dir, 'depth')
        self.transform = transform
        self.image_filenames = [f for f in os.listdir(self.images_dir) if f.endswith('.png')]
        
        # Load class names from obj.names file
        obj_names_path = os.path.join(root_dir, 'obj.names')
        with open(obj_names_path, 'r') as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        # Get the image filename (without extension)
        image_filename = self.image_filenames[idx]
        base_filename = os.path.splitext(image_filename)[0]

        # Load image
        image_path = os.path.join(self.images_dir, image_filename)
        image = Image.open(image_path).convert('RGB')

        # Load depth image
        depth_path = os.path.join(self.depth_dir, f'{base_filename.replace("color", "depth")}.png')
        depth = Image.open(depth_path).convert('L')  # Assuming depth image is single-channel (grayscale)

        # Load labels
        label_path = os.path.join(self.labels_dir, f'{base_filename}.txt')
        boxes = []
        class_labels = []  # This will store both class IDs and names

        with open(label_path, 'r') as f:
            for line in f:
                label_data = line.strip().split()
                class_id = int(label_data[0])
                bbox = [float(x) for x in label_data[1:]]
                boxes.append([class_id] + bbox)  # class_id, cx, cy, w, h

                # Get the class name using class_id
                class_name = self.class_names[class_id]
                class_labels.append({'id': class_id, 'name': class_name})

        # Convert boxes to torch tensors
        boxes = torch.tensor(boxes, dtype=torch.float32)

        # Apply any transformations (for image, depth, and possibly boxes)
        if self.transform:
            transformed = self.transform(image=np.array(image), depth=np.array(depth), boxes=boxes)
            image = transformed['image']
            depth = transformed['depth']
            boxes = transformed['boxes']

        # Return the image, depth, labels, and class names
        return {
            'image': image,
            'depth': depth,
            'labels': boxes,
            'class_labels': class_labels  # Returns both class ID and name
        }
