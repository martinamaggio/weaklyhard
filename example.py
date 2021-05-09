from lib.wh_constraint import *


if __name__ == '__main__':

  # example of library usage
  # generating 10 random sequences according to one constraint (am: 3, 8)
  # with 25 deadlines (sequence length 25)
  # and checking if the sequence satisfies the other constraints
  num_sequence = 10
  len_sequence = 25

  # c_rm: cannot have more than 2 consecutive missed deadlines
  # c_am: cannot have more than 3 misses in 8 deadline window
  # c_ah: must have 4 or more hits in any 8 deadline window
  # c_rh: must have 3 or more consecutive hits in any 6 deadline window
  # c_r2: at most 2 consecutive misses, followed by (4-misses) hits
  #       with any hits in between (e.g., 0011 11 0111 1 0011 111)
  c_rm = RM_Constraint(2)
  c_am = AM_Constraint(3, 8)
  c_ah = AH_Constraint(4, 8)
  c_rh = RH_Constraint(3, 6)
  c_r2 = R2_Constraint(2, 4)

  for i in range(num_sequence):  # num_sequence attempts

    sequence = c_am.gen_sequence(len_sequence)

    correct_rm = c_rm.check_sequence(sequence)
    correct_am = c_am.check_sequence(sequence)
    correct_ah = c_ah.check_sequence(sequence)
    correct_rh = c_rh.check_sequence(sequence)
    correct_r2 = c_r2.check_sequence(sequence)

    correct = (correct_rm, correct_am, correct_ah, correct_rh, correct_r2)
    print(correct, sequence)
