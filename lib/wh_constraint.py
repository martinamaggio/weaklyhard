import random
from itertools import groupby


class WH_Constraint:

  # this defines a weakly hard constraint
  # the type of constraint is specified by the subclass
  def __init__(self, x: int, w: int = 0, mp: float = 0.5):
    self.x = x    # number of events
    self.w = w    # window length
    self.mp = mp  # probability of missing a deadline if possible

  # returns a list of length size containing zeroes and ones
  # must be implemented in the subclass
  def gen_sequence(self, size):
    pass

  # returns true if the sequence satisfies the constraint
  # must be implemented in the subclasses
  def check_sequence(self, sequence):
    pass


# consecutive deadline misses constraint
# the number of consecutive deadline misses is
# at most self.x
class RM_Constraint(WH_Constraint):

  def gen_sequence(self, size: int):
    sequence = list()
    for p in range(size):
      # look at the last self.x values in the sequence reversed
      # and find the first hit (number of misses at the end)
      try:
        misses = sequence[:-self.x-1:-1].index(1)
      # the exception is raised when:
      # a) there is no 1 in the list above (too many misses)
      # b) the list is empty (initial state)
      except ValueError:
        misses = len(sequence[:-self.x-1:-1])
      if misses < self.x and random.uniform(0, 1) < self.mp:
        sequence.append(0)
      else:
        sequence.append(1)
    return sequence

  def check_sequence(self, sequence):
    len_g_misses = [len(list(g)) for k, g in groupby(sequence, lambda x: x == 0) if k]
    return max(len_g_misses) <= self.x


# any deadline misses in a window constraint
# i.e., in any window of self.w jobs there are
# at most self.x misses
class AM_Constraint(WH_Constraint):

  def __init__(self, x: int, w: int, mp: float = 0.5):
    super().__init__(x, w, mp)
    if self.x > self.w:
      raise Exception("<AM_Constraint> window must at least be equal to number of misses")

  def gen_sequence(self, size: int):
    sequence = list()
    for i in range(size):
      window = sequence[max(i-self.w+1, 0):i]
      misses = window.count(0)
      if misses < self.x and random.uniform(0, 1) < self.mp:
        sequence.append(0)
      else:
        sequence.append(1)
    return sequence

  def check_sequence(self, sequence):
    for i in range(len(sequence) - self.w):
      window = sequence[i:i + self.w]
      misses = window.count(0)
      if misses > self.x:
        return False
    return True


# any deadline hits in a window constraint
# i.e., in any window of self.w jobs there are
# at least self.x hits
class AH_Constraint(WH_Constraint):

  def __init__(self, x: int, w: int, mp: float = 0.5):
    super().__init__(x, w, mp)
    if self.x > self.w:
      raise Exception("<AH_Constraint> window must at least be equal to number of misses")

  def gen_sequence(self, size: int):
    sequence = list()
    for i in range(size):
      window = sequence[max(i-self.w+1, 0):i]
      hits = window.count(1)
      if hits >= self.x and random.uniform(0, 1) < self.mp:
        sequence.append(0)
      else:
        sequence.append(1)
    return sequence

  def check_sequence(self, sequence):
    for i in range(len(sequence) - self.w):
      window = sequence[i:i + self.w]
      hits = window.count(1)
      if hits < self.x:
        return False
    return True


# consecutive deadline hits constraint
# i.e., in any window of self.w jobs there are
# at least self.x _consecutive_ hits
class RH_Constraint(WH_Constraint):

  def __init__(self, x: int, w: int, mp: float = 0.5):
    super().__init__(x, w, mp)
    if self.x > self.w:
      raise Exception("<RH_Constraint> window must at least be equal to number of misses")

  def gen_sequence(self, size: int):
    sequence = list()
    # speed up: if 2x > w then all ones
    if 2*self.x > self.w:
      for i in range(size):
        sequence.append(1)
      return sequence

    # otherwise let's try to add a zero and check if possible
    for i in range(size):
      window = sequence[max(i - self.w + 1, 0):i]
      window.append(0)  # let's test a zero
      for j in range(self.x):  # followed by x ones
        window.append(1)
      if self.check_sequence(window) and random.uniform(0, 1) < self.mp:
        sequence.append(0)
      else:
        sequence.append(1)
    return sequence

  def check_sequence(self, sequence):
    for i in range(len(sequence) - self.w):
      window = sequence[i:i + self.w]
      len_g_hits = [len(list(g)) for k, g in groupby(window, lambda x: x == 1) if k]
      if max(len_g_hits) < self.x:
        return False
    return True


# double row constraint: hits then misses from
#   Nils Vreman, Anton Cervin, Martina Maggio
#   "Stability and performance analysis of control
#   systems subject to bursts of deadline misses"
# presented at ECRTS 2021
# at most self.x misses, followed by self.w - misses hits
# with any sequence of hits in between
class R2_Constraint(WH_Constraint):

  def __init__(self, x: int, w: int, mp: float = 0.5):
    super().__init__(x, w, mp)
    if self.x > self.w:
      raise Exception("<R2_Constraint> window must at least be equal to number of misses")

  def gen_sequence(self, size: int):
    sequence = list()
    while len(sequence) < size:
      if random.uniform(0, 1) >= self.mp:
        sequence.append(1)  # wanted a hit anyway
      else:
        num_misses = 1
        while num_misses < self.x and random.uniform(0, 1) < self.mp:
          num_misses += 1
        num_hits = self.w - num_misses

        for i in range(num_misses):
          sequence.append(0)
        for i in range(num_hits):
          sequence.append(1)
    return sequence[0:size]  # cut to the desired size

  def check_sequence(self, sequence):
    lm = [len(list(g)) if k else 0 for k, g in groupby(sequence, lambda x: x == 0)]
    lh = [len(list(g)) if k else 0 for k, g in groupby(sequence, lambda x: x == 1)]
    groups = len(lm)  # number of unique groups

    # the last one could be misses (avoid checking that)
    # and the last hits may not be complete (sequence cut)
    for j in range(groups-1):
      if 0 < lm[j] <= self.x:
        if lh[j+1] < self.w - lm[j] and j+1 is not groups-1:
          return False
    # if we pass the check above
    # check that we don't have more than self.x consecutive misses
    return all(map(lambda x: x <= self.x, lm))
