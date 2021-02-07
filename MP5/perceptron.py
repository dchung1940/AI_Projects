# perceptron.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np
def classify(train_set, train_labels, dev_set, learning_rate,max_iter):
    """
    train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
                This can be thought of as a list of 7500 vectors that are each
                3072 dimensional.  We have 3072 dimensions because there are
                each image is 32x32 and we have 3 color channels.
                So 32*32*3 = 3072
    train_labels - List of labels corresponding with images in train_set
    example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
             and X1 is a picture of a dog and X2 is a picture of an airplane.
             Then train_labels := [1,0] because X1 contains a picture of an animal
             and X2 contains no animals in the picture.

    dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
              It is the same format as train_set
    """
    # TODO: Write your code here
    # return predicted labels of development set
    #train
    matrix = np.zeros(len(train_set[0]))
    bias = 0.0
    # print(max_iter)
    for j in range(max_iter):
        for i in range(len(train_set)):
            rgb_pic = train_set[i]
            label = train_labels[i]
            y_compute = np.dot(rgb_pic,matrix)+bias
            # print(y_compute)
            if(y_compute < 0):
                y_compute = 0
            else:
                y_compute = 1
            # print(matrix)
            # if(y_compute == label):
            #     continue
            matrix += learning_rate*(label - y_compute)*rgb_pic
            # print(matrix)
        #The weight of the bias term in a layer is updated in the same fashion as all the other weights are.
        #What makes it different is that it is independent of output from previous layers.
            bias += learning_rate*(label - y_compute)*1
    
    print(bias,"\n",matrix)
    #development
    result =[]
    for i in range(len(dev_set)):
        rgb_pic = dev_set[i]
        y_compute = np.dot(rgb_pic,matrix)+bias
        # print(y_compute)
        if(y_compute <0):
            result.append(0)
        else:
            result.append(1)

    return result

def classifyEC(train_set, train_labels, dev_set,learning_rate,max_iter):
    # Write your code here if you would like to attempt the extra credit
    matrix = np.zeros(len(train_set[0]))
    bias = 0.5
    # print(max_iter)
    for i in range(len(train_set)):
        rgb_pic = train_set[i]
        label = train_labels[i]
        for j in range(max_iter):
            y_compute = np.sign(np.dot(rgb_pic,matrix)+bias)
            # print(y_compute)
            # if(y_compute < 0):
            #     y_compute = -1
            # elif(y_compute == 0):
            #     y_compute = 0
            # else:
            #     y_compute = 1
            
            # if(y_compute == label):
            #     break
            if((y_compute == -1 and label == 0) or (y_compute == 1 and label == 1)):
                break
            matrix += learning_rate*(label - y_compute)*rgb_pic
            # print(matrix)
        #The weight of the bias term in a layer is updated in the same fashion as all the other weights are.
        #What makes it different is that it is independent of output from previous layers.
            bias += learning_rate*(label - y_compute)*1
    
    
    #development
    result =[]
    for i in range(len(dev_set)):
        rgb_pic = dev_set[i]
        y_compute = np.dot(rgb_pic,matrix)+bias
        # print(y_compute)
        if(y_compute <0):
            result.append(0)
        else:
            result.append(1)

    return result
    
