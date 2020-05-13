from music21 import converter
from clarinet import Clarinet

if __name__ == "__main__":

    possible1 = [
        'B4', 'C#5', 'C5', 'E-5'
    ]

    impossible1 = [
        'B4', 'C#5', 'C5', 'E-5', 'B4', 'C5', 'E-5', 'F5'
    ]
    impossible2 = [
        'B4', 'C#5', 'C5', 'E-5', 'B4', 'C5', 'E-5', 'F5',
        'B4', 'C#5', 'C5', 'E-5', 'B4', 'C5', 'E-5'
    ]

    # s = stream.Stream()
    # s.append([note.Note(n) for n in impossible2])

    s = converter.parse('./examples.musicxml')

    clarinet = Clarinet()

    clarinet.label_little_finger_gymnastics(s)
    clarinet.label_break_jumping(s)
    clarinet.label_range(s)
    s.show()
