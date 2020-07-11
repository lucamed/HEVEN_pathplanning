#HOW-TO

1. Separate train and test dataset through [Split](/YOLO/Split_Train_Test.py)
2. Fill [objects.names](./objects.names) with needed classes in order with the image names. E.g 0 -> first class
3. Set right paths in [trainer.data](./trainer.data)
4. Edits needed for the YOLO cfg files:
    - Classes - num of needed classes
    - Max batches = (classes*2000). eg: 3 classes -> max_batches = 6000
    - Filters=(classes + 5)x3
    - Anchors --> `./darknet detector calc_anchors custom/trainer.data -num_of_clusters 6 -width 416 -height 416`



Training:
`./darknet detector train custom/trainer.data custom/yolov3.cfg darknet53.conv.74 `

Testing: 
`./darknet detector test custom/trainer.data custom/yolov3.cfg backup/[filename].weights [imgname].jpg`

Check accuracy mAP:
`./darknet detector map custom/trainer.data custom/[].cfg backup/[].weights`
