import random
import time
from mrjob.job import MRJob


STEP = 10 ** 7
TASK_LIFETIME_S = 60 * 5

def avg(counts):
  return sum(count * i for i, count in enumerate(counts[1:])) / float(sum(counts))


class MRMonteCarlo(MRJob):
  def mapper(self, _, __):
    self.increment_counter('status', 'mappers_started', 1)
    bag = range(7) * 10
    counts = [0] * 8
    start = time.time()

    while time.time() - start < TASK_LIFETIME_S:
      for i in xrange(STEP):
        counts[len(set(random.sample(bag, 20)))] += 1

    yield 'counts', counts

  def reducer(self, key, values):
    counts = [sum(counts) for counts in zip(*values)]
    yield '%s rounds' % sum(counts), counts


if __name__ == '__main__':
  MRMonteCarlo.run()