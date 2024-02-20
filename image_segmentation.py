from pycocotools.coco import COCO
import os
import numpy as np
from PIL import Image, ImageDraw

annotations_file = "Annotations_Path"

image_dir = "Images_directory_path"

mask_dir = os.path.join(image_dir, "masked")

coco = COCO(annotations_file)

image_ids = coco.getImgIds()

for img_id in image_ids:
    img_info = coco.loadImgs(img_id)[0]
    img_filename = img_info['file_name']
    img_name, img_ext = os.path.splitext(img_filename)
    
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    
    mask = Image.new('L', (img_info['width'], img_info['height']), 0)
    draw = ImageDraw.Draw(mask)
    
    for ann in anns:
        segmentation = ann['segmentation']
        for seg in segmentation:
            seg = [(seg[i], seg[i + 1]) for i in range(0, len(seg), 2)]
            draw.polygon(seg, fill=255)
    
    mask.save(os.path.join(mask_dir, f"{img_name}_masked.jpg"))

    # mask.show()
