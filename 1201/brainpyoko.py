#fineencode: utf-8

from __future__ import print_function
import sys

class brainpyoko():
    plus   = "+"
    minus  = "-"
    gt     = ">"
    lt     = "<"
    lb     = "["
    rb     = "]"
    comma  = ","
    period = "."
    token_set = set([plus,minus,gt,lt,lb,rb,comma,period])

    def __init__(self,filename):
        with open(filename) as f:
            self.raw_code = ("".join(f.readlines())).strip()
        self.iptr = 0
        self.dptr = 0
        self.data = [0]*100
        self.loopmap = {} 
        self.insts = []
        self.parser()

    def parser(self):
        self.tokenizer()

    def tokenizer(self):
        for i in self.raw_code:
            if i in brainpyoko.token_set:
                self.insts.append(i)

    def __gen_loopmap(self):
        stack = []
        for i, val in enumerate(self.insts):
            if val == brainpyoko.lb:
                stack.append(i)
            elif val == brainpyoko.rb:
                if len(stack) == 0:
                    print("parse error: right brackets exists more than left brackets")
                    sys.exit()
                lb_index = stack.pop()
                self.loopmap[i] = lb_index
                self.loopmap[lb_index] = i

        if len(stack) != 0:
            print("parse error: left brackets exists more than right brackets")
            sys.exit()


    def executor(self):
        self.__gen_loopmap()
        while self.iptr < len(self.insts):
            if self.insts[self.iptr] == brainpyoko.gt: # >
                self.dptr += 1
                if self.dptr >= len(self.data):
                    for i in range(len(self.data)):
                        self.data.append(0)
            elif self.insts[self.iptr] == brainpyoko.lt: # <
                self.dptr -= 1
                if self.dptr < 0:
                    print("data pointer underflow", self.iptr, self.insts, self.dptr, self.data)
            elif self.insts[self.iptr] == brainpyoko.plus: # +
                self.data[self.dptr] += 1
            elif self.insts[self.iptr] == brainpyoko.minus: # -
                self.data[self.dptr] -= 1
            elif self.insts[self.iptr] == brainpyoko.period: # .
                print(chr(self.data[self.dptr]), end="")
            elif self.insts[self.iptr] == brainpyoko.comma:  # ,
                self.data[self.dptr] = sys.stdin.read(1)
            elif self.insts[self.iptr] == brainpyoko.lb: # [
                if self.data[self.dptr] == 0:
                    self.iptr = self.loopmap[self.iptr]
            elif self.insts[self.iptr] == brainpyoko.rb: # ]
                if self.data[self.dptr] != 0:
                    self.iptr = self.loopmap[self.iptr]
            self.iptr += 1

    def run(self):
        self.executor()

def usage():
    print("usage: python brainpyoko.py <filename>")
    sys.exit()

def main():
    if len(sys.argv) != 2:
        usage()
    b = brainpyoko(sys.argv[1])
    b.run()
    print()

if __name__ == "__main__":
    main()
