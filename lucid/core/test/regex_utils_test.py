"""
# Regex Utils Unit Test
"""


import unittest

import lucid.core.regex_utils


class TestRegexUtils(unittest.TestCase):
    def test_get_file_version_number(self) -> None:
        # Valid versioned files
        self.assertEqual(lucid.core.regex_utils.get_file_version_number('GhostA_anim_v001.ma'), '001')
        self.assertEqual(lucid.core.regex_utils.get_file_version_number('Some_asset_v1234.mb'), '1234')
        self.assertEqual(lucid.core.regex_utils.get_file_version_number('thing_v000.txt'), '000')

        # No version pattern
        self.assertIsNone(lucid.core.regex_utils.get_file_version_number('no_version_here.ma'))
        self.assertIsNone(lucid.core.regex_utils.get_file_version_number('thing_v.ma'))  # malformed version
        self.assertIsNone(lucid.core.regex_utils.get_file_version_number('v123.ma'))  # missing underscore
        self.assertIsNone(lucid.core.regex_utils.get_file_version_number('thing_v123'))  # missing extension

    def test_is_path_like(self) -> None:
        # Windows drive-letter paths
        self.assertTrue(lucid.core.regex_utils.is_path_like('C:\\project\\scene.ma'))
        self.assertTrue(lucid.core.regex_utils.is_path_like('D:/assets/character.mb'))

        # UNC path
        self.assertTrue(lucid.core.regex_utils.is_path_like('\\\\server\\share\\file.txt'))

        # Relative paths
        self.assertTrue(lucid.core.regex_utils.is_path_like('.\\temp\\test.txt'))
        self.assertTrue(lucid.core.regex_utils.is_path_like('..\\archive\\shot.ma'))

        # Slash-based paths
        self.assertTrue(lucid.core.regex_utils.is_path_like('folder/file.txt'))
        self.assertTrue(lucid.core.regex_utils.is_path_like('a\\b\\c'))

        # File with extension (no path separators)
        self.assertTrue(lucid.core.regex_utils.is_path_like('myfile.jpg'))
        self.assertTrue(lucid.core.regex_utils.is_path_like('something.ma'))

        # False cases
        self.assertFalse(lucid.core.regex_utils.is_path_like('notapath'))
        self.assertFalse(lucid.core.regex_utils.is_path_like('this is just text'))
        self.assertFalse(lucid.core.regex_utils.is_path_like('note'))
        self.assertFalse(lucid.core.regex_utils.is_path_like('file.'))  # invalid extension
        self.assertFalse(lucid.core.regex_utils.is_path_like(''))  # empty string
        self.assertFalse(lucid.core.regex_utils.is_path_like(123))  # type: ignore

    def test_pascale_to_snake(self) -> None:
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake('MyClassName'), 'my_class_name')
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake('Version3File'), 'version3_file')
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake('XMLHttpRequest'), 'xml_http_request')
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake('Already_Snake'), 'already__snake')  # handles underscore
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake('lowercase'), 'lowercase')  # stays the same
        self.assertEqual(lucid.core.regex_utils.pascale_to_snake(''), '')  # empty string


if __name__ == '__main__':
    unittest.main()
