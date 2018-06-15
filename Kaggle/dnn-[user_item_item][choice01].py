
# coding: utf-8

# In[1]:


import tensorflow as tf
import numpy as np
import os
import tensorflow as tf

########## Hyperparameter ##########
BATCH_SIZE = 5
EPOCH_BOUND = 1000
EARLY_STOP_CHECK_EPOCH = 60
TAKE_CROSS_VALIDATION = True
LEARNING_RATE = 0.05
CROSS_VALIDATION = 10
########## Hyperparameter ##########

def loadTrainFile():
    tmp = np.loadtxt("train.csv", dtype=np.str, delimiter=",")
    userID = tmp[1:,0].astype(np.float)
    item1 = tmp[1:,1].astype(np.float)
    item2 = tmp[1:,2].astype(np.float)
    label = tmp[1:,3].astype(np.float)
    return userID, item1, item2, label
def loadTestFile():
    tmp = np.loadtxt("test.csv", dtype=np.str, delimiter=",")
    userID = tmp[1:,0].astype(np.float)
    item1 = tmp[1:,1].astype(np.float)
    item2 = tmp[1:,2].astype(np.float)
    return userID, item1, item2
def loadUserFile():
    tmp = np.loadtxt("users.csv", dtype=np.str, delimiter=",")
    user_dic = {}
    for u in tmp[1:]:
        user_dic[int(u[0])] = u[1:]
    return user_dic

def loadItemFile():
    tmp = np.loadtxt("items.csv", dtype=np.str, delimiter=",")
    item_dic = {}
    for i in tmp[1:]:
        item_dic[int(i[0])] = i[1:]
        
    return item_dic

def dnn(x):
    dense1 = tf.layers.dense(
        inputs=x,
        units=10,
        activation=tf.nn.relu,
        name='dense1'
    )
    dense2 = tf.layers.dense(
        inputs=dense1,
        units=10,
        activation=tf.nn.relu,
        name='dense2'
    )
    dense3 = tf.layers.dense(
        inputs=dense2,
        units=10,
        activation=tf.nn.relu,
        name='dense3'
    )
    dense4 = tf.layers.dense(
        inputs=dense3,
        units=10,
        activation=tf.nn.relu,
        name='dense4'
    )
    dense5 = tf.layers.dense(
        inputs=dense4,
        units=10,
        activation=tf.nn.relu,
        name='dense5'
    )
    logits = tf.layers.dense(inputs=dense5, units=2, name='logits')
    
    return logits

# split dataset into training set and one validation set
def split_folds(indices, Inputs, Labels, cross_validation, fold):
    n = Inputs.shape[0]
    if fold == cross_validation:
        validation_size = n - (int(n/cross_validation) * (cross_validation-1))
        X_train_idx, X_validate_idx = indices[:(n-validation_size)], indices[(n-validation_size):]
        y_train_idx, y_validate_idx = indices[:(n-validation_size)], indices[(n-validation_size):]
    else:
        validation_size = int(n/cross_validation)
        X_train_idx, X_validate_idx = np.concatenate((indices[:validation_size*(fold-1)], indices[validation_size*fold:]), axis=0), indices[(validation_size*(fold-1)):(validation_size*fold)]
        y_train_idx, y_validate_idx = np.concatenate((indices[:validation_size*(fold-1)], indices[validation_size*fold:]), axis=0), indices[(validation_size*(fold-1)):(validation_size*fold)]
    X_train, X_validate = np.array(Inputs[X_train_idx,:]), np.array(Inputs[X_validate_idx,:])
    y_train, y_validate = np.array(Labels[y_train_idx]), np.array(Labels[y_validate_idx])
    return X_train, y_train, X_validate, y_validate

def train(X_train, y_train, X_validate, y_validate, optimizer, epoch_bound, stop_threshold, batch_size, testing=False):

    global saver
    global predictions
    global loss
    
    early_stop = 0
    winner_loss = np.infty
    
    for epoch in range(epoch_bound):

        # randomize training set
        indices_training = np.random.permutation(X_train.shape[0])
        X_train, y_train = X_train[indices_training,:], y_train[indices_training]

        # split training set into multiple mini-batches and start training
        total_batches = int(X_train.shape[0] / batch_size)
        for batch in range(total_batches):
            if batch == total_batches - 1:
                sess.run(optimizer, feed_dict={x: X_train[batch*batch_size:], 
                                               y: y_train[batch*batch_size:]})
            else:
                sess.run(optimizer, feed_dict={x: X_train[batch*batch_size : (batch+1)*batch_size], 
                                               y: y_train[batch*batch_size : (batch+1)*batch_size]})
        
        # validating
        cur_loss = 0.0
        total_batches = int(X_validate.shape[0] / batch_size)
        cur_loss = sess.run(loss, feed_dict={x:X_validate,
                                             y:y_validate})
        
        # If the accuracy rate does not increase for many times, it will early stop epochs-loop 
        if cur_loss < winner_loss:
            early_stop = 0
            winner_loss = cur_loss
            
            save_path = saver.save(sess, "./saved_model/dnn.ckpt")
        else:
            early_stop += 1
        if early_stop == stop_threshold:
            break
    
    saver.restore(sess, "./saved_model/dnn.ckpt")
    winner_accuracy = sess.run(accuracy, feed_dict={x:X_validate,
                                                    y:y_validate})
    return winner_loss, winner_accuracy, epoch


