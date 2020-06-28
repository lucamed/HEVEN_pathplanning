# Making a dataset and training it for YOLOV3

Preparation:
1. Background images: Find 500+ pictures sized in at least 608x608 but ideally larger - random scenery
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
1. Separate train and test dataset through Split
2. Fill objects.names with needed classes in order with the image names. E.g 0 -> first class
3. Fill obj.data with the needed paths 
4. Calculate anchor values
5. Tune hyperparameters:
	- Batch_size: 64				Subdivisions: 16
	- **Max batches = (classes*2000)**. eg: 12 classes ->                HxW: 608x608
	- max_batches = 24000
	- **Filters=(classes + 5)x3 -> 51** **_ONLY THE LAST LAYER OF EVERY CNN (3)_**
	- Line 17 flip = 0
	- **steps = (max_batches * 0.8), (max_batches * 0.9)**
	
Anchors

./darknet detector calc_anchors custom/obj.data -num_of_clusters 9 -width 608 -height 608

 eg. 16, 27,  32, 49,  51, 83,  51,172,  82,125, 123,195, 189,135, 165,257, 255,350

1. Training:
	- ./darknet detector train custom/ obj.data custom/yolov3-64.cfg darknet53.conv.74 `
2. Testing: 
	- ./darknet detector test custom/obj.data custom/yolov3-642.cfg backup/yolov3-64_last.weights [imgname].jpg`
3. Check accuracy mAP:
	- ./darknet detector map custom/trainer.data custom/yolov3-642.cfg backup/yolov3-64_last.weights.weights`

	
