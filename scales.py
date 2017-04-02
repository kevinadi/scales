#!/usr/bin/python

import sys
MAXFRET = 16

def interval2idx(intervalinput):
    interval_flat =  ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']
    interval_sharp = ['1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7']
    if repr(intervalinput).find('b') >= 0:
        interval = interval_flat
    else:
        interval = interval_sharp
    return [ interval.index(x) for x in intervalinput.split(',') ]

notes_flat =  ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
strings = [4, 11, 7, 2, 9, 4] #standard tuning

### Scale dictionary
scaledict=  [ ['Scale', 'Chromatic'        , '1,b2,2,b3,3,4,b5,5,b6,6,b7,7'],
              ['Scale', 'Major'            , '1,2,3,4,5,6,7'],
              ['Scale', 'Natural Minor'    , '1,2,b3,4,5,b6,b7'],
              ['Scale', 'Harmonic Minor'   , '1,2,b3,4,5,b6,7'],
              ['Scale', 'Major Pentatonic' , '1,2,3,5,6'],
              ['Scale', 'Minor Pentatonic' , '1,b3,4,5,b7'],
              ['Scale', 'Blues Pentatonic' , '1,b3,4,b5,5,b7'],
              ['Mode', 'Ionian'            , '1,2,3,4,5,6,7'],
              ['Mode', 'Dorian'            , '1,2,b3,4,5,6,b7'],
              ['Mode', 'Phrygian'          , '1,b2,b3,4,5,b6,b7'],
              ['Mode', 'Lydian'            , '1,2,3,#4,5,6,7'],
              ['Mode', 'Mixolydian'        , '1,2,3,4,5,6,b7'],
              ['Mode', 'Aeolian'           , '1,2,b3,4,5,b6,b7'],
              ['Mode', 'Locrian'           , '1,b2,b3,4,b5,b6,b7'],
              ['Chord', 'Major'            , '1,3,5'],
              ['Chord', 'Minor'            , '1,b3,5'],
              ['Chord', '7th'              , '1,3,5,b7'],
              ['Chord', 'Major 7th'        , '1,3,5,7'],
              ['Chord', 'Minor 7th'        , '1,b3,5,b7'],
              ['Chord', '6th'              , '1,3,5,6'],
              ['Chord', 'Augmented'        , '1,3,#5'],
              ['Chord', 'Diminished'       , '1,b3,b5']
            ]

### Pretty print the scale dictionary
scaletype = ''
for x in range(len(scaledict)):
    if scaletype != scaledict[x][0]:
        scaletype = scaledict[x][0]
        print '\n', scaletype.center(6),
    else:
        print ''.center(6),
    print x,':', scaledict[x][1]

### Get inputs
scaleinput = int(raw_input('Scale: '))
while scaleinput not in range(len(scaledict)):
    print 'Scale must be between 0 and', len(scaledict)-1
    scaleinput = int(raw_input('Scale: '))
scalevalues = scaledict[int(scaleinput)][2]
if scaleinput != 0: #get key if not chromatic
    key = raw_input('Key: ').title()
else:
    key = 'C'
if key.find('b') >=0 or scalevalues.find('b') >= 0:
    notes = notes_flat
else:
    notes = notes_sharp
scale = [ (x + notes.index(key)) % 12 for x in interval2idx(scalevalues) ] #get the scale & transpose

### Construct the fretboard
scalenotes = [ notes[x] for x in scale ]
frets = [ [ notes[ (x+y) % 12 ] for x in range(MAXFRET) ] for y in strings ]
for x in range(6): #eliminate notes not in scale
    for y in range(MAXFRET):
        if frets[x][y] not in scalenotes:
            frets[x][y] = ''

### Figure out the intervals
idx = [ x for x in interval2idx(scalevalues) ] + [12]
intervals = ' - '.join(str((idx[x] - idx[x-1])/2.) for x in range(1,len(idx)))

### Pretty print
scalename = key + ' ' + scaledict[scaleinput][1] + ' ' + scaledict[scaleinput][0]
print '\n', '-'*len(scalename), '\n', scalename, '\n', '-'*len(scalename)
print '\nScale notes:', ' - '.join(x.center(3) for x in scalenotes)
print ' '*12, ' - '.join(x.center(3) for x in scalevalues.split(',')), '\n'
print 'Intervals:', intervals, '\n'
for x in range(6):
    if x == 0:
        FRET, NUT = '|', '||'
    elif x == 5:
        FRET, NUT = '|', '||'
    else:
        FRET, NUT = '|', '||'
    if frets[x][0] == '':
        sys.stdout.write( ' '*2 + NUT )
    else:
        sys.stdout.write( frets[x][0].center(2) + NUT )
    for y in range(1,MAXFRET):
        if frets[x][y] == '':
            sys.stdout.write( '-'*5 + FRET )
        elif frets[x][y] == scalenotes[0] and scaleinput != 0:
            sys.stdout.write( ('('+frets[x][y]+')').center(5,'-') + FRET )
        else:
            sys.stdout.write( frets[x][y].center(5,'-') + FRET )
    print
DOT = 'o'
print
print ' '*17, 3, ' '*9, 5, ' '*9, 7, ' '*9, 9, ' '*14, DOT,DOT, ' '*14, 15
