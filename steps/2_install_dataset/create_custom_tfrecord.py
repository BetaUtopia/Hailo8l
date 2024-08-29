#!/usr/bin/env python

import argparse
import os
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image
from tqdm import tqdm

TF_RECORD_TYPE = "train", "val"

TF_RECORD_LOC = {
    "train": "models_files/my_dataset/train.tfrecord",
    "val": "models_files/my_dataset/val.tfrecord",
}

def _int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def _bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

def _float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def _create_tfrecord(filenames, name, num_images, imgs_name2id):
    """Loop over all the images in filenames and create the TFRecord"""
    tfrecords_filename = Path(TF_RECORD_LOC[name])
    tfrecords_filename.parent.mkdir(parents=True, exist_ok=True)

    progress_bar = tqdm(filenames[:num_images])
    with tf.io.TFRecordWriter(str(tfrecords_filename)) as writer:
        for i, (img_path, bbox_annotations) in enumerate(progress_bar):
            img_path = Path(img_path)
            progress_bar.set_description(f"{name} #{i+1}: {img_path}")

            xmin, xmax, ymin, ymax, category_id, is_crowd, area = [], [], [], [], [], [], []
            img_jpeg = open(img_path, "rb").read()
            img = np.array(Image.open(img_path))
            image_height = img.shape[0]
            image_width = img.shape[1]

            # Read annotations from the corresponding .txt file
            txt_file_path = Path(f"datasets/labels/{name}") / (img_path.stem + ".txt")
            if txt_file_path.is_file():
                with open(txt_file_path, "r") as txt_file:
                    for line in txt_file:
                        parts = line.strip().split()
                        print(f"Parsing line: {line.strip()}")  # Debug print
                        if len(parts) != 5:
                            print(f"Skipping invalid annotation line: {line.strip()}")
                            continue
                        class_id, x_center, y_center, width, height = map(float, parts)
                        xmin.append((x_center - width / 2) * image_width)
                        xmax.append((x_center + width / 2) * image_width)
                        ymin.append((y_center - height / 2) * image_height)
                        ymax.append((y_center + height / 2) * image_height)
                        category_id.append(int(class_id))
                        is_crowd.append(0)  # Assuming is_crowd is not provided
                        area.append(width * height * image_width * image_height)
            else:
                print(f"Warning: Annotation file {txt_file_path} not found")

            # Log the annotations found for this image
            print(f"Annotations for {img_path.name}:")
            print(f"Xmin: {xmin}")
            print(f"Xmax: {xmax}")
            print(f"Ymin: {ymin}")
            print(f"Ymax: {ymax}")
            print(f"Category ID: {category_id}")
            print(f"Is Crowd: {is_crowd}")
            print(f"Area: {area}")

            # If no boxes were found, log the image for review
            if not category_id:
                print(f"No annotations found for image: {img_path.name}")

            # Generate a numerical ID or skip if not needed
            img_id = i  # Use the index as the ID, or generate your own ID

            example = tf.train.Example(
                features=tf.train.Features(
                    feature={
                        "height": _int64_feature(image_height),
                        "width": _int64_feature(image_width),
                        "num_boxes": _int64_feature(len(category_id)),
                        "image_id": _int64_feature(img_id),
                        "xmin": _float_list_feature(xmin),
                        "xmax": _float_list_feature(xmax),
                        "ymin": _float_list_feature(ymin),
                        "ymax": _float_list_feature(ymax),
                        "area": _float_list_feature(area),
                        "category_id": _int64_feature(category_id),
                        "is_crowd": _int64_feature(is_crowd),
                        "image_name": _bytes_feature(str.encode(img_path.name)),
                        "image/bytes": _bytes_feature(img_jpeg),
                        "image_jpeg": _bytes_feature(img_jpeg),
                        "label": _int64_feature(category_id),
                    }
                )
            )
            writer.write(example.SerializeToString())
            print(f"Processed and written {img_path.name}")
    return i + 1


def get_img_labels_list(dataset_dir, det_dir):
    img_labels_list = []
    imgs_name2id = {}
    
    # Map image files to their names (use filenames as IDs)
    for img_file in Path(dataset_dir).glob("*.jpg"):
        img_name = img_file.name
        img_id = img_name  # Use filename as ID or modify as needed
        imgs_name2id[img_name] = img_id
        txt_file = Path(det_dir) / (img_file.stem + ".txt")
        if txt_file.is_file():
            with open(txt_file, "r") as f:
                annotations = [line.strip() for line in f]
            img_labels_list.append((str(img_file), annotations))
        else:
            print(f"No annotation file found for image: {img_file.name}")
    
    print(f"Loaded {len(img_labels_list)} images and annotations")
    random.shuffle(img_labels_list)
    return img_labels_list, imgs_name2id

def run(dataset_dir, det_dir, name, num_images):
    if dataset_dir == "" or det_dir == "":
        raise ValueError("Please use img and det arguments together.")
    img_labels_list, imgs_name2id = get_img_labels_list(Path(dataset_dir), Path(det_dir))
    images_num = _create_tfrecord(img_labels_list, name, num_images, imgs_name2id)
    print("\nDone converting {} images".format(images_num))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="which tf-record to create {}".format(TF_RECORD_TYPE)) # train or val
    parser.add_argument("--img", "-img", help="images directory", type=str, default="")
    parser.add_argument("--det", "-det", help="detection ground truth directory", type=str, default="")
    parser.add_argument("--num-images", type=int, default=8192, help="Limit num images")
    args = parser.parse_args()
        # Set default paths if not provided
    if args.img == "":
        args.img = f"datasets/images/{args.type}"
    if args.det == "":
        args.det = f"datasets/labels/{args.type}"


    assert args.type in TF_RECORD_TYPE, "need to provide which kind of tfrecord to create {}".format(TF_RECORD_TYPE)
    run(args.img, args.det, args.type, args.num_images)
