# Data Augmentation for Object Detection(YOLO)

TODO:
- Find more targets and usefull backgrounds

The available image transfromations are as follows:-
1. Addition of Gaussian noise.
2. Brightness variation.
3. Addition of Salt and Pepper noise.
4. Scaling of the image.
5. Affine rotation given the maximum possible rotation. 
6. Perspective Transform within user provided min and max rotation angle about x, y and z axes.
7. Image sharpening.
8. Power Law transfrom for illumination effects. (needs to be update)

The starting point is the [CreateSamples](./CreateSamples.py). 
Define the required parameters in [Parameters](./Parameters.config). 

SUGGESTION: As sample images it is good to use images where there are a couple of rows and columns of white/black pixels padding the object. These will help in reducing the cropping of the object during rotation.

[SampleImageInterface](./SampleImgInterface.py) is the class that contains all the transfomrations in a single class. It also has functions to extract the tight bounding box of the modified sample image before it is placed on background images. 


Referred Sources and borrowed scripts:
1. https://github.com/srp-31/Data-Augmentation-for-Object-Detection-YOLO-
2. https://github.com/eborboihuc/rotate_3d 
3. https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
