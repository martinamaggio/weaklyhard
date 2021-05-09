from lib.wh_constraint import *


if __name__ == '__main__':

  num_sequence = 10000
  len_sequence = 15
  c_rm = RH_Constraint(2, 4)

  misses = [0] * len_sequence
  for i in range(num_sequence):
    seq = c_rm.gen_sequence(len_sequence)
    misses = list(map(lambda x, y: x + (1 if y == 0 else 0), misses, seq))

  empirical_miss_probability = list(map(lambda x: x/num_sequence, misses))
  print(empirical_miss_probability)
