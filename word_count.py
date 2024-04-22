# import gmpy2
from Pyro4 import expose
import random


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        text = self.read_input()
        lines = text.split('\n')
        step = len(lines) / len(self.workers)
        step = int(step)
        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            if i < len(self.workers) - 1:
                mapped.append(self.workers[i].mymap(lines[i * step: i * step + step]))
            else:
                mapped.append(self.workers[i].mymap(lines[i * step: len(lines)]))
        # reduce
        primes = self.myreduce(mapped)
        # output
        self.write_output(primes)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(lines):
        word_count = {}
        res_size = 0
        for line in lines:
            words = line.split()
            for word in words:
                word = word.strip().lower().strip('.,!?')
                if word:
                    word_count[word] = word_count.get(word, 0) + 1
                    res_size += 1
        word_count["."] = res_size
        return word_count

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = ""
        res_count = 0
        res = {}
        for x in mapped:
            for word, count in x.value.items():
                if word == '.':
                    res_count+=count
                res[word] = res.get(word, 0) + count
        print("merge done")
        output += 'size ' + str(res_count) + '\n'
        for word, count in res.items():
            output+= word +' : ' + str(count) + '\n'
        print("reduce done")
        return output

    def read_input(self):
        with open(self.input_file_name,'r') as f:
            text = f.read()
        return  text


    def write_output(self, output):
        with open(self.output_file_name, 'w') as file:
            file.write(str(output))

        print("output done")

