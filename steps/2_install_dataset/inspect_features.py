import tensorflow as tf


def inspect_tfrecord(file_path):
    # Create a TFRecordDataset
    dataset = tf.data.TFRecordDataset(file_path)
    
    # Iterate through the dataset
    for i, raw_record in enumerate(dataset.take(1)):  # Take 10 records (adjust as needed)
        print(f"\nRecord {i+1}:\n")
        # Decode the raw record to a tensor
        print(f"Raw record (bytes): {raw_record.numpy()}\n")

if __name__ == "__main__":
    inspect_tfrecord("models_files/my_dataset/train.tfrecord")