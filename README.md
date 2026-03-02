# .tdx File Format Specification

The .tdx format is a binary file format used for Tride Dash level data. All .tdx files begin with the magic bytes `0x6942`, followed by a version number. The current version is 1.

## Metadata Chunks

**Song Name**
- Type identifier: `0x12` (1 byte)
- Length: 1 byte (including file extension)
- Data: Variable-length song name string

**Song Artist**
- Type identifier: `0x13` (1 byte)
- Length: 1 byte
- Data: Variable-length artist name string

**Level Creator**
- Type identifier: `0x21` (1 byte)
- Length: 1 byte
- Data: Variable-length creator name string

## Level Block Data

Each block is structured as follows:

| Field | Size | Type |
|-------|------|------|
| ID | 1 byte | int |
| Position X | 4 bytes | float |
| Position Y | 4 bytes | float |
| Rotation | 2 bytes | int |

## Command-Line Tool

The included script converts between Tride Dash .txt and .tdx file formats.

For usage details, run:
```bash
python main.py --help
```