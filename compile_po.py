#!/usr/bin/env python3
"""
Compila il file django.po in django.mo usando solo la libreria standard Python.
Uso: python compile_po.py
"""
import struct
import array
import os

PO_FILE = os.path.join(os.path.dirname(__file__), "locale", "en", "LC_MESSAGES", "django.po")
MO_FILE = os.path.join(os.path.dirname(__file__), "locale", "en", "LC_MESSAGES", "django.mo")


def parse_po(po_path):
    """Parse a .po file and return list of (msgid, msgstr) tuples."""
    entries = []
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False
    is_obsolete = False

    with open(po_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n\r")

            # Skip obsolete entries
            if line.startswith("#~"):
                is_obsolete = True
                continue

            # Skip comments
            if line.startswith("#"):
                continue

            # Empty line = end of entry
            if not line.strip():
                if current_msgid is not None and current_msgstr is not None and not is_obsolete:
                    entries.append((current_msgid, current_msgstr))
                current_msgid = None
                current_msgstr = None
                in_msgid = False
                in_msgstr = False
                is_obsolete = False
                continue

            if is_obsolete:
                continue

            if line.startswith("msgid "):
                in_msgid = True
                in_msgstr = False
                current_msgid = line[6:].strip().strip('"')
            elif line.startswith("msgstr "):
                in_msgstr = True
                in_msgid = False
                current_msgstr = line[7:].strip().strip('"')
            elif line.startswith('"') and line.endswith('"'):
                continuation = line.strip('"')
                if in_msgid and current_msgid is not None:
                    current_msgid += continuation
                elif in_msgstr and current_msgstr is not None:
                    current_msgstr += continuation

    # Don't forget last entry
    if current_msgid is not None and current_msgstr is not None and not is_obsolete:
        entries.append((current_msgid, current_msgstr))

    return entries


def unescape(s):
    """Unescape common escape sequences in .po strings."""
    s = s.replace("\\n", "\n")
    s = s.replace("\\t", "\t")
    s = s.replace("\\\\", "\\")
    s = s.replace('\\"', '"')
    return s


def write_mo(entries, mo_path):
    """Write entries to a .mo file (GNU gettext binary format)."""
    # Sort entries by msgid (required by .mo format)
    entries.sort(key=lambda x: x[0])

    # MO file magic number
    MAGIC = 0x950412DE

    offsets = []
    ids = b""
    strs = b""

    for msgid, msgstr in entries:
        msgid_bytes = unescape(msgid).encode("utf-8")
        msgstr_bytes = unescape(msgstr).encode("utf-8")

        offsets.append((len(ids), len(msgid_bytes), len(strs), len(msgstr_bytes)))
        ids += msgid_bytes + b"\0"
        strs += msgstr_bytes + b"\0"

    # Header
    n_entries = len(entries)
    # Size of header: magic(4) + revision(4) + nstrings(4) + offset_orig(4) + offset_trans(4) + size_hash(4) + offset_hash(4) = 28
    header_size = 28
    # Each table entry: length(4) + offset(4) = 8 bytes
    key_start = header_size
    value_start = key_start + n_entries * 8
    ids_start = value_start + n_entries * 8

    koffsets = []
    voffsets = []
    for o in offsets:
        koffsets.append((o[1], o[0] + ids_start))
        voffsets.append((o[3], o[2] + ids_start + len(ids)))

    output = struct.pack(
        "Iiiiiii",
        MAGIC,           # magic
        0,               # revision
        n_entries,       # number of strings
        key_start,       # offset of original strings table
        value_start,     # offset of translated strings table
        0,               # size of hash table
        0,               # offset of hash table
    )

    for length, offset in koffsets:
        output += struct.pack("ii", length, offset)
    for length, offset in voffsets:
        output += struct.pack("ii", length, offset)

    output += ids
    output += strs

    with open(mo_path, "wb") as f:
        f.write(output)


if __name__ == "__main__":
    if not os.path.exists(PO_FILE):
        print(f"ERRORE: File non trovato: {PO_FILE}")
        exit(1)

    print(f"Parsing {PO_FILE}...")
    entries = parse_po(PO_FILE)
    print(f"Trovate {len(entries)} traduzioni attive.")

    print(f"Scrittura {MO_FILE}...")
    write_mo(entries, MO_FILE)
    print(f"SUCCESSO! File compilato: {MO_FILE}")
    print(f"Dimensione: {os.path.getsize(MO_FILE)} bytes")
