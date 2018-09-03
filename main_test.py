import unittest
from datetime import datetime
import main
import os
import mock

def mocked_requests_get(*args, **kwargs):

    class MockedResponse:
        def __init__(self, response_text, status_code):
            self.text = response_text
            self.status_code = status_code
    

    data = ""
    with open("./test.html", "r") as testFile:
        data = testFile.read()

    if args[0] == "https://www.v2ex.com/?tab=hot":
        return MockedResponse(data, 200)


def mocked_requests_get_failed(*args, **kwargs):
    class MockedResponse:
        def __init__(self, response_text, status_code):
            self.text = response_text
            self.status_code = status_code
    
    if args[0] == "https://www.v2ex.com/?tab=hot":
        return MockedResponse('', 500)

class TestDict(unittest.TestCase):

    @mock.patch("os.makedirs")
    def test_getDir(self, mock_makedirs):
        dateStr = '1991-10-10 23:40:00'
        time = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        prefix = "json"

        targetDir = main.getDir(time, prefix)
        mock_makedirs.assert_called_once_with(targetDir)


    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_getHotList(self, mock_get):
        retList = main.get_hot_list()

        self.assertTrue(len(retList) == 34)

    @mock.patch("requests.get", side_effect=mocked_requests_get_failed)
    def test_getHotListFailed(self, mock_get):
        retList = main.get_hot_list()
        self.assertTrue(len(retList) == 0)


if __name__ == '__main__':
    unittest.main()
