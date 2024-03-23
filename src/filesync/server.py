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
from os import walk, listdir
from hashlib import sha512
from .utils import safeListGet

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
    configf = open(args.config)
    config = load(configf)
    configf.close()

    # summon config file for client
    # New: allow reverse join
    cc = {}
    for obj in config:
        if ':' in obj["resourcePath"]:
            cc[obj["targetPath"]].append(obj["resourcePath"])
        fx = walk(obj["resourcePath"])
        for root, _, files in fx:
            root = root.replace('\\','/') if root!='.' else ''
            sr = '/'.join(root.split(obj["resourcePath"])[-1].split('/')[-1:0:-1])
            rp = ('/'+sr)if sr else ''
            if obj["targetPath"]+rp not in cc:
                cc[obj["targetPath"]+rp] = []
            for file in files:
                if (file.split('.')[-1] in obj["fileTypes"]) or ('' in obj["fileTypes"]):
                    filename = (root+'/'+file) if root else file
                    with open(filename, 'rb') as f:
                        mhash = sha512(f.read()).hexdigest()
                    cc[obj[2]+rp].append([filename, mhash])

    for obj in cc:
        cc[obj] = set(cc[obj])

    # save to file
    ccf = open(args.index, 'w')
    dump(cc, ccf)
    ccf.close()
