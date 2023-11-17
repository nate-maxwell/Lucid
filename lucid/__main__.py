import subprocess
from pathlib import Path


def main() -> None:
    launcher_path = Path(Path(__file__).parent, 'launcher')
    launcher_file = Path(launcher_path, 'lucid_launcher.bat')
    p = subprocess.Popen(launcher_file.as_posix(), cwd=launcher_path.as_posix())
    p.communicate()


if __name__ == '__main__':
    main()
