
# How to Setup Raspberry Pi 5 with Hailo8l AI Kit using yolov8n on Windows (WSL2 Ubuntu)

## WSL Ubuntu

### Get Guide
```bash
git clone https://github.com/BetaUtopia/Hailo8l.git
```

### Training
```bash
cd Hailo8l
sudo apt-get update
sudo apt-get install libpython3.11-stdlib libgl1-mesa-glx
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv_yolov8
source venv_yolov8/bin/activate
pip install ultralytics
```

```bash
cd model
```

```bash
yolo detect train data=coco128.yaml model=yolov8n.pt name=retrain_yolov8n project=./runs/detect epochs=100 batch=16

```

### Convert to ONNX
```bash
cd runs/detect/retrain_yolov8n/weights   
```

```bash
yolo export model=./best.pt imgsz=640 format=onnx opset=11 
```

```bash
cd ~/Hailo8l && deactivate
```

### Install Hailo
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3.8-dev
```

```bash
python3.8 -m venv venv_hailo
source venv_hailo/bin/activate
sudo apt-get update
sudo apt-get install build-essential python3-dev graphviz graphviz-dev python3-tk
pip install pygraphviz
```

```bash
pip install whl/hailo_dataflow_compiler-3.27.0-py3-none-linux_x86_64.whl
pip install whl/hailo_model_zoo-2.11.0-py3-none-any.whl
```

```bash
git clone https://github.com/hailo-ai/hailo_model_zoo.git
```

### Install Coco dataset
```bash
python hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py val2017
python hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py calib2017
```

```bash
cd model/runs/detect/retrain_yolov8n/weights
```

### Parse
```bash
hailomz parse --hw-arch hailo8l --ckpt ./best.onnx yolov8n
```

### Optimize
-Use your own username /home/USER

```bash
hailomz optimize --hw-arch hailo8l --har ./yolov8n.har \
    --calib-path /home/sam/.hailomz/data/models_files/coco/2023-08-03/coco_calib2017.tfrecord \
    --model-script /home/sam/Hailo8l/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/yolov8n.alls \
    yolov8n
```

### Compile
```bash
hailomz compile yolov8n --hw-arch hailo8l --har ./yolov8n.har
```

## Raspbery Pi 5

```bash
cd hailo8l
git clone https://github.com/hailo-ai/hailo-rpi5-examples.git
pip install setproctitle

```

```bash
cd hailo-rpi5-examples
source setup_env.sh
cd ..
```

```bash
python hailo-rpi5-examples/basic_pipelines/detection.py -i rpi --hef yolov8n.hef
```

