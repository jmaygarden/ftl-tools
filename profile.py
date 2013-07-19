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

from struct import calcsize, pack, unpack

def parse(filename):
    with open(filename, 'rb') as fin:
        data = {
                'version': 0,
                'achievements': [],
                'topFive': [],
                'highScores': [],
                'skills': [],
                }

        data['version'], numAchievements = unpack('2L', fin.read(calcsize('2L')))

        for i in xrange(numAchievements):
            n = unpack('L', fin.read(calcsize('L')))[0]
            name = fin.read(n)
            normal = unpack('L', fin.read(calcsize('L')))[0]
            data['achievements'].append((name, normal))

        data['ships'] = [unpack('L', fin.read(calcsize('L')))[0] for i in xrange(12)]

        numTopFive = unpack('L', fin.read(calcsize('L')))[0]
        for i in xrange(numTopFive):
            n = unpack('L', fin.read(calcsize('L')))[0]
            shipName = fin.read(n)
            n = unpack('L', fin.read(calcsize('L')))[0]
            shipType = fin.read(n)
            stats = unpack('4L', fin.read(calcsize('4L')))
            data['topFive'].append((shipName, shipType, stats))

        numHighScores = unpack('L', fin.read(calcsize('L')))[0]
        for i in xrange(numHighScores):
            n = unpack('L', fin.read(calcsize('L')))[0]
            shipName = fin.read(n)
            n = unpack('L', fin.read(calcsize('L')))[0]
            shipType = fin.read(n)
            stats = unpack('4L', fin.read(calcsize('4L')))
            data['highScores'].append((shipName, shipType, stats))

        data['scores'] = list(unpack('10L', fin.read(calcsize('10L'))))
        for i in xrange(5):
            score = unpack('L', fin.read(calcsize('L')))[0]
            n = unpack('L', fin.read(calcsize('L')))[0]
            name = fin.read(n)
            n = unpack('L', fin.read(calcsize('L')))[0]
            race = fin.read(n)
            gender = unpack('L', fin.read(calcsize('L')))[0]
            data['skills'].append((score, name, race, gender))

        return data


def merge((file1, file2)):
    p1, p2 = parse(file1), parse(file2)
    new = dict()

    new['version'] = max(p1['version'], p2['version'])

    def _merge_without_duplicates(a, b):
        diff = set(b) - set(a)
        return a + list(diff)

    def _merge_key(a, b, key):
        return _merge_without_duplicates(a[key], b[key])

    keys = [
            'achievements',
            'ships',
            'topFive',
            'highScores',
            ]
    for key in keys:
        new[key] = _merge_key(p1, p2, key)

    new['topFive'] = sorted(new['topFive'], key=lambda x: x[2], reverse=True)[:5]

    new['scores'] = []
    for a, b in zip(p1['scores'], p2['scores']):
        new['scores'].append(max(a, b))

    new['skills'] = []
    for a, b in zip(p1['skills'], p2['skills']):
        new['skills'].append(max(a, b, lambda x: x[0]))

    return new


def to_txt(data):
    s = 'Version: %s\n' % data['version']

    s += '\nAchievements:\n'
    for achievement in data['achievements']:
        s += '\t%s (%d)\n' % achievement

    s += '\nShips: %s\n' % ' '.join(map(str, data['ships']))

    s += '\nHigh Scores:\n'
    for score in data['topFive']:
        s += '\t%s, %s, %s\n' % (score[0], score[1], ', '.join(map(str, score[2])))

    s += '\nAll Scores:\n'
    for score in data['highScores']:
        s += '\t%s, %s, %s\n' % (score[0], score[1], ', '.join(map(str, score[2])))

    s += '\nOther: %s\n' % ', '.join(map(str, data['scores']))

    s += '\nSkills:\n'
    categories = [
            'Repair',
            'Combat Kills',
            'Pilot Evasions',
            'Jumps Survived',
            'Skill Masteries'
            ]
    for category, skill in zip(categories, data['skills']):
        s += '\t%s: %d, %s, %s, %d\n' % ((category, ) + skill)

    return s

def to_sav(data):
    s = pack('<L', data['version'])

    s += pack('<L', len(data['achievements']))
    for achievement in data['achievements']:
        n = len(achievement[0])
        s += pack('<L%dsL' % n, n, achievement[0], achievement[1])

    s += pack('<12L', *data['ships'])

    s += pack('<L', len(data['topFive']))
    for score in data['topFive']:
        n1, n2 = len(score[0]), len(score[1])
        s += pack('<L%dsL%ds4L' % (n1, n2), n1, score[0], n2, score[1], *score[2])

    s += pack('<L', len(data['highScores']))
    for score in data['highScores']:
        n1, n2 = len(score[0]), len(score[1])
        s += pack('<L%dsL%ds4L' % (n1, n2), n1, score[0], n2, score[1], *score[2])

    s += pack('<10L', *data['scores'])

    for skill in data['skills']:
        n1, n2 = len(skill[1]), len(skill[2])
        s += pack('<LL%dsL%dsL' % (n1, n2), skill[0], n1, skill[1], n2, skill[2], skill[3])

    return s

