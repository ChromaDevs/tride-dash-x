from sys import argv
import re, struct

__version__ = 1

if len(argv) < 2 or argv[1] in ["--help", "-h"] or (argv[1] not in ["--txt", "-t"] and argv[0][0] == "-"):
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
    -h, --help      show this message""")
    exit(0)

if argv[1] in ["--txt", "-t"]:
    print("NOT IMPLEMENTED. EXITING")
    exit(0)

g = open(argv[1], "r")

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

output = open(f"{argv[1][0:-4]}.tdx", "wb")

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
for block in blocks:
    prog += 1
    percent = f"{str(int(
        prog * 100 / no_blocks
    ))}%".rjust(4)
    print(f"\033[1A\033[30D\033[9C{percent}")

    output.write(
        int(block["id"]).to_bytes(1)
    )

    output.write(struct.pack("<f", block["posx"]))
    output.write(struct.pack("<f", block["posy"]))

    output.write(
        int(block["rot"]).to_bytes(2)
    )
print(f"\033[1A[{'='*20}]\033[30D\033[8C!DONE!")
print(f"file saved to {output.name}")
output.close()