# In[2]:


########### Data ###########
user_dic = loadUserFile()
item_dic = loadItemFile()
#train
userID, item1, item2, label = loadTrainFile()

user_X = []
item1_X = []
item2_X = []

for u in userID:
    user_X.append(user_dic[int(u)])
for i in item1:
    item1_X.append(item_dic[int(i)])
for i in item2:
    item2_X.append(item_dic[int(i)])

X_train = np.concatenate([user_X, item1_X, item2_X], axis=1)
X_train = X_train.astype(float)
y_train = label.astype(int)

#test
userID, item1, item2 = loadTestFile()
user_X = []
item1_X = []
item2_X = []

for u in userID:
    user_X.append(user_dic[int(u)])
for i in item1:
    item1_X.append(item_dic[int(i)])
for i in item2:
    item2_X.append(item_dic[int(i)])

X_test = np.concatenate([user_X, item1_X, item2_X], axis=1)
X_test = X_test.astype(float)
########### Data ###########


# In[3]:


########### Model ###########
x = tf.placeholder(tf.float32, [None, X_train.shape[1]], name='x')
y = tf.placeholder(tf.int32, [None], name='y')
onehot_y = tf.one_hot(indices=tf.cast(y,tf.int32), depth=2)

logits = dnn(x)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=onehot_y, logits=logits, name="loss"))

# Training iteration
optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())

# Calculate Accuracy
probabilities = tf.nn.softmax(logits, name="softmax_tensor")
correct_prediction = tf.equal(y, tf.argmax(probabilities,1,output_type=tf.int32))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

########## Train ##########
print("########## Start training ##########")
sess = tf.Session()
writer = tf.summary.FileWriter("./log", sess.graph)
init = tf.global_variables_initializer()
# init saver to save model
saver = tf.train.Saver()

# randomize dataset
indices = np.random.permutation(X_train.shape[0])

# start cross validation
avg_accuracy = 0.0
avg_loss = 0.0

if TAKE_CROSS_VALIDATION == True:
    for fold in range(1, CROSS_VALIDATION+1):
        print("########## Fold:", fold, "##########")
        # init weights
        sess.run(init)
        # split inputs into training set and validation set for each fold
        X_train_fold, y_train_fold, X_validate_fold, y_validate_fold = split_folds(indices, X_train, y_train, CROSS_VALIDATION, fold)
        print('validate data: ', X_validate_fold.shape)
        print('validate label: ', y_validate_fold.shape)
        print('train data: ', X_train_fold.shape)
        print('train label: ', y_train_fold.shape)

        winner_loss, winner_accuracy, epoch = train(X_train_fold, y_train_fold, X_validate_fold, y_validate_fold
                                , train_op, EPOCH_BOUND, EARLY_STOP_CHECK_EPOCH, BATCH_SIZE, testing=False)
        avg_loss += winner_loss
        avg_accuracy += winner_accuracy
        
        print("Epoch: ", epoch, " Loss: ", winner_loss, " Accuracy: ", winner_accuracy)
    avg_loss /= CROSS_VALIDATION
    avg_accuracy /=CROSS_VALIDATION
    
    print("average loss: ", avg_loss)
    print("average accuracy: ", avg_accuracy)

writer.close()


# In[4]:


########## Final Train ##########
print("########## Start training ##########")
sess.run(init)

for epoch in range(100):

        # randomize training set
        indices_training = np.random.permutation(X_train.shape[0])
        X_train, y_train = X_train[indices_training,:], y_train[indices_training]
        
        # split training set into multiple mini-batches and start training
        total_batches = int(X_train.shape[0] / BATCH_SIZE)
        for batch in range(total_batches):
            if batch == total_batches - 1:
                sess.run(train_op, feed_dict={x: X_train[batch*BATCH_SIZE:], 
                                               y: y_train[batch*BATCH_SIZE:]})
            else:
                sess.run(train_op, feed_dict={x: X_train[batch*BATCH_SIZE : (batch+1)*BATCH_SIZE], 
                                               y: y_train[batch*BATCH_SIZE : (batch+1)*BATCH_SIZE]})
        
pridiction = tf.argmax(probabilities,axis=1,output_type=tf.int32, name="pridiction")
pridict_output = sess.run(pridiction, feed_dict={x:X_test})

test_output=[['User-Item1-Item2','Preference']]
for idx in range(pridict_output.shape[0]):
    entry = str(int(userID[idx]))+'-'+str(int(item1[idx]))+'-'+str(int(item2[idx]))
    value = pridict_output[idx]
    test_output.append([entry,value])

print(test_output)
np.savetxt("output.csv", np.array(test_output, dtype=np.str), fmt='%s,%s', delimiter=",")

