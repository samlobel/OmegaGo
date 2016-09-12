from __future__ import print_function

import tensorflow as tf
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x,W):
  return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def conv2d_skip(x,W):
  return tf.nn.conv2d(x,W,strides=[1,2,2,1],padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')



x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None,10])  


W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x,[-1,28,28,1])

h_conv1 = tf.nn.relu(conv2d_skip(x_image, W_conv1) + b_conv1)
# h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d_skip(h_conv1, W_conv2) + b_conv2)
# h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_conv2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1,W_fc2) + b_fc2)


# cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(output), reduction_indices=[1]))
# mean_square = tf.reduce_mean(tf.reduce_sum((y_ - output)**2, reduction_indices=[1]))

# use_err = cross_entropy


# train_step = tf.train.GradientDescentOptimizer(0.1).minimize(use_err)



# correct_prediction = tf.equal(tf.argmax(output,1), tf.argmax(y_,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print("all compiled")

# for i in range(20000):
#   batch_xs, batch_ys = mnist.train.next_batch(100)
#   # if i%100==0:
#   sess.run(train_step, feed_dict={x:batch_xs, y_:batch_ys})
#   if i%50==0:
#     print(sess.run(accuracy, feed_dict={x:mnist.test.images, y_:mnist.test.labels}))



cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# init = tf.initialize_all_variables()
saver = tf.train.Saver()

sess = tf.Session()
# sess.run(init)
saver.restore(sess, 'saved_models/model_batch_1000.ckpt')
print("model restored")
# sess.run(tf.initialize_all_variables())
for i in range(5000):
  batch = mnist.train.next_batch(200)
  if i % 25 == 0:
    train_accuracy = sess.run(accuracy, feed_dict={
        x:batch[0], y_: batch[1]})
    # accuracy.eval(feed_dict={
    #     x:batch[0], y_: batch[1]})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  if i % 100 == 0:
    save_path = saver.save(sess, "./saved_models/model_batch_" + str(i) +".ckpt")
    print("Model saved in file: %s" % save_path)
  sess.run(train_step, feed_dict={x: batch[0], y_: batch[1]})

print("test accuracy %g"%sess.run(accuracy, feed_dict={
    x: mnist.test.images, y_: mnist.test.labels}))
