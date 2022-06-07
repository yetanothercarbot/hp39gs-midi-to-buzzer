#!/usr/bin/env python3
import music21, sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print(f"Usage: {sys.argv[0]} input-file [beat-length]")
  sys.exit(1)

if len(sys.argv) == 3:
  try:
    beat_length = int(sys.argv[2]) # Last argument is beat length
  except:
    print("Error - beat length is not a valid integer")
    sys.exit(1)
else:
  beat_length = 500
notes = []
command = "HP39AscD 4 MIDI"

def print_iter(item, counter=0):
  try:
    for k, v in enumerate(item):
      if type(v) is music21.note.Note:
        #print((" " * 6 * counter) + f"[{k}/{len(item)}] ({type(v)}) {v.pitch} for {v.quarterLength}")
        notes.append(v)
      elif type(v) is music21.note.Rest:
        #print((" " * 6 * counter) + f"[{k}/{len(item)}] ({type(v)}) Rest for {v.quarterLength}")
        if k > 0 and v.quarterLength < 4:
          notes.append(v)
      else:
        pass
        #print((" " * 6 * counter) + f"[{k}/{len(item)}] ({type(v)}) {v}")
      print_iter(v, counter+1)
  except TypeError:
    pass

score = music21.converter.parse(sys.argv[1])
print_iter(score)

for k, note in enumerate(notes):
  if type(note) is music21.note.Rest:
    command += f"WAIT {int(beat_length * note.quarterLength)/100}:\r\n"
  else:
    command += f"BEEP {int(note.pitch.frequency)};{int(beat_length * note.quarterLength)/1000}:\r\n"
print(command)
