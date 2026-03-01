from sys import argv
import re, struct

if argv[1] == "-d":
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
output.write(b'\x06\x94\x20') # magic bites

output.write(b'\x12')
output.write(bytes([len(bytes(songname, "utf-8"))]))
output.write(bytes(songname, "utf-8"))

output.write(b'\x13')
output.write(bytes([len(bytes(artist, "utf-8"))]))
output.write(bytes(artist, "utf-8"))

output.write(b'\x21')
output.write(bytes([len(bytes(creator, "utf-8"))]))
output.write(bytes(creator, "utf-8"))

for block in blocks:
    # id
    output.write(
        bytes([
            block["id"]
        ])
    )

    #position
    output.write(struct.pack("<f", block["posx"]))
    output.write(struct.pack("<f", block["posy"]))

    #rotation
    output.write(
        bytes([
            block["rot"]
        ]).rjust(2, b'\x00')
    )

output.close()