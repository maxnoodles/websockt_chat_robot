import time
import unittest

from const import CONST


class MyTestCase(unittest.TestCase):
    def test_get_mag_type(self):
        msg_type = 'imag'
        # content = [{"url": '21321'}]
        content = '213213'
        result = self.get_mag_type(content)
        self.assertEqual(result, msg_type)

    def get_mag_type(self, msg_content, msg_type='text'):
        if msg_content and isinstance(msg_content, list):
            if isinstance(msg_content[0], dict):
                if 'url' in msg_content[0].keys():
                    msg_type = 'image'
        return msg_type


if __name__ == '__main__':
    unittest.main()

