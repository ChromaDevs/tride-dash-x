from sys import argv
import re, struct
import zlib

__version__ = 1
verbose = False

if (len(argv) < 2 or 
    "-h"in argv or "--help" in argv or 
    (argv[1] not in ["--txt", "-t","-v","--verbose"] and argv[1][0] == "-" and "." not in argv[1])):
    print(
        f"""
▀▀█▀▀ █▀▀█ ░▀░ █▀▀▄ █▀▀ 　 █▀▀▄ █▀▀█ █▀▀ █░░█ 　 █░█ 
░░█░░ █▄▄▀ ▀█▀ █░░█ █▀▀ 　 █░░█ █▄▄█ ▀▀█ █▀▀█ 　 ▄▀▄ 
░░▀░░ ▀░▀▀ ▀▀▀ ▀▀▀░ ▀▀▀ 　 ▀▀▀░ ▀░░▀ ▀▀▀ ▀░░▀ 　 ▀░▀

USAGE:
    {argv[0]} [options] file

OPTIONS
    [no options]    converts tride's .txt to .tdx
    -t, --txt       converts .tdx back to tride's .txt (wip)
    -h, --help      show this message
    -v, --verbose   show extra output""")
    exit(0)

if "-t" in argv or "--txt" in argv:
    print("NOT IMPLEMENTED. EXITING")
    exit(0)

if "-v" in argv or "--verbose" in argv:
    verbose = True

g = open(argv[-1], "r")

src = g.read()
g.close()
songname = re.findall(r"song: (.+)Â§", src)[0]
artist = "" if re.findall(r"artist: (.+)Â§", src) == [] else re.findall(r"artist: (.+)Â§", src)[0]
creator = re.findall(r"creator: (.+)Â§", src)[0]
blocks = []

src = src.split("{")[1].strip(" \n}{")
for blok in src.splitlines():
    iD, px, py, rot = re.findall(r"id: (.+); pos: \((.+), (.+)\); rot: (.+);", blok)[0]
    blocks.append(
        {
            "id": int(iD),
            "posx": float(px),
            "posy": float(py),
            "rot": int(float(rot))
        }
    )

output = open(f"{argv[-1][0:-4]}.tdx", "wb")

output.truncate(0)
output.write(b'\x69\x42')

output.write(__version__.to_bytes())

output.write(b'\x12')
output.write(bytes([len(bytes(songname, "utf-8"))]))
output.write(bytes(songname, "utf-8"))

output.write(b'\x13')
output.write(bytes([len(bytes(artist, "utf-8"))]))
output.write(bytes(artist, "utf-8"))

output.write(b'\x21')
output.write(bytes([len(bytes(creator, "utf-8"))]))
output.write(bytes(creator, "utf-8"))

no_blocks = len(blocks)
prog = 0
print(f"[{'='*20}]")

blocks_buffer = bytearray(b'')

for block in blocks:
    prog += 1
    percent = f"{str(int(
        prog * 100 / no_blocks
    ))}%".rjust(4)
    print(f"\033[1A\033[30D\033[9C{percent}")

    blocks_buffer.extend(
        int(block["id"]).to_bytes(1)
    )

    blocks_buffer.extend(struct.pack("<f", block["posx"]))
    blocks_buffer.extend(struct.pack("<f", block["posy"]))

    blocks_buffer.extend(
        int(block["rot"]).to_bytes(2)
    )

compressed_buffer = zlib.compress(blocks_buffer)

output.write(compressed_buffer)

print(f"\033[1A[{'='*20}]\033[30D\033[8C!DONE!")
if verbose:
    print(f"Block data compressed, file size reduced by {len(blocks_buffer) - len(compressed_buffer)} bytes")
    print(f"file saved to {output.name}")
output.close()