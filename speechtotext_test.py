import speechtotext
import openai

import unittest

from parameterized import parameterized
from unittest import mock
from unittest.mock import MagicMock

class MockResponse:

    def __init__(self, method):
        self.method = method


def mocked_requests_get(*args, **kwargs):
    return MockResponse('GET')

def mock_request_post(*args, **kwargs):
    return MockResponse('POST')


class AppTest(unittest.TestCase):

    def test_save_file_calls_save(self):
        uploaded_file = MagicMock()
        uploaded_file.filename = 'filename'
        
        speechtotext.save_file(uploaded_file)
        
        uploaded_file.save.assert_called_once_with('filename')

    def test_save_file_raises_value_error(self):
        uploaded_file = MagicMock()
        uploaded_file.filename = ''
        
        with self.assertRaises(ValueError) as e:
            speechtotext.save_file(uploaded_file)

    @mock.patch.object(__builtins__, 'open', autospec=True)
    @mock.patch.object(openai.Audio, 'transcribe', autospec=True)
    def test_transcribe(self, mock_transcribe, mock_open):
        expected_value = MagicMock()
        mock_transcribe.return_value = expected_value
        mock_open.return_value = MagicMock()

        actual_value = speechtotext.transcribe('filepath')

        mock_open.assert_called_once_with('filepath', 'rb')
        self.assertEqual(expected_value, actual_value)


if __name__ == '__main__':
    unittest.main()