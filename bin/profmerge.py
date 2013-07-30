#
# Copyright (C) 2013 Judge Maygarden (wtfpl.jmaygarden@safersignup.com)
#
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

import argparse
from ftltools import profile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge two FTL profiles.')
    parser.add_argument('infile', nargs=2, help='FTL profile (prof.sav) files to merge.')
    parser.add_argument('-o', metavar='outfile', required=True, help='New FTL profile created from the merge.')
    args = parser.parse_args()

    p1 = profile.parse(open(args.infile[0]))
    p2 = profile.parse(open(args.infile[1]))
    data = profile.merge(p1, p2)
    with open(args.o, 'wb') as fout:
        fout.write(profile.to_sav(data))

