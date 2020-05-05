## -*- coding: utf-8 -*-
##
##  Jonathan Salwan - 2014-05-12 - ROPgadget tool
##
##  http://twitter.com/JonathanSalwan
##  http://shell-storm.org/project/ROPgadget/
##

import ropgadget.args
import ropgadget.binary
import ropgadget.core
import ropgadget.gadgets
import ropgadget.options
import ropgadget.rgutils
import ropgadget.updateAlert
import ropgadget.version
import ropgadget.loaders
import ropgadget.ropchain
import os

def main(bin_path, module_name, p):
    import sys
    from   ropgadget.args import Args
    from   ropgadget.core import Core
    from argparse import Namespace
    # sys.exit(0 if Core(Args().getArgs()).analyze() else 1)

    l = 0

    for j in bin_path:
        n = j.split('\\')
        n = n[len(n)-1]

        if len(n) > l:
            l = len(n)

    # p = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\"
    f = open(module_name + "_ROP_Gadgets.txt", "w")

    for b in bin_path:

        options = Namespace(
              all=False
            , badbytes=None
            , binary=b
            , callPreceded=False
            , checkUpdate=False
            , console=False
            , depth=10
            , dump=False
            , filter=None
            , memstr=None
            , multibr=False
            , noinstr=False
            , nojop=True
            , norop=False
            , nosys=True
            , offset=None
            , only=None
            , opcode=None
            , range='0x0-0x0'
            , rawArch=None
            , rawEndian=None
            , rawMode=None
            , re=None
            , ropchain=False
            , silent=True
            , string=None
            , thumb=False
            , version=False)

        print(b)

        c = Core(options)
        c.analyze()
        g = (c.gadgets())

        name = b.split('\\')
        name = name[len(name)-1]

        for i in g:
            s = str(name) + ("-" * (len(name) - l)) + " | " + str(hex(i['vaddr'])) + " | " + str(i['gadget']) + "\n"
            f.write(s)

    f.close()
    return module_name + "_ROP_Gadgets.txt"