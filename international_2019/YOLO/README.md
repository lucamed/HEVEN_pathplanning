# Making a dataset and training it for YOLOV3

Preparation:
1. Background images: Find 500+ pictures sized in at least 408x408 but ideally larger - random scenery
2. Target images: 
	- Add some real life signs to the data
	- Find bigger images
	- Change background color to black: images with white writings on it and do augmentation separatetly (cuz of crop)
	- Do augmentation for left and right separatelly without flip option (or without z transform)
	- Traffic Lights - find green arrow dataset/ put it on a white background
	- Make all balanced as 1:1 classes (10 targets per class)

3. Negative samples- find ~20000 images of random scenery WITHOUT any of the classes (maybe add bg imgs here)
	add selected street pictures also. Video framed.
4. Validation dataset - part of total dataset


Augmentation:
1. Do a complete Create_Samples.py process for the white background pictures with 200 samples per img 
2. Black backgrounded (excluding left/right) images also do complete process but with different bgd settings (=0)
3. Right/left, do the process with z_transform OFF
4. Yolo_mark labeling the real pictures
6. Merge all files (img and parameters) into one folder ~24000

Training:
./darknet detector train data/obj.data custom/yolo-obj.cfg darknet53.conv.74 -map
1. Separate train, test, valid datasets
2. Fill obj.names with all the classes names
3. Fill obj.data with the needed paths 
4. Calculate anchor values
5. Tune hyperparameters:
	- batch = 64
	- subdivision = 16
	- max_batches = 24000
	- steps=19200,21600
	- *line 17* flip = 0
	- classes = 12
	- filters = 51 (only before yolo networks, leave the rest same)
	
...

Image feeding / Buffer
 - Check ImageAI, pytorch-yolo, darknetpy libraries
...
