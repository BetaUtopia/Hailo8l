# On the Raspbery Pi 5

### Install Requirements
```bash
sudo apt-get update
sudo apt-get install python3-picamera2
pip install opencv-python Pillow
```

### Get Images
```bash
python steps/0_get_images/from_raspberypi.py --classname Green_Cube --total_pictures 100 --onkeypress
```
<!-- # Get Images
python from_raspberypi.py --classname Green_Cube --total_pictures 100 -->