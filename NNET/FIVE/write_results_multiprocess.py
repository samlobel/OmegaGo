import json
import numpy as np

import sys
import os

# from Queue import Queue
import time
from multiprocessing import Process, Queue
# from threading import Thread

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.'))

from go_util import util









def random_board_iterator():
  with open('./random_boards.txt') as f:
    while True:
      to_yield = f.readline().strip()
      if to_yield == '':
        break
      try:
        to_yield =  json.loads(to_yield)
        yield to_yield
      except Exception:
        print "fail on to_yield=" + str(to_yield)
  print 'exit iterator'

def board_to_result_obj(board, games_to_average=5):
  """
  There's some trickiness here. Because, it's not actually about who wins,
  its about whether YOU win. And for the purposes of the policy network, YOU
  are the person who just moved. Because, you look ahead one move and you say,
  which has the best value for ME, the person before that board? So,
  if the next person to go is black, it's the value for WHITE. Meaning that 
  if determine_winner gives you 1, and it's white's (-1) turn now, that is good.
  
  white_to_go_value : chance BLACK wins given that white is to go next.
  -- should just be determine_winner().
  black_to_go_value : chance WHITE wins given that black is to go next.
  -- should be -1 * determine_winner(). Because if black wins, that's bad.

  # And when I train on it, I'll do black_to_go_average_results on a board saying
  # that black is ME and white is YOU, etc.

  """
  np_board = np.asarray(board)
  black_to_go_total_value = 0.0
  white_to_go_total_value = 0.0
  for i in range(games_to_average):
    black_to_go_total_value += (-1.0 * util.determine_random_winner_of_board(np_board, 1, []))
    white_to_go_total_value += util.determine_random_winner_of_board(np_board, -1, [])

  black_to_go_average_value = (black_to_go_total_value + 0.0) / games_to_average
  white_to_go_average_value = (white_to_go_total_value + 0.0) / games_to_average

  return {
    'board' : board,
    'black_to_go_average_value' : black_to_go_average_value,
    'white_to_go_average_value' : white_to_go_average_value
  }

def read_boards_write_results(write_path):
  i = 0
  with open(write_path, 'a') as f_out:
    for board in random_board_iterator():
      i += 1
      if i % 100 == 0:
        print 'finished board: ' + str(i)
      # board_np = np.asarray(board, dtype=np.float32)
      result_obj = board_to_result_obj(board)
      json_result = json.dumps(result_obj)
      f_out.write(json_result)
      f_out.write('\n')
  print 'done with writing'


# Q_in = Queue()
# Q_out = Queue()

# def worker():
#   board = Q.get()
#   result_obj = board_to_result_obj(board)


# BOARD_QUEUE = Queue(maxsize=100)

def worker_loader(b_queue):
  i = 0
  filename_in = './random_boards.txt'
  with open(filename_in, 'r') as f_in:
    while True:
      i += 1
      line = f_in.readline()
      line = line.strip()
      if line == '':
        print 'END OF FILE'
        break
      board_obj = json.loads(line)
      b_queue.put(board_obj)
      if i % 100 == 0:
        print "read in " + str(i)
      

# BOARD_RESULT_QUEUE = Queue(maxsize=100)

def worker_transform(b_queue, r_queue):
  while True:
    try:
      board_obj = b_queue.get(block=True, timeout=10)
      result_obj = board_to_result_obj(board_obj)
      r_queue.put(result_obj)
    except Exception:
      print 'exception in writer!'
      break

def worker_writer(r_queue):
  filename_out = './random_board_results_from_queue.txt'
  i = 0
  time_now = time.time()
  with open(filename_out, 'w', buffering=1) as f_out:
    while True:
      try:
        i += 1
        result_obj = r_queue.get(block=True, timeout=10)
        json_result = json.dumps(result_obj)
        f_out.write(json_result)
        f_out.write('\n')
        if i % 100 == 0:
          print "wrote out " + str(i)
        # if i % 200 == 0:
          print "DONE. took " + str(time.time() - time_now) + " time"
      except Exception:
        print 'exception in writer!'
        break





"""
I should make something for processing, which is the same as threading but BETTER.

"""

# def test_1(q):
#   with open('samalamalam.txt','a') as f:
#     f.write(q['1'])
#     f.write('\n')
#     f.write(q['2'])
#     f.write('\n')
#     f.write(q['3'])
#   print 'complete'

# def test_1(q_in, q_out):
#   while True:
#     elem = q_in.get(block=True, timeout=10)
#     neg = elem * -1
#     q_out.put(neg)
#     time.sleep(0.1)


# def queue_loader(q_in):
#   i = 0
#   while True:
#     q_in.put(i)
#     i += 1

# def queue_unloader(q_out):
#   while True:
#     elem = q_out.get(block=True, timeout=10)
#     print "elem out: "
#     print elem


if __name__ == '__main__':
  print 'starting'
  BOARD_QUEUE = Queue(maxsize=100)
  BOARD_RESULT_QUEUE = Queue(maxsize=100)
  NUM_WORKERS = sys.argv[1]
  if NUM_WORKERS:
    NUM_WORKERS = int(NUM_WORKERS)
  else:
    NUM_WORKERS = 4
  # NUM_WORKERS = 1
  print 'num workers: ' + str(NUM_WORKERS)
  proc_in = Process(target=worker_loader, args=[BOARD_QUEUE])
  proc_in.start()
  proc_out = Process(target=worker_writer, args=[BOARD_RESULT_QUEUE])
  proc_out.start()
  for i in range(NUM_WORKERS):
    proc_transform = Process(target=worker_transform, args=[BOARD_QUEUE,BOARD_RESULT_QUEUE])
    proc_transform.start()
    print "process kicked off: " + str(i)
  print "processes kicked off"












   






# if __name__ == '__main__':
  # print 'read_boards: '
  # read_boards_write_results('./random_board_results.txt')
  # print 'done!'

  # NUM_TRANSFORM_THREADS = 4

  # print 'read boards:'
  # T_read = Thread(target=worker_loader)
  # T_read.daemon = True
  # T_read.start()
  # T_write = Thread(target=worker_writer)
  # T_write.daemon = True
  # T_write.start()
  # for i in range(NUM_TRANSFORM_THREADS):
  #   T_write = Thread(target=worker_transform)
  #   T_write.daemon = True
  #   T_write.start()
  #   print 'thread ' + str(i) + ' kicked off.'

  # print 'threads kicked off.'
  # BOARD_QUEUE.join()
  # BOARD_RESULT_QUEUE.join()

  # print 'done'


