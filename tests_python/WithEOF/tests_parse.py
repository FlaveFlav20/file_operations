import file_operations_lib
import unittest
import os

path: str = "./tests_files/DDHC.txt"

def get_list(string: str) -> list:
    res: list = string.split("\n")
    if len(res) == 1 and res[0] == '':
        return []
    elif len(res) > 1 and res[-1] == '':
        res.pop()
    return res 

class TestWithEOFParse(unittest.TestCase):
    def test_parse_no_options(self):
        file = os.popen("cat " + path)
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path), ref)

    def test_parse_remove_empty_string(self):
        file = os.popen("sed '/^$/d' " + path)
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path, remove_empty_string=True), ref)

    def test_parse_keep_when_regex(self):
        file = os.popen("grep \"^La loi\" " + path)
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path, remove_empty_string=False, keep_when_regex=True, regex="^La loi.*"), ref)

    def test_parse_pass_when_regex(self):
        file = os.popen("grep -v \"^La loi\" " + path)
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path, remove_empty_string=False, pass_when_regex=True, regex="^La loi.*"), ref)
    
    def test_remove_empty_string_parse_keep_when_regex(self):
        file = os.popen("sed '/^$/d' " + path + " | grep \"^La loi\" ")
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path, remove_empty_string=True, keep_when_regex=True, regex="^La loi.*"), ref)

    def test_parse_pass_when_regex(self):
        file = os.popen("sed '/^$/d' " + path + " | grep -v \"^La loi\" ")
        res: str= file.read()
        file.close()
        ref: list = get_list(res)
        self.assertEqual(file_operations_lib.WithEOL.parse(file=path, remove_empty_string=True, pass_when_regex=True, regex="^La loi.*"), ref)

if __name__ == '__main__':
    unittest.main()