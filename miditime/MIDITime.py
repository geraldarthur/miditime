
#-----------------------------------------------------------------------------
# Name:        makemidi.py
# Purpose:     Convert time-series data to a .mid file.
#
# Author:      Michael Corey <mcorey) at (cironline . org>
#
# Created:     2015/05/12
# Copyright:   (c) 2015 Michael Corey
# License:     Please see License.txt for the terms under which this
#              software is distributed.
#-----------------------------------------------------------------------------

from midiutil.MidiFile import MIDIFile


class MIDITime(object):

    def __init__(self, tempo=120, outfile='miditime.mid'):
        self.tempo = tempo
        self.outfile = outfile
        self.tracks = []

    def scale_to_note(self, mode, octave, scale_pct, octave_range=1):
            full_mode = []
            n = 0
            while n < octave_range:
                for m in mode:
                    current_octave = str(octave + (n*1))
                    full_mode.append(m + current_octave)
                n += 1
            index = int(scale_pct*float(len(full_mode)))
            if index >= len(full_mode):
                index = len(full_mode) - 1
            return full_mode[index]

    def note_to_midi_pitch(self, notename):
        midinum = 0
        note_chart = [["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"], ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"], ["A#", "Bb"], ["B"]]
        letter = notename[:-1]
        octave = notename[-1]

        i = 0
        for note in note_chart:
            for form in note:
                if letter == form:
                    midinum = i
                    break
            i += 1
        midinum += (int(octave))*12
        return midinum

    def linear_scale_pct(self, domain_min, domain_max, input, reverse=False):
        domain_range = domain_max - domain_min
        domain_pct = (input - domain_min)/domain_range

        if reverse:
            domain_pct = 1 - domain_pct
        return domain_pct

    def log_scale_pct(self, domain_min, domain_max, input, reverse=False):
        min_log_domain = pow(10, domain_min)
        max_log_domain = pow(10, domain_max)
        domain_range = max_log_domain - min_log_domain

        log_input = pow(10, input)
        domain_pct = (log_input - min_log_domain)/domain_range

        if reverse:
            domain_pct = 1 - domain_pct
        return domain_pct

    def scale(self, range_min, range_max, input_pct):
        scale_range = range_max - range_min
        return range_min + (input_pct*scale_range)

    def add_track(self, note_list):
        self.tracks.append(note_list)

    def add_note(self, track, channel, note):
        time = note[0]
        pitch = note[1]
        volume = note[2]
        duration = note[3]

        print pitch, time, duration, volume

        # Now add the note.
        self.MIDIFile.addNote(track, channel, pitch, time, duration, volume)

    def save_midi(self):
        # Create the MIDIFile Object with 1 track
        self.MIDIFile = MIDIFile(len(self.tracks))

        for i, note_list in enumerate(self.tracks):

            # Tracks are numbered from zero. Times are measured in beats.
            track = i
            time = 0
            channel = 0

            # Add track name and tempo.
            self.MIDIFile.addTrackName(track, time, "Track 1")
            self.MIDIFile.addTempo(track, time, self.tempo)

            for n in note_list:
                self.add_note(track, channel, n)

        # And write it to disk.
        binfile = open(self.outfile, 'wb')
        self.MIDIFile.writeFile(binfile)
        binfile.close()
