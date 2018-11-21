# Data_Compilation

## Objective

Give a drone the ability to asess to safety of a landing zone underneath from a video feed and to look for a landing zone safe enough. To be able to test the results I'll implement a basic simulation.

## Train the ConvNet (Inception) 

To train the network, I picked a satelite image of a city and drawn a mask of "danger".

http://www.mediafire.com/view/5hdm63pad6cw29s/Out.bmp

![out](preview_out.png)

http://www.mediafire.com/view/mlk5tweibs6ggz0/Base.bmp

![base](preview_base.png)


Then we use *Data_compilation.py* to split the two images in many pairs of small crops that correspond it the same geographical region. 

![split](preview_split.png)

We can use the data generated to train a segmentation network but for our use a classifier semms more apropriate.
To train a classifier, we can seperate the images by calculating the level of "safety" with the average of the pixel brightness.

This work is done by *class.py*

