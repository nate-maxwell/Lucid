"""
# Lucid Logger Unit Test
"""


import logging
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import lucid.core.logger


class TestLucidLogging(unittest.TestCase):
    def setUp(self) -> None:
        # Patch const.USER_LOG_DIR and const.USERNAME to use a temp directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_user_dir = Path(self.temp_dir.name)
        self.mock_username = 'testuser'

        self.patcher_user_dir = mock.patch('lucid.core.const.USER_LOG_DIR',
                                           self.mock_user_dir)
        self.patcher_username = mock.patch('lucid.core.const.USERNAME',
                                           self.mock_username)
        self.patcher_user_dir.start()
        self.patcher_username.start()

        # Clear previous handlers if any
        test_logger = logging.getLogger(lucid.core.logger.ROOT_LOGGER_NAME)
        test_logger.handlers.clear()

    def tearDown(self) -> None:
        self.patcher_user_dir.stop()
        self.patcher_username.stop()

        logger = logging.getLogger(lucid.core.logger.ROOT_LOGGER_NAME)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
        self.temp_dir.cleanup()

    def test_setup_root_logger_creates_file_handler(self) -> None:
        ret_code = lucid.core.logger.setup_root_logger()
        self.assertEqual(ret_code, 0)

        logger = logging.getLogger(lucid.core.logger.ROOT_LOGGER_NAME)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(any(
            isinstance(h, logging.handlers.RotatingFileHandler) for h in
            logger.handlers))

        # Send a log message
        logger.info('This is a test message.')

        # Ensure the log file was written to
        log_file = Path(self.mock_user_dir, f'{self.mock_username}.log')
        self.assertTrue(log_file.exists())

        contents = log_file.read_text()
        self.assertIn('This is a test message.', contents)

    def test_logger_is_singleton(self) -> None:
        lucid.core.logger.setup_root_logger()
        handler_count_1 = len(
            logging.getLogger(lucid.core.logger.ROOT_LOGGER_NAME).handlers)

        # Call again — should not add more handlers
        lucid.core.logger.setup_root_logger()
        handler_count_2 = len(
            logging.getLogger(lucid.core.logger.ROOT_LOGGER_NAME).handlers)

        self.assertEqual(handler_count_1, handler_count_2)


if __name__ == '__main__':
    unittest.main()
