
# coding: utf-8

# In[12]:


import sys
import numpy as np
from sklearn import preprocessing

def loadTrainFile():
    tmp = np.loadtxt("train.csv", dtype=np.str, delimiter=",")
    userID = tmp[1:,0].astype(int)
    item1 = tmp[1:,1].astype(int)
    item2 = tmp[1:,2].astype(int)
    labels = tmp[1:,3].astype(int)
    return userID, item1, item2, labels
def loadTestFile():
    tmp = np.loadtxt("test.csv", dtype=np.str, delimiter=",")
    userID = tmp[1:,0].astype(int)
    item1 = tmp[1:,1].astype(int)
    item2 = tmp[1:,2].astype(int)
    return userID, item1, item2
def loadUserFile():
    tmp = np.loadtxt("users.csv", dtype=str, delimiter=",")
    return tmp[1:,1:]

def loadItemFile():
    tmp = np.loadtxt("items.csv", dtype=np.str, delimiter=",")
    return tmp[1:,1:]



# In[55]:


########### Data ###########
user_dic = loadUserFile()
item_dic = loadItemFile()
userID, item1, item2, labels = loadTrainFile()

user_car_preference = np.zeros([len(user_dic),10], dtype=int)
weighted_user_car_preference = np.zeros([len(user_dic),10], dtype=float)

for idx, label in enumerate(labels):
    if(label==0):
        user_car_preference[userID[idx]-1][item1[idx]-1]+=1
        user_car_preference[userID[idx]-1][item2[idx]-1]-=1
    else:
        user_car_preference[userID[idx]-1][item1[idx]-1]-=1
        user_car_preference[userID[idx]-1][item2[idx]-1]+=1
norm = np.linalg.norm(user_car_preference, axis=1, ord=2)
user_car_preference  = user_car_preference / norm[:, None]
user_car_preference = user_car_preference-user_car_preference.min()

for idx, label in enumerate(labels):
    if(label==0):
        weighted_user_car_preference[userID[idx]-1][item1[idx]-1]+=user_car_preference[userID[idx]-1][item2[idx]-1]
        weighted_user_car_preference[userID[idx]-1][item2[idx]-1]-=user_car_preference[userID[idx]-1][item1[idx]-1]
    else:
        weighted_user_car_preference[userID[idx]-1][item1[idx]-1]-=user_car_preference[userID[idx]-1][item2[idx]-1]
        weighted_user_car_preference[userID[idx]-1][item2[idx]-1]+=user_car_preference[userID[idx]-1][item1[idx]-1]

#weighted_user_car_preference = preprocessing.scale(user_car_preference, axis=1, copy=False)
user_carAttribute_preference = {}

#initialize user_carAttribute_preference
for user in range(len(user_dic)):
    user_carAttribute_preference[user] = {0:{'1':0,'2':0}, 1:{'1':0, '2':0}, 2:{'2.5':0, '3.5':0, '4.5':0, '5.5':0, '6.2':0}, 3:{'1':0, '2':0}}

for user, probabilities in enumerate(user_car_preference):
    for car, per_car_probability in enumerate(probabilities):
        this_car_attributes = item_dic[car]
        for attr_idx, attr in enumerate(this_car_attributes):
            user_carAttribute_preference[user][attr_idx][attr]+=weighted_user_car_preference[user][car]
all_people_preference = np.mean(user_car_preference, axis=0)

# tmp = np.concatenate([user_dic, user_car_preference], axis=1)
# np.savetxt("userattr_carprob.csv", np.array(tmp, dtype=np.str),fmt='%s', delimiter=",")

def getItemPreferenceByAttribute(attributes, user_reference_table):
    result = 0.0;
    for idx, attr in enumerate(attributes):
        result += user_reference_table[idx][attr]
    return result
########## Data ###########
# hit = 0
# equal = 0
# other = 0
# for idx in range(userID.shape[0]):
#     if(labels[idx]==0 and user_car_preference[userID[idx]-1][item1[idx]-1]>user_car_preference[userID[idx]-1][item2[idx]-1]):
#         hit+=1
#     elif(labels[idx]==1 and user_car_preference[userID[idx]-1][item1[idx]-1]<user_car_preference[userID[idx]-1][item2[idx]-1]):
#         hit+=1
#     elif(user_car_preference[userID[idx]-1][item1[idx]-1]==user_car_preference[userID[idx]-1][item2[idx]-1]):
#         equal+=1
#         item1_preference = getItemPreferenceByAttribute(item_dic[item1[idx]-1], user_carAttribute_preference[userID[idx]-1])
#         item2_preference = getItemPreferenceByAttribute(item_dic[item2[idx]-1], user_carAttribute_preference[userID[idx]-1])
#         if(labels[idx]==0 and item1_preference >= item2_preference):
#             hit+=1
#         elif(labels[idx]==1 and item1_preference < item2_preference):
#             hit+=1
#     else:
#         other+=1

# print("hit %: " , hit/userID.shape[0])
# print("equal: ", equal)
# print("other: ", other)


# In[56]:


########## Test ##########
print("########## Start Test ##########")
equal = 0
other = 0

userID, item1, item2 = loadTestFile()
test_output=[['User-Item1-Item2','Preference']]

for idx in range(userID.shape[0]):
    entry = str(int(userID[idx]))+'-'+str(int(item1[idx]))+'-'+str(int(item2[idx]))
    item1_preference = getItemPreferenceByAttribute(item_dic[item1[idx]-1], user_carAttribute_preference[userID[idx]-1])
    item2_preference = getItemPreferenceByAttribute(item_dic[item2[idx]-1], user_carAttribute_preference[userID[idx]-1])
    if(item1_preference >= item2_preference):
        if(item1_preference == item2_preference):
            equal+=1
        value=0
    else:
        value=1
    test_output.append([entry,value])
print("output #(lines)", len(test_output))
print("equal: ",equal)
np.savetxt("answer.csv", np.array(test_output, dtype=np.str), fmt='%s,%s', delimiter=",")

