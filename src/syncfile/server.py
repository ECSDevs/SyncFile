# Copyright (C) 2024 originalFactor
# 
# This file is part of MCSMT.
# 
# MCSMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# MCSMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with MCSMT.  If not, see <https://www.gnu.org/licenses/>.

from json import load, dump
from os import walk
from hashlib import sha512
from os.path import split

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
    
    # import config file
    with open(args.config) as f:
        config = load(f)

    '''
    Config structure:
    ```json
    [
        ["resourcePath", ["extensions"], "targetPath"]
    ]
    '''

    # summon config file for client
    # New: force traverse join
    cc = {}
    for obj in config:
        # It's not allowed to use absolute path for targetPath or resourcePath.
        if obj[0].startswith("/") or obj[2].startswith("/"):
            raise Exception("Absolute path is not allowed for targetPath or resourcePath.")
        # loop to add all files to the client config
        for root, _, files in walk(obj[0]):
            compatibleRoot = root[len(obj[0]):].replace("\\", "/")
            targetPath = split(obj[1])[0] + (f'/{compatibleRoot}' if compatibleRoot else '')
            if targetPath not in cc:
                cc[targetPath] = []
            for file in files:
                if (file.split('.')[-1] in obj[1]) or ('*' in obj[1]): # add support for `*` in extensions
                    with open(f'{root}/{file}', 'rb') as f:
                        mhash = sha512(f.read(1024*1024)).hexdigest()
                    cc[targetPath].append([(f'{compatibleRoot}/' if compatibleRoot else '') + file, mhash])

    for obj in cc:
        cc[obj] = set(cc[obj])

    # save to file
    ccf = open(args.index, 'w')
    dump(cc, ccf)
    ccf.close()
