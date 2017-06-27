#!/usr/bin/python
'''
Print guitar scales to stdout
'''
import argparse
import textwrap

MAXFRET = 16
NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Scale dictionary
SCALEDICT = [
    ['Scale', 'Chromatic', '1,b2,2,b3,3,4,b5,5,b6,6,b7,7'],
    ['Scale', 'Major', '1,2,3,4,5,6,7'],
    ['Scale', 'Minor Natural', '1,2,b3,4,5,b6,b7'],
    ['Scale', 'Minor Harmonic', '1,2,b3,4,5,b6,7'],
    ['Scale', 'Major Pentatonic', '1,2,3,5,6'],
    ['Scale', 'Minor Pentatonic', '1,b3,4,5,b7'],
    ['Scale', 'Blues Pentatonic', '1,b3,4,b5,5,b7'],
    ['Mode', 'Ionian', '1,2,3,4,5,6,7'],
    ['Mode', 'Dorian', '1,2,b3,4,5,6,b7'],
    ['Mode', 'Phrygian', '1,b2,b3,4,5,b6,b7'],
    ['Mode', 'Lydian', '1,2,3,#4,5,6,7'],
    ['Mode', 'Mixolydian', '1,2,3,4,5,6,b7'],
    ['Mode', 'Aeolian', '1,2,b3,4,5,b6,b7'],
    ['Mode', 'Locrian', '1,b2,b3,4,b5,b6,b7'],
    ['Chord', 'Major', '1,3,5'],
    ['Chord', 'Minor', '1,b3,5'],
    ['Chord', '7th', '1,3,5,b7'],
    ['Chord', 'Major 7th', '1,3,5,7'],
    ['Chord', 'Minor 7th', '1,b3,5,b7'],
    ['Chord', '6th', '1,3,5,6'],
    ['Chord', 'Augmented', '1,3,#5'],
    ['Chord', 'Diminished', '1,b3,b5']
]


class GuitarScale(object):
    ''' Determines scales & notes on a fretboard
    '''

    def __init__(self, key, scale, chord, tuning):
        scale = scale.title()
        scaleinput = [
            n for n, l in enumerate(SCALEDICT)
            if l[1].title().startswith(scale) and (l[0] == 'Chord') is chord][0]
        scalevalues = SCALEDICT[scaleinput][2]

        key = key.title()
        if key.find('b') >= 0 or scalevalues.find('b') >= 0:
            notes = NOTES_FLAT
        else:
            notes = NOTES_SHARP

        # get the scale & transpose to key
        scale = [(x + notes.index(key)) %
                 12 for x in GuitarScale.interval2idx(scalevalues)]

        strings = list(reversed([NOTES_FLAT.index(z) for z in tuning]))

        self.params = {
            'fretboard': None,
            'scalenotes': None,
            'intervals': None,
            'notes': notes,
            'scalevalues': scalevalues,
            'scaleinput': scaleinput
        }
        self.inputs = {
            'key': key,
            'scale': scale,
            'chord': chord,
            'tuning': tuning,
            'strings': strings
        }

    @staticmethod
    def interval2idx(intervalinput):
        ''' Convert from interval numbers to notes '''
        interval_flat = ['1', 'b2', '2', 'b3', '3',
                         '4', 'b5', '5', 'b6', '6', 'b7', '7']
        interval_sharp = ['1', '#1', '2', '#2', '3',
                          '4', '#4', '5', '#5', '6', '#6', '7']
        if repr(intervalinput).find('b') >= 0:
            interval = interval_flat
        else:
            interval = interval_sharp
        return [interval.index(i) for i in intervalinput.split(',')]

    @staticmethod
    def description():
        ''' Return a description of the class '''
        return 'available scales/chords:\n  ' + \
               '\n  '.join(' - '.join(x[:2]) for x in SCALEDICT)

    @staticmethod
    def calculate_notes(notes, scale, strings):
        ''' Calculate the notes '''
        scalenotes = [notes[x] for x in scale]
        fretboard = [[notes[(x + y) % 12] for x in range(MAXFRET)] for y in strings]
        for string in xrange(len(strings)):  # eliminate notes not in scale
            for fret in range(MAXFRET):
                if fretboard[string][fret] not in scalenotes:
                    fretboard[string][fret] = ''
        return fretboard, scalenotes

    @staticmethod
    def calculate_intervals(scalevalues, scalenotes):
        ''' Calculate the intervals '''
        idx = [x for x in GuitarScale.interval2idx(scalevalues)] + [12]
        intervals = ' - '.join(str((idx[x] - idx[x - 1]) / 2.)
                               for x in range(1, len(idx)))
        return scalenotes, intervals

    def construct_fretboard(self):
        ''' Construct the fretboard '''
        strings = self.inputs.get('strings')
        scale = self.inputs.get('scale')
        notes = self.params.get('notes')
        scalevalues = self.params.get('scalevalues')
        fretboard, scalenotes = GuitarScale.calculate_notes(notes, scale, strings)
        scalenotes, intervals = GuitarScale.calculate_intervals(scalevalues, scalenotes)
        self.params['fretboard'] = fretboard
        self.params['scalenotes'] = scalenotes
        self.params['intervals'] = intervals

    def printable_fretboard(self):
        ''' Pretty print '''
        key = self.inputs.get('key')
        strings = self.inputs.get('strings')
        tuning = self.inputs.get('tuning')
        scaleinput = self.params.get('scaleinput')
        scalenotes = self.params.get('scalenotes')
        scalevalues = self.params.get('scalevalues')
        intervals = self.params.get('intervals')
        fretboard = self.params.get('fretboard')
        scalename = key + ' ' + SCALEDICT[scaleinput][1] + ' ' + SCALEDICT[scaleinput][0]

        output = textwrap.dedent('''
        {dashline}
        {scalename}
        {dashline}

        Scale notes: {scalenotes}
                     {scalevalues}

        Intervals: {intervals}

        Tuning: {tuning}

        '''.format(
            dashline='-'*len(scalename),
            scalename=scalename,
            scalenotes=' - '.join(x.center(3) for x in scalenotes),
            scalevalues=' - '.join(x.center(3) for x in scalevalues.split(',')),
            intervals=intervals,
            tuning=' - '.join(tuning)
        ))

        for current_string in xrange(len(strings)):
            fret_sym, nut_sym = '|', '||'
            if fretboard[current_string][0] == '':
                output += ' ' * 2 + nut_sym
            else:
                output += fretboard[current_string][0].center(2) + nut_sym
            for current_fret in range(1, MAXFRET):
                if fretboard[current_string][current_fret] == '':
                    output += '-' * 5 + fret_sym
                elif fretboard[current_string][current_fret] == scalenotes[0] and scaleinput != 0:
                    output += (
                        '(' + fretboard[current_string][current_fret] + ')').center(5, '-') + \
                        fret_sym
                else:
                    output += fretboard[current_string][current_fret].center(5, '-') + \
                        fret_sym
            output += '\n'
        output += '\n                  3           5           7' +\
                     '           9                o o                15'

        return output

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description=GuitarScale.description(),
        formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('key', type=str, help='The key')
    PARSER.add_argument('scale', type=str, help='The scale')
    PARSER.add_argument('--chord', '-c', help='Display chord', action='store_true')
    PARSER.add_argument('--tuning', '-t', help='String tuning', default='EADGBE', type=str)
    ARGS = PARSER.parse_args()

    SCALE = GuitarScale(key=ARGS.key, scale=ARGS.scale, chord=ARGS.chord, tuning=ARGS.tuning)
    SCALE.construct_fretboard()
    print SCALE.printable_fretboard()
