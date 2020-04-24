# encoding: utf-8

"""
File: bloomredis.py
Author: Rock Johnson
"""
class SimpleHash:
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class RedisBloomFilter:
    def __init__(self, server, key):
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31]
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def __contains__(self, fp):
        ret = True

        for f in self.hashfunc:
            loc = f.hash(fp)
            ret = ret & self.server.getbit(self.key, loc)
        return ret

    def add(self, fp):
        for f in self.hashfunc:
            loc = f.hash(fp)
            self.server.setbit(self.key, loc, 1)