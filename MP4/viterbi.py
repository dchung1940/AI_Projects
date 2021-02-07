import math
"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    temp_dict = {}
    predicts = []
    for sentence in train:
        for word in sentence:
                # print(word)
                if word[0] in temp_dict:
                        if word[1] in temp_dict[word[0]]:
                                temp_dict[word[0]][word[1]] = temp_dict[word[0]][word[1]] + 1
                        else:
                                temp_dict[word[0]][word[1]] = 1
                else:
                        temp_dict[word[0]] = {word[1]:1}
#     print(temp_dict)
    for sentence in test:
        temp_sen = []
        for word in sentence:
                if word in temp_dict:
                        count = 0
                        temp_word = ""
                        for i in temp_dict[word]:
                                if temp_dict[word][i] > count:
                                        temp_word = i
                                        count = temp_dict[word][i]
                        temp_sen.append((word,temp_word))
                else:
                        temp_sen.append((word,'NOUN'))
        predicts.append(temp_sen)
    return predicts


def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tag_list = ['START', 'ADJ','ADV','IN','PART','PRON','NUM','CONJ','UH','TO','VERB','MODAL','DET','NOUN','PERIOD','PUNCT','X']
    init_dict = {}
    alpha = .001
    for i in tag_list:
        if(i == 'START'):
                init_dict['START'] =1
        else:
                init_dict[i] = .0000000001
#     print(init_dict)
    tran_dict = {}
    for sentence in train:
        for word in range(len(sentence)):
                if sentence[word][1] == 'START':
                        # print(sentence[word][1])
                        continue
                else:
                        if sentence[word-1][1] in tran_dict:
                                if sentence[word][1] in tran_dict[sentence[word-1][1]]:
                                        tran_dict[sentence[word-1][1]][sentence[word][1]] +=1
                                else:
                                        tran_dict[sentence[word-1][1]][sentence[word][1]] = 1
                        else:
                                tran_dict[sentence[word-1][1]] = {sentence[word][1]:1}
#     print(tran_dict)
#     for i in tran_dict:
#             count = 0
#             for j in tran_dict[i]:
#                     count += tran_dict[i][j]
#             for k in tran_dict[i]:
#                     tran_dict[i][k] = (tran_dict[i][k] + alpha)/count
#     print(tran_dict)

    base_dict = {}
    total_num_words = 0
    for sentence in train:
        for word in sentence:
                # print(word)
                # break
                if word[0] in base_dict:
                        if word[1] in base_dict[word[0]]:
                                base_dict[word[0]][word[1]] = base_dict[word[0]][word[1]] + 1
                        else:
                                base_dict[word[0]][word[1]] = 1
                else:
                        base_dict[word[0]] = {word[1]:1}
                total_num_words +=1

    emiss_dict = {}
    for sentence in train:
            for word in sentence:
                if word[1] in emiss_dict:
                        if word[0] in emiss_dict[word[1]]:
                                emiss_dict[word[1]][word[0]] +=1
                        else:
                                emiss_dict[word[1]][word[0]] = 1
                else:
                        emiss_dict[word[1]] = {word[0]:1}
                            
                                
    emiss_count = {}
    for i in emiss_dict:
        count = 0
        for j in emiss_dict[i]:
                count += emiss_dict[i][j]
        emiss_count[i] = count

    tran_count = {}
    for i in tran_dict:
        count = 0
        for j in tran_dict[i]:
                count += tran_dict[i][j]
        tran_count[i]=count


