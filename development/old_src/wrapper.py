#!/usr/bin/env python3
# pipx.py (또는 pip-plus 등)

import sys
import subprocess

def main():
    if '-gp' in sys.argv:
        idx = sys.argv.index('-gp')
        target = sys.argv[idx + 1]
        name, version = target.split('==')
        url = f'git+https://github.com/crimson206/{name}.git@{version}'
        args = ['pip', 'install', url]
        subprocess.run(args)
    else:
        subprocess.run(['pip'] + sys.argv[1:])

if __name__ == '__main__':
    main()
