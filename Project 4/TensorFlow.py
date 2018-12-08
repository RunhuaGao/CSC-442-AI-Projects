import tensorflow as tf
import numpy as np
from demo import continuousIris

data = np.array([d[:-1] for d in continuousIris])
label = np.array([d[-1] for d in continuousIris])

# Define network's input, output, forward propagation function
x = tf.placeholder(tf.float32, shape=(None, 4))
y_ = tf.placeholder(tf.float32, shape=(None, 3))

w1 = tf.Variable(tf.random_normal([4, 2], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))

a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

#  Define loos function and back propagation function
loss = tf.reduce_mean(tf.square(y - y_))
train_step = tf.train.GradientDescentOptimizer(0.002).minimize(loss)

# session start
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    # initial weight matrix
    print("w1:\n", sess.run(w1))
    print("w2:\n", sess.run(w2))
    print("\n")

    # start training
    for i in range(150):
        sess.run(train_step, feed_dict={x: data[i:], y_: label[i:]})
        total_loss = sess.run(loss, feed_dict={x: data, y_: label})
        print("After %d training step(s), loss on all data is %g" % (i, total_loss))

    # print weight matrix after training
    print("\n")
    print("w1:\n", sess.run(w1))
    print("w2:\n", sess.run(w2))
