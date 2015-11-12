#fineencode: utf-8

from __future__ import print_function
import sys

def brainpyoko(f):
    insts = ("".join(f.readlines())).strip()
    iptr = 0
    dptr = 0
    data = [0]*100
    while iptr < len(insts):
        if insts[iptr] == ">":
            dptr += 1
            if dptr >= len(data):
                data.append(0)
        elif insts[iptr] == "<":
            dptr -= 1
            if dptr < 0:
                print("data pointer underflow", iptr, insts, dptr, data)
        elif insts[iptr] == "+":
            data[dptr] += 1
        elif insts[iptr] == "-":
            data[dptr] -= 1
        elif insts[iptr] == ".":
            print(chr(data[dptr]), end="")
        elif insts[iptr] == ",":
            data[dptr] = sys.stdin.read(1)
        elif insts[iptr] == "[":
            if data[dptr] == 0:
                iptr = insts[iptr:].find("]")
        elif insts[iptr] == "]":
            if data[dptr] != 0:
                iptr -= (insts[:iptr+1][::-1]).find("[")
        iptr += 1

def usage():
    print("usage: python brainpyoko.py <filename>")
    sys.exit()

def main():
    if len(sys.argv) != 2:
        usage()
    with open(sys.argv[1]) as f:
        brainpyoko(f)

if __name__ == "__main__":
    main()
