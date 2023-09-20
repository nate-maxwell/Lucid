"""
# Command Line Input

* Description:

    The main cli module

* Update History:

    `2023.09.19` - Init, starting args ['maya', 'unreal', 'spainter', 'sdesigner']
"""


import argparse

import launch


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Startup command for Lucid Pipeline.')
    parser.add_argument(
        'dcc',
        metavar='DCC',
        help='DCC to launch. Must be one of {maya, unreal, spainter, sdesigner}.',
        choices={'maya', 'unreal', 'spainter', 'sdesigner'}
    )

    parser._positionals.title = parser._positionals.title.capitalize()
    parser._optionals.title = parser._optionals.title.capitalize()

    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    if args.dcc == 'maya':
        launch.launch_maya()
    elif args.dcc == 'unreal':
        launch.launch_unreal()
    elif args.dcc == 'spainter':
        launch.launch_painter()
    elif args.dcc == 'sdesigner':
        launch.launch_designer()


if __name__ == '__main__':
    main()
