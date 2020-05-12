from music21 import *
from enum import Enum
from typing import List, Set


class ClarinetRegister(Enum):
    chalumeau = 'chalumeau'
    throat = 'throat'
    clarion = 'clarion'
    altissimo = 'altissimo'


class Clarinet:

    def __init__(self, minimum_pitch='E3', maximum_pitch='B-6'):
        self.minimum_pitch = pitch.Pitch(minimum_pitch)
        self.maximum_pitch = pitch.Pitch(maximum_pitch)

    def check_note_in_range(self, n: note.Note) -> bool:
        return self.minimum_pitch <= n.pitch <= self.maximum_pitch

    def get_register(self, n: note.Note) -> ClarinetRegister:
        if n.pitch <= pitch.Pitch('E4'):
            return ClarinetRegister.chalumeau
        if n.pitch <= pitch.Pitch('A#4'):
            return ClarinetRegister.throat
        if n.pitch <= pitch.Pitch('C6'):
            return ClarinetRegister.clarion
        else:
            return ClarinetRegister.altissimo

    def normalize_to_clarion(self, n: note.Note):
        '''
        If a note is in the lower Chalumeau register,
        converts to the note with the same fingering
        in the Clarion register.
        Useful for working with fingerings.
        '''
        if isinstance(n, note.Rest):
            return n

        if self.get_register(n) != ClarinetRegister.chalumeau:
            return n

        return note.Note(n.pitch.ps + 19)

    def label_little_finger_gymnastics(self, s: stream.Stream) -> List[int]:
        '''
        Returns positions of notes in a stream containing a sequence of notes
        that is difficult to finger on the clarinet.

        Left-right pinky gymnastics
         - L -> B4R, C4R, C#4R, E-4R
         - R -> B4L, C4L, C#4L
        '''

        class LFP(Enum):
            left = 'left'
            right = 'right'
            up = 'up'
            fail = 'fail'

        requires_little_finger: Set[int] = {note.Note(s).pitch.ps for s in [
            'B4', 'C5', 'C#5', 'D#5']}
        right_side = requires_little_finger
        left_side = {note.Note(s).pitch.ps for s in ['B4', 'C5', 'C#5']}

        eflat_ps = note.Note('E-5').pitch.ps

        notes: List[note.Note] = [
            self.normalize_to_clarion(n) for n in s.recurse().getElementsByClass(['Note', 'Rest'])]

        def run_assignment(lfp: LFP, n: note.Note):
            if lfp == LFP.left:
                lfp = LFP.right if n.pitch.ps in right_side else LFP.fail
            elif lfp == LFP.right:
                lfp = LFP.left if n.pitch.ps in left_side else LFP.fail
            return lfp

        def end_sequence(seq_a, seq_b):
            if len(seq_a) > 0 and seq_a[-1][1] != LFP.fail:
                for n, lfp in seq_a:
                    if lfp == LFP.left:
                        n.lyric = 'L'
                    elif lfp == LFP.right:
                        n.lyric = 'R'
                    elif lfp == LFP.fail:
                        n.style.color = 'red'
            elif len(seq_b) > 0 and seq_b[-1][1] != LFP.fail:
                for n, lfp in seq_a:
                    if lfp == LFP.left:
                        n.lyric = 'L'
                    elif lfp == LFP.right:
                        n.lyric = 'R'
                    elif lfp == LFP.fail:
                        n.style.color = 'red'
            else:
                longest_seq = seq_a if len(seq_a) > len(seq_b) else seq_b
                for n, lfp in longest_seq:
                    if lfp == LFP.left:
                        n.lyric = 'L'
                        n.style.color = 'red'
                    elif lfp == LFP.right:
                        n.lyric = 'R'
                        n.style.color = 'red'
                    elif lfp == LFP.fail:
                        n.style.color = 'red'

        sequence_start_left = []
        sequence_start_right = []

        for i, n in enumerate(notes):

            if isinstance(n, note.Rest) or \
                (isinstance(notes[i-1], note.Note) and n.pitch.ps == notes[i-1].pitch.ps) \
                    or n.pitch.ps not in requires_little_finger:
                end_sequence(sequence_start_left, sequence_start_right)
                sequence_start_left = []
                sequence_start_right = []
                continue

            if len(sequence_start_left) == 0:
                if n.pitch.ps == eflat_ps:
                    sequence_start_left.append((n, LFP.fail))
                    sequence_start_right.append((n, LFP.right))
                else:
                    sequence_start_left.append((n, LFP.left))
                    sequence_start_right.append((n, LFP.right))
                continue

            if n.pitch.ps == eflat_ps:
                if sequence_start_left[-1][1] == LFP.left:
                    sequence_start_left.append((n, LFP.right))
                else:
                    sequence_start_left.append((n, LFP.fail))

                if sequence_start_right[-1][1] == LFP.left:
                    sequence_start_right.append((n, LFP.right))
                else:
                    sequence_start_right.append((n, LFP.fail))

            else:
                if sequence_start_left[-1][1] != LFP.fail:
                    sequence_start_left.append(
                        (n, LFP.left if sequence_start_left[-1][1] == LFP.right else LFP.right))
                if sequence_start_right[-1][1] != LFP.fail:
                    sequence_start_right.append(
                        (n, LFP.left if sequence_start_right[-1][1] == LFP.right else LFP.right))

            # if n.pitch.ps not in requires_little_finger:
            #     start_left_lfp = LFP.up
            #     start_right_lfp = LFP.up
            #     continue

            # if start_left_lfp == LFP.up or start_right_lfp == LFP.up:
            #     start_left_lfp = LFP.left if n.pitch.ps in left_side else LFP.fail
            #     start_right_lfp = LFP.right if n.pitch.ps in right_side else LFP.fail
            #     continue

            # if start_left_lfp != LFP.fail:
            #     start_left_lfp = run_assignment(start_left_lfp, n)

            # if start_right_lfp != LFP.fail:
            #     start_right_lfp = run_assignment(start_left_lfp, n)

            # if start_left_lfp == LFP.fail and start_right_lfp == LFP.fail:
            #     n.style.color = 'red'

        # print(start_left_lfp, start_right_lfp)
