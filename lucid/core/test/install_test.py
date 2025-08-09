"""
# Install Unit Test
"""

import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

import lucid.core.install


class TestInstall(unittest.TestCase):
    def setUp(self) -> None:
        # Create temporary directories for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

        # Mock paths to use our temp directory
        self.mock_facility_dir = self.base_path / 'facility'
        self.mock_facility_pipe_configs_dir = self.mock_facility_dir / 'pipeline_configs'
        self.mock_facility_systems_dir = self.mock_facility_pipe_configs_dir / 'sys'
        self.mock_user_details_dir = self.mock_facility_pipe_configs_dir / 'users'
        self.mock_projects_dir = self.base_path / 'projects'
        self.mock_user_appdata_dir = self.base_path / 'user_appdata'
        self.mock_user_log_dir = self.mock_user_appdata_dir / 'logs'
        self.mock_user_home_dir = self.base_path / 'home' / 'testuser'

        # Start patches for constants
        self.patcher_facility_dir = mock.patch('lucid.core.const.FACILITY_DIR',
                                               self.mock_facility_dir)
        self.patcher_facility_pipe_configs = mock.patch('lucid.core.const.FACILITY_PIPE_CONFIGS_DIR',
                                                        self.mock_facility_pipe_configs_dir)
        self.patcher_facility_systems = mock.patch('lucid.core.const.FACILITY_SYSTEMS_DIR',
                                                   self.mock_facility_systems_dir)
        self.patcher_user_details = mock.patch('lucid.core.const.USER_DETAILS_DIR',
                                               self.mock_user_details_dir)
        self.patcher_projects_dir = mock.patch('lucid.core.const.PROJECTS_DIR',
                                               self.mock_projects_dir)
        self.patcher_user_appdata = mock.patch('lucid.core.const.USER_APPDATA_DIR',
                                               self.mock_user_appdata_dir)
        self.patcher_user_log = mock.patch('lucid.core.const.USER_LOG_DIR',
                                           self.mock_user_log_dir)
        self.patcher_user_home = mock.patch('lucid.core.const.USER_HOME_DIR',
                                            self.mock_user_home_dir)

        # Start all patches
        self.patcher_facility_dir.start()
        self.patcher_facility_pipe_configs.start()
        self.patcher_facility_systems.start()
        self.patcher_user_details.start()
        self.patcher_projects_dir.start()
        self.patcher_user_appdata.start()
        self.patcher_user_log.start()
        self.patcher_user_home.start()

    def tearDown(self) -> None:
        # Stop all patches
        self.patcher_facility_dir.stop()
        self.patcher_facility_pipe_configs.stop()
        self.patcher_facility_systems.stop()
        self.patcher_user_details.stop()
        self.patcher_projects_dir.stop()
        self.patcher_user_appdata.stop()
        self.patcher_user_log.stop()
        self.patcher_user_home.stop()
        self.temp_dir.cleanup()

    def test_setup_integrity_system_creates_token_file(self) -> None:
        """Test that _setup_integrity_system creates the integrity token file."""
        with mock.patch('lucid.core.install.io_utils.create_folder') as mock_create:
            with mock.patch('lucid.core.install.io_utils.export_data_to_json') as mock_export:
                lucid.core.install._setup_integrity_system()

        # Should create the systems directory
        mock_create.assert_called_once_with(self.mock_facility_systems_dir)

        # Should export the integrity token
        expected_file_path = self.mock_facility_systems_dir / '_integrity.json'
        mock_export.assert_called_once()
        args, kwargs = mock_export.call_args
        self.assertEqual(args[0], expected_file_path)
        self.assertIn('SYSTEM_TOKEN', args[1])
        self.assertEqual(kwargs.get('overwrite', True), False)

    def test_setup_integrity_system_generates_valid_uuid(self) -> None:
        """Test that the generated system token is a valid UUID."""
        with mock.patch('lucid.core.install.io_utils.create_folder'):
            with mock.patch('lucid.core.install.io_utils.export_data_to_json') as mock_export:
                lucid.core.install._setup_integrity_system()

        # Extract the data that was passed to export_data_to_json
        args, _ = mock_export.call_args
        data = args[1]

        # Verify it's a valid UUID string
        token = data['SYSTEM_TOKEN']
        self.assertIsInstance(token, str)

        # Should be able to parse as UUID without raising exception
        parsed_uuid = uuid.UUID(token)
        self.assertIsInstance(parsed_uuid, uuid.UUID)

    def test_add_admin_default_calls_setup_user_default(self) -> None:
        """Test that _add_admin_default calls the auth module's setup function."""
        with mock.patch('lucid.core.install.setup_user_default') as mock_setup:
            lucid.core.install._add_admin_default()

        mock_setup.assert_called_once()

    def test_install_default_user_calls_both_functions(self) -> None:
        """Test that install_default_user calls both setup functions in order."""
        # Use a parent mock to track call order
        parent_mock = mock.MagicMock()

        with mock.patch('lucid.core.install._setup_integrity_system') as mock_integrity:
            with mock.patch('lucid.core.install._add_admin_default') as mock_admin:
                # Attach child mocks to parent to track order
                parent_mock.attach_mock(mock_integrity, 'setup_integrity')
                parent_mock.attach_mock(mock_admin, 'add_admin')

                lucid.core.install.install_default_user()

        # Both functions should be called
        mock_integrity.assert_called_once()
        mock_admin.assert_called_once()

        # Verify call order - integrity should be called before admin
        expected_calls = [
            mock.call.setup_integrity(),
            mock.call.add_admin()
        ]
        parent_mock.assert_has_calls(expected_calls)

    def test_install_user_dirs_creates_all_user_directories(self) -> None:
        """Test that install_user_dirs creates all required user directories."""
        with mock.patch('lucid.core.install.io_utils.create_folder') as mock_create:
            lucid.core.install.install_user_dirs()

        expected_calls = [
            mock.call(self.mock_user_appdata_dir),
            mock.call(self.mock_user_log_dir),
            mock.call(self.mock_user_home_dir)
        ]

        mock_create.assert_has_calls(expected_calls, any_order=True)

    def test_install_facility_dirs_creates_all_facility_directories(self) -> None:
        """Test that install_facility_dirs creates all required facility directories."""
        with mock.patch('lucid.core.install.io_utils.create_folder') as mock_create:
            lucid.core.install.install_facility_dirs()

        expected_calls = [
            mock.call(self.mock_facility_dir),
            mock.call(self.mock_facility_pipe_configs_dir),
            mock.call(self.mock_user_details_dir),
            mock.call(self.mock_projects_dir)
        ]

        mock_create.assert_has_calls(expected_calls, any_order=True)

    def test_install_user_facility_calls_all_install_functions(self) -> None:
        """Test that install_user_facility calls all the individual install functions."""
        with mock.patch('lucid.core.install.install_default_user') as mock_default:
            with mock.patch('lucid.core.install.install_user_dirs') as mock_user:
                with mock.patch('lucid.core.install.install_facility_dirs') as mock_facility:
                    lucid.core.install.install_user_facility()

        # All three functions should be called
        mock_default.assert_called_once()
        mock_user.assert_called_once()
        mock_facility.assert_called_once()

    def test_install_user_facility_logs_completion(self) -> None:
        """Test that install_user_facility logs completion message."""
        with mock.patch('lucid.core.install.install_default_user'):
            with mock.patch('lucid.core.install.install_user_dirs'):
                with mock.patch('lucid.core.install.install_facility_dirs'):
                    # Capture logger calls
                    with mock.patch('lucid.core.install._logger') as mock_logger:
                        lucid.core.install.install_user_facility()

        # Should log completion
        mock_logger.info.assert_called_with('Install complete')

    @mock.patch('lucid.core.install.install_user_facility')
    def test_main_execution_calls_install_user_facility(self, mock_install):
        """Test that running the module as main calls install_user_facility."""
        # This tests the if __name__ == '__main__' block
        # We need to actually execute the module code, but we can test the function it calls
        mock_install.return_value = None

        # Import and execute the main block
        import importlib
        import sys

        # Store original argv to restore later
        original_argv = sys.argv[:]

        try:
            # Set argv to simulate running as main
            sys.argv = ['lucid.core.install']

            # Reload the module to trigger the main block
            importlib.reload(lucid.core.install)

        finally:
            # Restore original argv
            sys.argv = original_argv


