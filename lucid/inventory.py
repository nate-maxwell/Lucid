"""
# Tool inventory and manifest handling

* Description:

    This module creates a json snapshot of the pipeline and current tools
    for updating deployed snapshots or versions of the pipeline.

    This file is responsible for creating/updating
    lucid.loader.pipeline_manifest.json.

* Update History:

    `2023-11-23` - Init
"""


from pathlib import Path
from typing import Optional

import lucid.constants
import lucid.io_utils
import lucid.debug


def get_imported_files(file: Path) -> list[str]:
    """
    Gets imported lucid files in a given file.

    Args:
        file(Path): The path to the file to get the imports of.

    Returns:
        list[str]: A list of the string namespaces of the imported files.
    """
    imported_files = []
    with open(file, 'r') as f:
        in_doc_string = False
        for line in f:
            if '"""' in line:
                in_doc_string = not in_doc_string
            if not in_doc_string:

                # from x import y
                if 'from ' in line and 'import ' in line and 'lucid' in line:
                    import_file = line.replace('\n', '').split(' import')[0].split('from ')[-1]
                    imported_files.append(import_file)

                # import x
                elif 'import ' in line and 'lucid' in line:
                    import_file = line.replace('\n', '').split('import ')[-1]
                    imported_files.append(import_file)

    return imported_files


def scan_files(directory: Path, structure: Optional[dict] = None) -> dict:
    """
    Recursively goes through the project python files and creates a dictionary
    of file names to import namespaces of project files that are imported
    into the currently scanned file.

    Args:
        directory(Path): The path to the current file/folder being scanned.

        structure(dict): The file: import record so far. This arg should not
        be filled, as it is autofilled in the recursive search.

    Returns:
        dict: An updated file: import record, also containing the date the file
        was inventoried.
    """
    if structure is None:
        structure = {}

    contents = lucid.io_utils.list_folder_contents(directory, True)
    for f in contents:
        is_init = False
        if f.suffix == '.py':
            if f.stem == '__init__':
                split_file_name = f.parent.as_posix().split(f'{lucid.constants.LUCID_REPO.as_posix()}/')[-1]
                is_init = True
            else:
                split_file_name = f.as_posix().split(f'{lucid.constants.LUCID_REPO.as_posix()}/')[-1]

            # Converts D:/git/lucid.lucid.maya.tool_name.py -> lucid.maya.tool_name
            # Converts D:/git/lucid.lucid.maya.__init__.py -> lucid.maya
            namespace = split_file_name.replace('/', '.').replace('.py', '')
            structure[namespace] = {
                'date-time': f'{lucid.io_utils.get_date()}-{lucid.io_utils.get_time()}',
                'imports': get_imported_files(f),
                '__init__': is_init
            }
        elif f.is_dir():
            scan_files(f, structure)

    return structure


def _combine_lists(a: list, b: list) -> list:
    """
    Combines two lists of unique elements together into one list of unique elements.

    Returns:
        list: The combined list, accounting for overlapping elements.
    """
    diff = set(a) - set(b)
    return list(diff) + b


def export_manifest():
    """Exports the manifest json to lucid project folder."""
    manifest_path = Path(lucid.constants.LUCID_PATH, 'pipeline_manifest.json')
    data = scan_files(lucid.constants.LUCID_PATH)

    # make imports a list of unique elements
    for k in data.keys():
        data[k]['imports'] = list(set(data[k]['imports']))

    lucid.io_utils.export_data_to_json(manifest_path, data, True)


def get_all_dependencies(module_namespace: str) -> list[str]:
    """
    Recursively get all imports of the imports of a file,
    collecting all lucid python files that make up a lucid file.

    This function traverses lucid.loader.pipeline_manifest.json
    file to collect all needed imports.

    Args:
        module_namespace(str): The full lucid namespace of the
        module to search, e.g. lucid.maya.asset_browser.

    Returns:
        list[str]: The list of unique modules that go into the
        import chain that makes up the given module.
    """
    manifest = scan_files(lucid.constants.LUCID_PATH)
    dependencies = manifest[module_namespace]['imports']
    for i in dependencies:
        dependencies = _combine_lists(dependencies, get_all_dependencies(i))

    return dependencies


@lucid.debug.timer
def main():
    export_manifest()
    print(get_all_dependencies('lucid.maya.shelves'))


if __name__ == '__main__':
    main()