#     lol = 0
    predicts = []
    for sentence in test:
        temp_sen = []
        matrix = [[0 for x in range(len(sentence))]for y in range(17)]
        for num in range(len(sentence)):
                word = sentence[num]
                if word in base_dict:
                        for col in range(len(tag_list)):
                                tag = tag_list[col]
                                if(num == 0):
                                        if(tag in emiss_dict):
                                                if(word in emiss_dict[tag]):
                                                        emiss = (emiss_dict[tag][word] + alpha)/(emiss_count[tag]+18*alpha)
                                                else:
                                                        emiss = alpha/(total_num_words + alpha*18)
                                        else:
                                                emiss = alpha/(total_num_words + alpha*18)
                                        matrix[col][num] = (math.log(init_dict[tag]) + (math.log(emiss)),'GG')
                                        # print(matrix)
                                else:
                                        val = -1000000000000
                                        tag_temp = 0
                                        for dim in range(len(tag_list)):
                                                tag_prev = tag_list[dim]
                                                emiss = 0
                                                trans = 0
                                                if(tag in emiss_dict):
                                                        if(word in emiss_dict[tag]):
                                                                emiss = (emiss_dict[tag][word] + alpha)/(emiss_count[tag]+18*alpha)
                                                        else:
                                                                emiss = alpha/(total_num_words + alpha*18)
                                                else:
                                                        emiss = alpha/(total_num_words + alpha*18)
                                                if(tag_prev in tran_dict):
                                                        if(tag in tran_dict[tag_prev]):
                                                                trans = (tran_dict[tag_prev][tag]+alpha)/(tran_count[tag_prev]+alpha*18)
                                                        else:
                                                                trans = alpha/(tran_count[tag_prev]+alpha*18)
                                                else:
                                                        trans = alpha/(total_num_words + alpha*18)
                                                # print(matrix)
                                                # print(matrix[dim][num-1],"aa",dim,"dd",num-1,"dd",math.log(trans),"bb",math.log(emiss))
                                                calc = matrix[dim][num-1][0]+math.log(trans)+math.log(emiss)
                                                if(calc > val):
                                                        val = calc
                                                        tag_temp = dim
                                        matrix[col][num] = (val,tag_temp)
                else:
                        for col in range(len(tag_list)):
                                tag = tag_list[col]
                                if(num == 0):
                                        if(tag in emiss_dict):
                                                temp = len(emiss_dict[tag])/total_num_words
                                                if(word in emiss_dict[tag]):
                                                        emiss = (emiss_dict[tag][word] + alpha*temp)/(emiss_count[tag]+18*alpha)
                                                else:
                                                        
                                                        emiss = alpha/(total_num_words + alpha*18)
                                        else:
                                                emiss = alpha*temp/(total_num_words + alpha*18)
                                        matrix[col][num] = (math.log(init_dict[tag]) + math.log(emiss),'GG')
                                else:
                                        val = -10000000000
                                        tag_temp = 0
                                        emiss =0
                                        trans = 0
                                        for dim in range(len(tag_list)):

                                                tag_prev = tag_list[dim]
                                                if(tag in emiss_dict):
                                                        temp = len(emiss_dict[tag])/total_num_words
                                                        emiss = temp*alpha/(total_num_words + temp*alpha*18)
                                                else:
                                                        emiss = alpha*temp/(total_num_words + alpha*18)
                                                # count = 0
                                                # for j in tran_dict[tag_prev]:
                                                #         count += tran_dict[tag_prev][j]
                                                if(tag_prev in tran_dict):
                                                        if(tag in tran_dict[tag_prev]):
                                                                trans = (tran_dict[tag_prev][tag]+alpha)/(tran_count[tag_prev]+alpha*18)
                                                        else:
                                                                trans = alpha/(tran_count[tag_prev]+alpha*18)
                                                else:
                                                        trans = alpha/(total_num_words + alpha*18)
                                                calc = matrix[dim][num-1][0] + math.log(trans)+math.log(emiss)
                                                if(calc > val):
                                                        val = calc
                                                        tag_temp = dim
                                        matrix[col][num] = (val,tag_temp)
                
        sent_len = len(sentence)-1
        max_value = matrix[0][sent_len][0]
        tag_num = 0
        for i in range(17):
                if matrix[i][sent_len][0]>max_value:
                        max_value = matrix[i][sent_len][0]
                        tag_num = i

        # print(sentence[sent_len],tag_list[tag_num])
        while(sent_len != 0):
                temp_sen.append((sentence[sent_len],tag_list[tag_num]))
                tag_num = matrix[tag_num][sent_len][1]
                sent_len = sent_len-1
        temp_sen.append((sentence[0],'START'))
        temp_sen.reverse()
        predicts.append(temp_sen)
        # lol +=1
        # print(lol)
    return predicts

                        




                
        # predicts.append(temp_sen)
#     for i in emiss_dict:
#             count = 0
#         #     print(i)
#         #     break
#             for j in emiss_dict[i]:
#                     count += emiss_dict[i][j]
#             for k in emiss_dict[i]:
#                     emiss_dict[i][k] = emiss_dict[i][k]/count
#     print(emiss_dict)


#     cal_tran_val = {}
#     for sentence in test:
#             cur_tag = 'START'
#             for k in range(1,len(sentence)):
#                         count = 0
#                         total = 0
#                         temp_word = ''
#                         word = sentence[k]
#                         for i in tran_dict[word]:  
#                                 total += tran_dict[word][i]
#                                 if tran_dict[word][i] > count:
#                                         temp_word = i
#                                         count = temp_dict[word][i]
#                 temp_sen.append((word,temp_word))

                    
                                 
    
#     predicts = []
#     raise Exception("You must implement me")
#     return predicts
