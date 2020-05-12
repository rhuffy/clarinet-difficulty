# Analyzing Clarinet Difficulty using Music21

## Usage

Requires [music21](https://web.mit.edu/music21/)
`pip install music21`

clarinet-difficulty can be used on any music21 stream

```python
from music21 import converter
from clarinet import Clarinet
 
s = converter.parse('./your_file.musicxml')
clarinet = Clarinet()

clarinet.label_little_finger_gymnastics(s)
s.show()
```

## Introduction
The clarinet is a popular instrument in western music, found commonly in wind ensembles and symphony orchestras. When composing a work for any large modern ensemble, the composer is almost guaranteed to include a part for clarinet. However, the clarinet has a few structural and mechanical limitations that make certain types of phrases unexpectedly difficult to perform. While clarinetists are aware of these limitations, composers without experience on the instrument might not be aware and may include phrases in their work that are very difficult to perform properly.

Many works in the clarinet repertoire include difficult passages that can catch even experienced performers by surprise when sight reading or performing music with limited rehearsal time. Often you will find these passages circled and marked up in parts by clarinetists attempting to avoid mistakes.

Here, I demonstrate how Music21 can be used to detect and mark up difficult passages in clarinet music. This tool is useful for both composers and performers. Composers can use this tool to be aware of the difficulty of parts they are writing, and they can make changes to difficult parts when composing specifically for less experienced players. Performers can use this tool to find the most difficult passages in large amounts of music, helping them find exactly which parts require the most practice.


## Difficult Idioms

### Break Jumping
The register key on the clarinet is not as responsive as normal keys and tone holes, so frequent and rapid jumps between registers are difficult to perform.

### Altissimo Register
Notes above C6 are more difficult to play in tune, especially for less experienced clarinetists. Composers should consider avoiding notes in this register for music meant for younger players. Notes above G6 are very difficult to play, even for experienced clarinetists. Composers should avoid using these notes.

### Little Finger Gymnastics
On the standard clarinet, there are four keys operated by the left pinky and four keys operated by the right pinky. The left side keys are used for the pitches [B, C, C#, G#] and the right side keys are used for the pitches [B, C, C#, D#]. When playing a sequence of notes requiring these pinky keys, the clarinetist must alternate between their left and right side keys to ensure that note transitions are smooth. While there exists an alternate fingering for G# that does not use the pinky keys, D# can only be played using the right pinky. This introduces a constraint that requires a clarinetist to plan which keys to use in advance in a sequence of notes of the set [B, C, C#, D#].

Consider a sequence [B, C, D#]. If B is played on the left and C is played on the right, the clarinetist cannot transition smoothly to a D# as their right pinky is already in use, and there is no way to play D# using their left pinky. One must preemptively play the B on the right side so that the right side will be available to play D#.

Now consider a sequence [D#, B, C, D#]. It is impossible to assign alternating side key fingerings here as the first D# must be played on the right, making the only option D#-R, B-L, C-R, D#-L - which is impossible.

(In this situation, one is able to slide their left pinky from B to C, making a sequence D#-R, B-L, C-L, D#-R possible for skilled clarinetists)