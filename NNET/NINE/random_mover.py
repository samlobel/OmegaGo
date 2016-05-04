from __future__ import print_function

import tensorflow as tf
import numpy as np
import random

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.'))

from NNET.interface import GoBot

from go_util import util

from copy import deepcopy as copy


class Random_Mover(GoBot):
  def __init__(self):
    GoBot.__init__(self)
    self.board_shape = (9,9)

  def get_best_move(self, board_matrix, previous_board, current_turn):
    valid_moves = list(util.output_all_valid_moves(board_matrix, previous_board, current_turn))
    valid_moves.append(None)
    valid_move = random.choice(list(valid_moves))
    return valid_move




