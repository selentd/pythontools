'''
Created on 20.10.2015

@author: SELEN00R
'''
import unittest

import test_fetchdata
import test_indexdata

class Test(unittest.TestCase):
    pass

class PackageTestLoader(unittest.TestLoader):

    def loadTestsFromModule(self, module):
        packageSuite = unittest.TestSuite()
        packageSuite.addTest(test_fetchdata.suite())
        packageSuite.addTest(test_indexdata.suite())
        return packageSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(testLoader=PackageTestLoader(), testRunner=unittest.TextTestRunner, exit=False, verbosity=2)

