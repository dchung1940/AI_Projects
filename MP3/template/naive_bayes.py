import math
# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior = P(type = Positive)
    """
    # TODO: Write your code here
    # return predicted labels of development set
    # P(Yes | Sunny) = P( Sunny | Yes) * P(Yes) / P (Sunny)

    pos_lookup_table = {}
    neg_lookup_table = {}
    total_n = 0
    total_p = 0
    # print(train_labels)
    # print(len(train_set))
    # print(len(train_labels))
    for i in range(len(train_set)):
        review = train_labels[i]
        for j in range(len(train_set[i])):
            key_ = train_set[i][j]
            if(review == 1):
                # print("1")
                total_p += 1
                if(key_ in pos_lookup_table):
                    pos_lookup_table[key_] += 1
                else:
                    pos_lookup_table[key_] = 1
            else:
                # print("0")
                total_n +=1
                if(key_ in neg_lookup_table):
                    neg_lookup_table[key_] += 1
                else:
                    neg_lookup_table[key_] = 1
    # print(pos_lookup_table)
    # print(neg_lookup_table)
    # print(len(pos_lookup_table))
    # print(len(neg_lookup_table))
    pos_v = len(pos_lookup_table)
    neg_v = len(neg_lookup_table)

    alpha = .1
    # print(total_n)
    pos_prob =[]
    neg_prob =[]

    for i in range(len(dev_set)):
        temp_positive = 0
        temp_negative = 0
        for word in dev_set[i]:
            if word in pos_lookup_table:
                count_w_pos = pos_lookup_table[word]
                temp_positive += math.log((count_w_pos + alpha)/(total_p+alpha*(pos_v+1)))
            else:
                temp_positive += math.log(alpha / (total_p+alpha*(pos_v+1)))
            if word in neg_lookup_table:
                count_w_neg = neg_lookup_table[word]
                temp_negative += math.log((count_w_neg + alpha)/(total_n+alpha*(neg_v+1)))
            else:
                temp_negative += math.log(alpha / (total_n+alpha*(neg_v+1)))
        pos_prob.append(temp_positive)
        neg_prob.append(temp_negative)
    
    # a = 0
    # print(pos_prob)
    # print(neg_prob)
    final_prob = []

    for i in range(len(dev_set)):
        if (pos_prob[i] + math.log(pos_prior) > neg_prob[i] + math.log((1-pos_prior))):
            # print(pos_prob[i] + math.log(pos_prior))
            final_prob.append(1)
        else:
            # print("-1")
            final_prob.append(0)
    
    return final_prob