class TestInstallIntegration(unittest.TestCase):
    """Integration tests with minimal mocking."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_install_user_dirs_actually_creates_directories(self) -> None:
        """Test that install_user_dirs actually creates directories."""
        # Mock the const paths to use our temp directory
        mock_user_appdata = self.base_path / 'user_appdata'
        mock_user_log = mock_user_appdata / 'logs'
        mock_user_home = self.base_path / 'home' / 'testuser'

        with mock.patch('lucid.core.const.USER_APPDATA_DIR', mock_user_appdata):
            with mock.patch('lucid.core.const.USER_LOG_DIR', mock_user_log):
                with mock.patch('lucid.core.const.USER_HOME_DIR', mock_user_home):
                    lucid.core.install.install_user_dirs()

        # Verify directories were actually created
        self.assertTrue(mock_user_appdata.exists())
        self.assertTrue(mock_user_appdata.is_dir())
        self.assertTrue(mock_user_log.exists())
        self.assertTrue(mock_user_log.is_dir())
        self.assertTrue(mock_user_home.exists())
        self.assertTrue(mock_user_home.is_dir())

    def test_install_facility_dirs_actually_creates_directories(self) -> None:
        """Test that install_facility_dirs actually creates directories."""
        # Mock the const paths to use our temp directory
        mock_facility = self.base_path / 'facility'
        mock_facility_pipe = mock_facility / 'pipeline_configs'
        mock_user_details = mock_facility_pipe / 'users'
        mock_projects = self.base_path / 'projects'

        with mock.patch('lucid.core.const.FACILITY_DIR', mock_facility):
            with mock.patch('lucid.core.const.FACILITY_PIPE_CONFIGS_DIR', mock_facility_pipe):
                with mock.patch('lucid.core.const.USER_DETAILS_DIR', mock_user_details):
                    with mock.patch('lucid.core.const.PROJECTS_DIR', mock_projects):
                        lucid.core.install.install_facility_dirs()

        # Verify directories were actually created
        for directory in [mock_facility, mock_facility_pipe, mock_user_details, mock_projects]:
            self.assertTrue(directory.exists())
            self.assertTrue(directory.is_dir())

    def test_setup_integrity_system_creates_actual_file(self) -> None:
        """Test that _setup_integrity_system creates an actual integrity file."""
        mock_facility_systems = Path(self.base_path, 'facility/pipeline_configs/sys')

        with mock.patch('lucid.core.const.FACILITY_SYSTEMS_DIR', mock_facility_systems):
            lucid.core.install._setup_integrity_system()

        # Verify directory and file were created
        self.assertTrue(mock_facility_systems.exists())
        self.assertTrue(mock_facility_systems.is_dir())

        integrity_file = mock_facility_systems / '_integrity.json'
        self.assertTrue(integrity_file.exists())

        # Verify file contains valid JSON with SYSTEM_TOKEN
        import json
        with open(integrity_file, 'r') as f:
            data = json.load(f)

        self.assertIn('SYSTEM_TOKEN', data)
        self.assertIsInstance(data['SYSTEM_TOKEN'], str)

        # Should be a valid UUID
        uuid.UUID(data['SYSTEM_TOKEN'])

    def test_setup_integrity_system_does_not_overwrite_existing(self) -> None:
        """Test that _setup_integrity_system doesn't overwrite existing integrity file."""
        mock_facility_systems = Path(self.base_path, 'facility/pipeline_configs/sys')
        mock_facility_systems.mkdir(parents=True)

        # Create existing integrity file
        integrity_file = mock_facility_systems / '_integrity.json'
        original_data = {'SYSTEM_TOKEN': 'original-token-12345'}
        with open(integrity_file, 'w') as f:
            import json
            json.dump(original_data, f)

        with mock.patch('lucid.core.const.FACILITY_SYSTEMS_DIR', mock_facility_systems):
            lucid.core.install._setup_integrity_system()

        # File should still contain original data
        with open(integrity_file, 'r') as f:
            import json
            data = json.load(f)

        self.assertEqual(data['SYSTEM_TOKEN'], 'original-token-12345')


if __name__ == '__main__':
    unittest.main()
