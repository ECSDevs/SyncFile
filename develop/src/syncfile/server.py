# Copyright (C) 2024 originalFactor
# 
# This file is part of Syncfile.
# 
# Syncfile is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Syncfile is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Syncfile.  If not, see <https://www.gnu.org/licenses/>.

from json import load, dump
from os import walk
from hashlib import sha512
from typing import List
from logging import getLogger

def contains(x:str, y:List[str])->bool:
    for i in y:
        if x.startswith(i):
            return True
    return False

logger = getLogger("server")

if __name__ == "__main__":
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(
        prog="EFS for Server",
        description="Like Git, but without Version Control.",
        usage="Generate index file for clients."
    )
    parser.add_argument(
        "-c", "--config",
        type=FileType('r'),
        default="Sconfig.json",
        help="the path of config file."
    )
    parser.add_argument(
        "-i", "--index",
        type=FileType('w'),
        default="index.json",
        help="the path of index file to generate."
    )
    args = parser.parse_args()
    
    logger.info("Loading configuration...")
    # import config file
    # with open(args.config) as f:
    #     config = load(f)
    config = load(args.config)

    '''
    Config structure:
    ```json
    [
        ["resourcePath", ["extensions"], "targetPath"]
    ]
    '''

    logger.info("Generating index...")
    # summon config file for client
    # New: force traverse join
    cc = {}
    for obj in config:
        logger.info(f"Generating {obj}...")
        # It's not allowed to use absolute path for targetPath or resourcePath.
        if obj[0].startswith("/") or obj[2].startswith("/"):
            raise Exception("Absolute path is not allowed for targetPath or resourcePath.")
        # loop to add all files to the client config
        for root, _, files in walk(obj[0]):
            compatibleRoot = root[len(obj[0]):].replace("\\", "/")
            if contains(compatibleRoot, obj[3]): continue # igore list
            logger.info(f"Walking through {compatibleRoot}")
            targetPath = (obj[2][:-1] if obj[2].endswith('/') else obj[2]) + (f'/{compatibleRoot}' if compatibleRoot else '')
            if targetPath not in cc:
                cc[targetPath] = {}
            for file in files:
                if ((file.split('.')[-1] in obj[1]) or ('*' in obj[1])) and \
                    (f'{compatibleRoot+"/" if compatibleRoot else ""}{file}' not in obj[3]): # add support for `*` in extensions
                    with open(f'{root}/{file}', 'rb') as f:
                        mhash = sha512(f.read(1024*1024)).hexdigest()
                    targetFileName = (root+'/' if '.' not in root else root[2:])+file
                    if targetFileName in cc[targetPath]:
                        logger.warn(f"{targetFileName} appeared twice! Check your configuration!")
                        continue
                    cc[targetPath][targetFileName] = mhash
                    logger.info(f"Proceed {targetFileName}!")

    logger.info(f"Generation Completed. Saving to {args.index}...")
    # save to file
    dump(cc, args.index)
