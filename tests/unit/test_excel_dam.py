'''
Created on Nov 27, 2011

@author: ppa
'''
import unittest

import os
import tempfile
from shutil import rmtree
from ultrafinance.model import Tick, Quote
from ultrafinance.dam.excelDAM import ExcelDAM

class testExcelDAM(unittest.TestCase):

    def setUp(self):
        self.targetPath = tempfile.mkdtemp()
        self.symbol = 'ebay'

    def tearDown(self):
        rmtree(self.targetPath)

    def testWriteExcel(self):
        writeDam = ExcelDAM()
        writeDam.setDir(self.targetPath)
        writeDam.setSymbol(self.symbol)

        for f in [writeDam.targetPath(ExcelDAM.QUOTE), writeDam.targetPath(ExcelDAM.TICK)]:
            if os.path.exists(f):
                os.remove(f)

        quote1 = Quote('1320676200', '32.58', '32.58', '32.57', '32.57', '65212', None)
        quote2 = Quote('1320676201', '32.59', '32.59', '32.58', '32.58', '65213', None)
        tick1 = Tick('1320676200', '32.58', '32.58', '32.57', '32.57', '65212')
        tick2 = Tick('1320676201', '32.59', '32.59', '32.58', '32.58', '65213')
        writeDam.writeQuotes([quote1, quote2])
        writeDam.writeTicks([tick1, tick2])

    def testReadExcel(self):
        self.testWriteExcel()
        readDam = ExcelDAM()
        readDam.setDir(self.targetPath)
        readDam.setSymbol(self.symbol)

