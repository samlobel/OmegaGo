import numpy as np
import tensorflow as tf

b1_4x4 = np.asarray(
  [[ 0, 0, 0, 0],
   [ 0, 0, 0, 0],
   [ 0, 0, 0, 0],
   [ 0, 0, 0, 0]]
)

b2_4x4 = np.asarray(
  [[ 0, 1,-1, 0],
   [ 1, 1,-1, 0],
   [-1,-1, -1, 0],
   [ 0, 0, 0, 0]]
)

b3_4x4 = np.asarray(
  [[ 1, 1, 1, 1],
   [ 1,-1,-1, 1],
   [ 1, 0,-1, 1],
   [ 1, 1, 1, 1]]
)

