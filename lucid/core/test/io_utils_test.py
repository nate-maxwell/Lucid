"""
# IO Utils Unit Test
"""

import datetime
import io
import sys
import tempfile
import time
import unittest
from pathlib import Path

from lucid.core import io_utils


class TestIOUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_create_folder(self) -> None:
        test_path = self.base_path / 'new_folder'
        result = io_utils.create_folder(test_path)
        self.assertTrue(result.exists())
        self.assertTrue(result.is_dir())

    def test_create_dated_folder(self) -> None:
        dated_path = io_utils.create_dated_folder(self.base_path)
        self.assertTrue(dated_path.exists())
        self.assertTrue(dated_path.is_dir())

        expected_name = str(datetime.date.today())
        self.assertTrue(dated_path.name == expected_name)

    def test_list_folder_contents(self) -> None:
        test_file = self.base_path / 'file.txt'
        test_file.write_text('content')
        contents = io_utils.list_folder_contents(self.base_path)
        self.assertIn('file.txt', contents)

        contents_full = io_utils.list_folder_contents(self.base_path, full_path=True)
        self.assertIn(test_file, contents_full)

    def test_delete_folder(self) -> None:
        folder = self.base_path / 'todelete'
        io_utils.create_folder(folder)
        dummy_file = folder / 'file.txt'
        dummy_file.write_text('data')
        io_utils._CHECK_PATH = self.base_path
        io_utils.delete_folder(folder)
        self.assertFalse(folder.exists())

    def test_delete_file(self) -> None:
        file = self.base_path / 'file.txt'
        file.write_text('data')
        io_utils._CHECK_PATH = self.base_path
        io_utils.delete_file(file)
        self.assertFalse(file.exists())

    def test_delete_files_in_directory(self) -> None:
        io_utils._CHECK_PATH = self.base_path
        for i in range(3):
            (self.base_path / f'file_{i}.txt').write_text('x')
        io_utils.delete_files_in_directory(self.base_path)
        remaining = list(self.base_path.iterdir())
        self.assertEqual(remaining, [])

    def test_copy_folder_contents(self) -> None:
        source = self.base_path / 'source'
        dest = self.base_path / 'dest'
        io_utils.create_folder(source)
        (source / 'file.txt').write_text('hello')
        io_utils.copy_folder_contents(source, dest)
        self.assertTrue((dest / 'file.txt').exists())

    def test_export_import_json(self) -> None:
        data = {'a': 1, 'b': [1, 2, 3]}
        file_path = self.base_path / 'data.json'
        io_utils.export_data_to_json(file_path, data)
        self.assertTrue(file_path.exists())

        loaded = io_utils.import_data_from_json(file_path)
        self.assertEqual(data, loaded)

    def test_serialize_object_json(self) -> None:
        class Dummy:
            def __init__(self) -> None:
                self.path = Path('/a/b')
                self.number = 1
                self.nonsense = {1, 2}

        obj = Dummy()
        result = io_utils.serialize_object_json(obj)
        self.assertEqual(result['path'], '/a/b')
        self.assertEqual(result['number'], 1)
        self.assertIsInstance(result['nonsense'], str)

    def test_sort_path_list(self) -> None:
        paths = [Path('file2.txt'), Path('file10.txt'), Path('file1.txt')]
        sorted_paths = io_utils.sort_path_list(paths)
        self.assertEqual([p.name for p in sorted_paths],
                         ['file1.txt', 'file2.txt', 'file10.txt'])

    def test_convert_size(self) -> None:
        size, label = io_utils.convert_size(2048)
        self.assertEqual(label, 'KB')
        self.assertGreater(size, 1)

    def test_print_center_header(self) -> None:
        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer
        try:
            io_utils.print_center_header('Hello', '=')
        finally:
            sys.stdout = original_stdout

        output = buffer.getvalue()
        self.assertIn('Hello', output)
        self.assertTrue(output.strip().startswith('='))

    def test_progress_bar(self) -> None:
        buffer = io.StringIO()
        original_stderr = sys.stderr
        sys.stderr = buffer
        try:
            for _ in io_utils.ProgressBar(range(3)):
                time.sleep(0.01)
        finally:
            sys.stderr = original_stderr

        output = buffer.getvalue()
        self.assertIn('|', output)
        self.assertIn('%', output)


if __name__ == '__main__':
    unittest.main()
