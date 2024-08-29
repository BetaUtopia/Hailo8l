from hailo_sdk_client import ClientRunner

onnx_model_name = 'best'
onnx_path = '/home/sam/Hailo8l/model/runs/detect/retrain_yolov8n/weights/best.onnx'
har_path = '/home/sam/Hailo8l/model/runs/detect/retrain_yolov8n/weights/best.har'

chosen_hw_arch = 'hailo8l'

runner = ClientRunner(hw_arch=chosen_hw_arch)
hn, npz = runner.translate_onnx_model(
    onnx_path, onnx_model_name,
    start_node_names=['images'],
    end_node_names=['/model.22/cv2.0/cv2.0.2/Conv', '/model.22/cv3.0/cv3.0.2/Conv', '/model.22/cv2.1/cv2.1.2/Conv', '/model.22/cv3.1/cv3.1.2/Conv', '/model.22/cv2.2/cv2.2.2/Conv', '/model.22/cv3.2/cv3.2.2/Conv'],
    net_input_shapes={'images': [1, 3, 640, 640]})

runner.save_har(har_path)
print(f"Model successfully translated and saved as {har_path}")
