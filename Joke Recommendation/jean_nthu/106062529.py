
# coding: utf-8

# In[1]:


import sys
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def loadTrainFile():
    userID = []
    itemID = []
    rating = []
    with open("train.csv") as f:
        for i,line in enumerate(f):
            if(i>0):
                row = line.strip().split(',')
                
                if(row[2]!='99.0'):
                    userID.append(round(float(row[0])))
                    itemID.append(round(float(row[1])))
                    rating.append(float(row[2]))
                
    return userID, itemID, rating

def loadTestFile():
    userID = []
    itemID = []
    with open("test.csv") as f:
        for i,line in enumerate(f):
            if(i>0):
                row = line.strip().split(',')
                userID.append(round(float(row[0])))
                itemID.append(round(float(row[1])))
                
    return userID, itemID

#############Data#############
train_userID, train_itemID, train_rating = loadTrainFile()
test_userID, test_itemID = loadTestFile()
#############User-User#############
user_item_ratings = np.zeros([10000,100])
user_item_has_ratings = np.full([10000,100], False)
for i, r in enumerate(train_rating):
    user_item_ratings[train_userID[i]-1][train_itemID[i]-1]=r
    user_item_has_ratings[train_userID[i]-1][train_itemID[i]-1]=True

user_mean = np.zeros([10000])
for i,ratings in enumerate(user_item_ratings):
    n = user_item_has_ratings[i].tolist().count(True)
    mean = ratings.sum()/n
    user_mean[i] = mean
    for j in range(len(ratings)):
        if(user_item_has_ratings[i][j]):
            user_item_ratings[i][j]-=mean

#User-User -> Item-Item
item_user_ratings = user_item_ratings.T
item_user_has_ratings = user_item_has_ratings.T
#print(user_mean)

# #############Item-Item############# 
# item_user_ratings = np.zeros([100,10000])
# item_user_has_ratings = np.full([100,10000], False)
# for i, r in enumerate(train_rating):
#     item_user_ratings[train_itemID[i]-1][train_userID[i]-1]=r
#     item_user_has_ratings[train_itemID[i]-1][train_userID[i]-1]=True

# #minus mean
# item_mean = np.zeros([100])
# for i,ratings in enumerate(item_user_ratings):
#     n = item_user_has_ratings[i].tolist().count(True)
#     mean = ratings.sum()/n
#     item_mean[i] = mean
#     for j in range(len(ratings)):
#         if(item_user_has_ratings[i][j]):
#             item_user_ratings[i][j]-=mean
# # print("item_user_ratings")
# # print(item_user_ratings)
# # print(item_user_ratings.sum(axis=1))
# # print(item_user_has_ratings)

item_similarity = np.full([100,100],1)
item_similarity = item_similarity-pairwise_distances(item_user_ratings, metric='cosine')
# print("item_similarity")
# print(item_similarity)
sort_index = np.argsort(-item_similarity,axis=1)
# print(sort_index)
# print(item_mean)

test_output=[['user_id-item_id','rating']]
for i in range(len(test_userID)):
    user_idx = test_userID[i]-1
    item_idx = test_itemID[i]-1
    n = 0
    similarity_sum = 0.0
    weighted_rate = 0.0
#     print('user_idx ', user_idx, 'item_idx ', item_idx)
    if(item_user_has_ratings[item_idx][user_idx]):
        value = item_user_ratings[item_idx][user_idx]
    else:
        for neighbor in sort_index[item_idx]:
            if(item_user_has_ratings[neighbor][user_idx]):
#                 print('neighbor ', neighbor, 'sim=', item_similarity[item_idx][neighbor])
                weighted_rate += item_user_ratings[neighbor][user_idx]*item_similarity[item_idx][neighbor]
                similarity_sum += abs(item_similarity[item_idx][neighbor])
                n+=1
            if(n==15 or item_similarity[item_idx][neighbor]< 0):
                weighted_rate /= similarity_sum
#                 value = weighted_rate+item_mean[item_idx]
                value = weighted_rate+user_mean[user_idx]
                break

    entry = str(test_userID[i])+'-'+str(test_itemID[i])
    test_output.append([entry,value])
np.savetxt("answer.csv", np.array(test_output, dtype=np.str), fmt='%s,%s', delimiter=",")


# In[ ]:


# output_userID=[]
# output_itemID=[]
# output_rating=[]

# with open("answer.csv") as f:
#         for i,line in enumerate(f):
#             if(i>0):
#                 row = line.strip().split(',')
#                 u_i = row[0].split('-')

#                 output_userID.append(int(u_i[0]))
#                 output_itemID.append(int(u_i[1]))
#                 output_rating.append(float(row[1]))

# output_item_user=np.zeros([100,10000])
# for i in range(len(output_userID)):
#     output_item_user[output_itemID[i]-1][output_userID[i]-1]=output_rating[i]
# output_mean = np.zeros([100])
# for i,item in enumerate(output_item_user):
#     output_mean[i] = item.mean()
# print(output_mean)


# In[ ]:


# output_userID=[]
# output_itemID=[]
# output_rating=[]

# with open("answer.csv") as f:
#         for i,line in enumerate(f):
#             if(i>0):
#                 row = line.strip().split(',')
#                 u_i = row[0].split('-')

#                 output_userID.append(int(u_i[0]))
#                 output_itemID.append(int(u_i[1]))
#                 output_rating.append(float(row[1]))

# output_user_item=np.zeros([10000,100])
# for i in range(len(output_userID)):
#     output_user_item[output_userID[i]-1][output_itemID[i]-1]=output_rating[i]
# output_mean = np.zeros([10000])
# for i,item in enumerate(output_user_item):
#     output_mean[i] = item.mean()
# print(output_mean)

