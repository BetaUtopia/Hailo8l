import tensorflow as tf
from hailo_sdk_client.runner.client_runner import ClientRunner

def validate_shapes(dataset):
    """Validates the shapes of the dataset elements."""
    # Inspect element_spec
    element_spec = dataset.element_spec
    print("Dataset element_spec:", element_spec)
    
    if isinstance(element_spec, tuple):
        # If element_spec is a tuple of TensorSpec objects
        for spec in element_spec:
            if isinstance(spec, tf.TensorSpec):
                print("Shape:", spec.shape)
                print("Dtype:", spec.dtype)
    elif isinstance(element_spec, tf.TensorSpec):
        # If element_spec is a single TensorSpec object
        print("Shape:", element_spec.shape)
        print("Dtype:", element_spec.dtype)
    else:
        raise TypeError("Unsupported element_spec type")

# Assuming `dataset` is already created and loaded with data
dataset = ...  # Your dataset loading logic here

# Validate dataset shapes
validate_shapes(dataset)

# Example usage in Hailo SDK
runner = ClientRunner(...)
calib_data = ...  # Your calibration data loading logic here

# Optimize with the calibration data
runner.optimize(calib_data)
