# 493.py
A brute force attempt at Project Euler's problem #493 using an AWS Elastic MapReduce and mrjob. See https://projecteuler.net, https://github.com/Yelp/mrjob for more information. The problem goes as follows:

> 70 colored balls are placed in an urn, 10 for each of the seven rainbow colors.

> What is the expected number of distinct colors in 20 randomly picked balls?

> Give your answer with nine digits after the decimal point (a.bcdefghij).

While it's simple to write a quick Python script to simulate the problem, it will take around a trillion rounds to converge to sufficient precision to answer the problem successfully:

    import random
    
    def avg(counts):
      return sum(count * i for i, count in enumerate(counts[1:])) / float(sum(counts))
    
    i = 1
    bag = range(7) * 10
    counts = [0, 0, 0, 0, 0, 0, 0, 0]
    while True:
      counts[len(set(random.sample(bag, 20)))] += 1
      i -= 1
      if i == 0: 
        i = 1000000
        print '{:,.0f}'.format(sum(counts)), '%5.9f' % avg(counts), counts

As such, more computing power is necessary. Enter AWS's Elastic MapReduce. Just run `run.sh` with the the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables defined appropriately (as well as the SSH credentials stored in `~/.ssh/EMR.pem`, and a basic MapReduce of three nodes will be launched, designed to complete in just under an hour (since AWS bills by discrete hours).

Up the tasks as much as your wallet is willing to bear, and let it fly! Just don't forget to increase the size of the dummy `input.txt` file as well, which effectively controls the duration of your job since each mapper is designed to run for about 5 minutes.
