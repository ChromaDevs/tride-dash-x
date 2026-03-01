# .tdx format for tride dash levels

It is a binary format. All *.tdx* files have the magic bytes `0x069420` at the start.

## Metadata chunks

- Song Name
    - 1 byte (`0x12`) to specify that it is a song name.
    - 1 byte for the length (includes file extension).
    - Bytes for the song's name

- Song Artist
    - 1 byte (`0x13`) to specify that it is the name of the song's artist.
    - 1 byte for the length.
    - Bytes for the artist's name

- Level's Creator
    - 1 byte (`0x21`) to specify that it is the name of the level's creator
    - 1 byte for the length.
    - Bytes for the creator's name

## Level block data

> For every block:
- ID: 1 byte
- position: (float) 4 bytes
- rotation: 2 bytes