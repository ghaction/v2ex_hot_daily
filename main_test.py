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

    @mock.patch("io.open")
    def test_saveJsonData(self, mock_open):
        data = []
        json_file = "./data/json/1991/01/01.json"
        main.save_json_data(data, json_file)
        mock_open.assert_called_once_with(json_file, 'w');

    @mock.patch("codecs.open")
    def test_saveMdData(self, mock_open):
        data = []
        dateStr = '1991-10-10 23:40:00'
        time = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

        md_file = "./data/md/1991/01/01.md"
        main.save_md_data(data, time, md_file)
        mock_open.assert_called_once_with(md_file, 'w', "utf-8");

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_getHotList(self, mock_get):
        retList = main.get_hot_list()

        self.assertTrue(len(retList) == 34)

    @mock.patch("requests.get", side_effect=mocked_requests_get_failed)
    def test_getHotListFailed(self, mock_get):
        retList = main.get_hot_list()
        self.assertTrue(len(retList) == 0)

    @mock.patch("main.get_hot_list")
    @mock.patch("main.getDir")
    @mock.patch("main.save_json_data")
    @mock.patch("main.save_md_data")
    def test_run_failed(self, mock_save_md_data, mock_save_json_data, mock_getDir, mock_get_hot_list):
        mock_get_hot_list.return_value = []
        mock_getDir.return_value = "./data/md/1991/01/"
        
        main.run()
        mock_save_md_data.assert_not_called()
        mock_save_json_data.assert_not_called()
        mock_getDir.assert_not_called()
        mock_get_hot_list.assert_called_once()
    
    @mock.patch("main.get_hot_list")
    @mock.patch("main.getDir")
    @mock.patch("main.save_json_data")
    @mock.patch("main.save_md_data")
    def test_run_succ(self, mock_save_md_data, mock_save_json_data, mock_getDir, mock_get_hot_list):
        mock_get_hot_list.return_value = [
            {
                "url": "https://www.v2ex.com/t/485555#reply158",
                "title": "石锤 github 买 star 行为",
                "replyNum": "158",
                "imgsrc": "//cdn.v2ex.com/gravatar/e21e7df9e540facf2c166961b73cbbbe?s=48&d=retro"
            }
        ]
        mock_getDir.return_value = "./data/md/1991/01/"
        
        main.run()
        mock_save_md_data.assert_called_once()
        mock_save_json_data.assert_called_once()
        self.assertEqual(2, mock_getDir.call_count)
        mock_get_hot_list.assert_called_once()

if __name__ == '__main__':
    unittest.main()
