import unittest
from datetime import datetime
import main
import os

class TestDict(unittest.TestCase):

    def test_getDir(self):
        time = datetime.now()
        prefix = "json"

        targetDir = main.getDir(time, prefix)

        self.assertTrue(os.path.exists(targetDir))
