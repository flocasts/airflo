#!/usr/bin/env python
from pyspark import SparkContext, SparkConf

import random


conf = SparkConf().setAppName("calculate_pyspark_example")
sc = SparkContext(conf=conf)
sc.setLogLevel('INFO')


class RandomFilter(object):

    def __init__(self, num_samples=100):
        self.num_samples = num_samples

    @staticmethod
    def inside(r):
        x, y = random.random(), random.random()
        return x * x + y * y < 1

    def run(self):
        return range(0, self.num_samples)


if __name__ == '__main__':
    result = RandomFilter(num_samples=100000).run()
    cnt_res = sc.parallelize(result).filter(RandomFilter.inside).count()
    print("Random count:", cnt_res)
