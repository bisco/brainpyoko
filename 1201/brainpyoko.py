#fineencoding: utf-8

from __future__ import print_function
import sys
import codecs

class brainpyoko():
    plus   = "+"
    minus  = "-"
    gt     = ">"
    lt     = "<"
    lb     = "["
    rb     = "]"
    comma  = ","
    period = "."
    #symbol_set = set([plus,minus,gt,lt,lb,rb,comma,period])

    def __init__(self,filename):
        with codecs.open(filename, "r", "utf-8") as f:
            self.raw_code = ("".join(f.readlines())).strip()
        self.iptr = 0
        self.dptr = 0
        self.data = [0]*100
        self.loopmap = {} 
        self.insts = []
        self.__parser()

    def __parser(self):
        self.__tokenizer()

    def __get_token(self, pos):
        is_same = lambda raw_code, pos, x: raw_code[pos:pos+len(x)] == x
        quasi_plus   = u"ﾋﾟｮｺ"
        quasi_minus  = u"ﾋﾟｮｺﾘ"
        quasi_gt     = u"ﾋﾟｮｯｺ"
        quasi_lt     = u"ﾋﾟｮ?!"
        quasi_lb     = u"ﾋﾟｮﾘｺ"
        quasi_rb     = u"ﾋﾟｮｺ-"
        quasi_comma  = u"ﾋﾟｮｺ?!"
        quasi_period = u"ﾋﾟｮｯｺﾘﾝ"

        if is_same(self.raw_code, pos, quasi_minus):
            return quasi_minus, brainpyoko.minus
        elif is_same(self.raw_code, pos, quasi_period):
            return quasi_period, brainpyoko.period
        elif is_same(self.raw_code, pos, quasi_gt):
            return quasi_gt, brainpyoko.gt
        elif is_same(self.raw_code, pos, quasi_lt):
            return quasi_lt, brainpyoko.lt
        elif is_same(self.raw_code, pos, quasi_lb):
            return quasi_lb, brainpyoko.lb
        elif is_same(self.raw_code, pos, quasi_rb):
            return quasi_rb, brainpyoko.rb
        elif is_same(self.raw_code, pos, quasi_plus):
            return quasi_plus, brainpyoko.plus
        elif self.raw_code[pos:pos+len(quasi_comma)] == quasi_comma:
            return quasi_comma, brainpyoko.comma
        else:
            return False, False

    def __tokenizer(self):
        pos = 0
        while pos < len(self.raw_code):
            token, symbol = self.__get_token(pos)
            if token is False:
                #print(pos,end="")
                #print(":",end="")
                #print(self.raw_code[pos])
                pos += 1
                continue
            self.insts.append(symbol)
            pos += len(token)
        #print("".join(self.insts))

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
    bp = brainpyoko(sys.argv[1])
    bp.run()
    print()

if __name__ == "__main__":
    main()
