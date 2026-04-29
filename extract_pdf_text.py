"""
extract_pdf_text.py — Extractor de texto de PDFs sin dependencias externas.

Uso:
    python3 extract_pdf_text.py <archivo.pdf>
    python3 extract_pdf_text.py <archivo.pdf> --output salida.txt
    python3 extract_pdf_text.py <archivo.pdf> --pages   # muestra texto página por página

Cómo funciona:
    Los PDFs modernos codifican el texto como CIDs (glyph IDs) en hexadecimal.
    Cada fuente embebe un mapa ToUnicode (CMap) que traduce CID → carácter Unicode.
    Este script:
      1. Parsea todos los CMap streams del PDF.
      2. Asocia cada nombre de fuente (/F1, /F2, …) con su CMap por página.
      3. Descomprime los content streams y decodifica los operadores TJ/Tj.
"""

import re
import zlib
import sys
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing de CMaps (ToUnicode)
# ---------------------------------------------------------------------------

def parse_cmap(cmap_data: bytes) -> dict[int, str]:
    """Parsea un CMap ToUnicode y retorna {cid: unicode_char}."""
    mapping: dict[int, str] = {}

    # beginbfchar ... endbfchar
    for section in re.findall(rb"beginbfchar(.*?)endbfchar", cmap_data, re.DOTALL):
        for cid_hex, uni_hex in re.findall(rb"<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>", section):
            cid = int(cid_hex, 16)
            uni_bytes = bytes.fromhex(uni_hex.decode())
            try:
                if len(uni_bytes) == 4:
                    high = int.from_bytes(uni_bytes[:2], "big")
                    low  = int.from_bytes(uni_bytes[2:], "big")
                    if 0xD800 <= high <= 0xDBFF and 0xDC00 <= low <= 0xDFFF:
                        # surrogate pair → código fuera del BMP
                        mapping[cid] = chr(0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00))
                    else:
                        mapping[cid] = uni_bytes.decode("utf-16-be")
                else:
                    mapping[cid] = uni_bytes.decode("utf-16-be")
            except Exception:
                pass

    # beginbfrange ... endbfrange
    for section in re.findall(rb"beginbfrange(.*?)endbfrange", cmap_data, re.DOTALL):
        for s_hex, e_hex, u_hex in re.findall(
            rb"<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>", section
        ):
            s_cid = int(s_hex, 16)
            e_cid = int(e_hex, 16)
            s_uni = int(u_hex, 16)
            for i in range(e_cid - s_cid + 1):
                mapping[s_cid + i] = chr(s_uni + i)

    return mapping


# ---------------------------------------------------------------------------
# Lectura de objetos del PDF
# ---------------------------------------------------------------------------

def index_objects(data: bytes) -> dict[int, int]:
    """Devuelve {obj_num: byte_offset} para todos los objetos del PDF."""
    return {int(m.group(1)): m.start() for m in re.finditer(rb"(\d+)\s+0\s+obj\b", data)}


def get_obj_content(data: bytes, obj_positions: dict[int, int], obj_num: int) -> bytes:
    """Retorna el contenido del objeto (hasta 'endobj')."""
    pos = obj_positions.get(obj_num)
    if pos is None:
        return b""
    end = data.find(b"endobj", pos)
    return data[pos:end] if end != -1 else b""


def get_stream_content(data: bytes, obj_positions: dict[int, int], obj_num: int) -> bytes | None:
    """Retorna el stream descomprimido del objeto, o None si no tiene stream."""
    pos = obj_positions.get(obj_num)
    if pos is None:
        return None
    end = data.find(b"endobj", pos)
    stream_m = re.search(rb"stream\r?\n", data[pos:end])
    if not stream_m:
        return None
    stream_start = pos + stream_m.end()
    stream_end   = data.find(b"\nendstream", stream_start)
    if stream_end == -1:
        return None
    raw = data[stream_start:stream_end]
    try:
        return zlib.decompress(raw)
    except Exception:
        return raw  # sin compresión o con otra compresión


# ---------------------------------------------------------------------------
# Construcción de tablas de fuentes
# ---------------------------------------------------------------------------

def build_cmap_table(data: bytes, obj_positions: dict[int, int]) -> dict[int, dict[int, str]]:
    """Retorna {obj_num: cmap} para todos los objetos que contienen un CMap."""
    table: dict[int, dict[int, str]] = {}
    for obj_num in obj_positions:
        sc = get_stream_content(data, obj_positions, obj_num)
        if sc and (b"beginbfchar" in sc or b"beginbfrange" in sc):
            cmap = parse_cmap(sc)
            if cmap:
                table[obj_num] = cmap
    return table


def build_font_table(
    data: bytes,
    obj_positions: dict[int, int],
    cmap_by_obj: dict[int, dict[int, str]],
) -> dict[int, dict[int, str]]:
    """
    Retorna {font_obj_num: cmap} para los objetos /Type /Font
    que tienen un /ToUnicode stream.
    """
    table: dict[int, dict[int, str]] = {}
    for obj_num in obj_positions:
        oc = get_obj_content(data, obj_positions, obj_num)
        if b"/Type /Font" not in oc and b"/Type\n/Font" not in oc:
            continue
        tou_m = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", oc)
        if tou_m:
            tou_obj = int(tou_m.group(1))
            if tou_obj in cmap_by_obj:
                table[obj_num] = cmap_by_obj[tou_obj]
    return table


def get_font_cmaps_for_resource(
    data: bytes,
    obj_positions: dict[int, int],
    font_by_obj: dict[int, dict[int, str]],
    res_obj_num: int,
) -> dict[str, dict[int, str]]:
    """
    Dado el objeto /Resources de una página, retorna
    {'F1': cmap, 'F2': cmap, ...}.
    """
    oc = get_obj_content(data, obj_positions, res_obj_num)
    font_m = re.search(rb"/Font\s*<<(.*?)>>", oc, re.DOTALL)
    if not font_m:
        return {}
    result: dict[str, dict[int, str]] = {}
    for fname, fobj_num in re.findall(rb"/(F\d+)\s+(\d+)\s+0\s+R", font_m.group(1)):
        fobj = int(fobj_num)
        if fobj in font_by_obj:
            result[fname.decode()] = font_by_obj[fobj]
    return result


# ---------------------------------------------------------------------------
# Decodificación de content streams
# ---------------------------------------------------------------------------

def decode_hex_string(hex_str: bytes, cmap: dict[int, str]) -> str:
    """Decodifica una cadena hex de 2-byte CIDs usando un CMap."""
    hs = hex_str.decode() if isinstance(hex_str, bytes) else hex_str
    return "".join(cmap.get(int(hs[i:i+4], 16), "") for i in range(0, len(hs) - 3, 4))


def decode_content_stream(dec: bytes, font_cmaps: dict[str, dict[int, str]]) -> list[str]:
    """
    Extrae todos los fragmentos de texto de un content stream descomprimido.
    Retorna una lista de strings (uno por bloque TJ/Tj).
    """
    fragments: list[str] = []
    current_cmap: dict[int, str] | None = None

    for line in dec.split(b"\n"):
        line = line.strip()
        if not line:
            continue

        # Cambio de fuente: /F1 12.5 Tf
        tf_m = re.match(rb"/(F\d+)\s+[\d.]+\s+Tf", line)
        if tf_m:
            current_cmap = font_cmaps.get(tf_m.group(1).decode())
            continue

        if current_cmap is None:
            continue

        # Operador TJ: [<hex> kern <hex> ...] TJ
        tj_m = re.match(rb"\[(.*)\]\s*TJ", line, re.DOTALL)
        if tj_m:
            text = "".join(
                decode_hex_string(h.group(1), current_cmap)
                for h in re.finditer(rb"<([0-9a-fA-F]+)>", tj_m.group(1))
            )
            if text.strip():
                fragments.append(text)
            continue

        # Operador Tj: <hex> Tj
        tj_m = re.match(rb"<([0-9a-fA-F]+)>\s*Tj", line)
        if tj_m:
            text = decode_hex_string(tj_m.group(1), current_cmap)
            if text.strip():
                fragments.append(text)

    return fragments


# ---------------------------------------------------------------------------
# Extracción principal
# ---------------------------------------------------------------------------

def extract_pages(pdf_path: str) -> list[tuple[int, list[str]]]:
    """
    Extrae el texto del PDF página por página.

    Retorna una lista de (page_obj_num, [fragmentos_de_texto]).
    El orden es el de los objetos página en el PDF (suele coincidir
    con el orden visual).
    """
    data = Path(pdf_path).read_bytes()

    obj_positions = index_objects(data)
    cmap_by_obj   = build_cmap_table(data, obj_positions)
    font_by_obj   = build_font_table(data, obj_positions, cmap_by_obj)

    pages: list[tuple[int, list[str]]] = []

    for obj_num in sorted(obj_positions):
        oc = get_obj_content(data, obj_positions, obj_num)

        # Filtrar solo objetos /Type /Page (no /Pages)
        if b"/Type /Page\n" not in oc and b"/Type /Page " not in oc:
            continue
        if b"/Type /Pages" in oc:
            continue

        # Obtener recursos de fuentes
        res_m = re.search(rb"/Resources\s+(\d+)\s+0\s+R", oc)
        if not res_m:
            continue
        font_cmaps = get_font_cmaps_for_resource(
            data, obj_positions, font_by_obj, int(res_m.group(1))
        )
        if not font_cmaps:
            continue

        # Obtener content stream(s)
        contents_m = re.search(rb"/Contents\s+\[?((?:\d+\s+0\s+R\s*)+)\]?", oc)
        if not contents_m:
            continue
        content_objs = [int(x) for x in re.findall(rb"(\d+)\s+0\s+R", contents_m.group(1))]

        page_fragments: list[str] = []
        for cobj in content_objs:
            dec = get_stream_content(data, obj_positions, cobj)
            if dec:
                page_fragments.extend(decode_content_stream(dec, font_cmaps))

        if page_fragments:
            pages.append((obj_num, page_fragments))

    return pages


def extract_full_text(pdf_path: str) -> str:
    """Retorna todo el texto del PDF como un único string."""
    pages = extract_pages(pdf_path)
    lines: list[str] = []
    for _, fragments in pages:
        lines.extend(fragments)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extrae texto de un PDF usando CMaps ToUnicode (sin dependencias)."
    )
    parser.add_argument("pdf", help="Ruta al archivo PDF")
    parser.add_argument(
        "--output", "-o", help="Guardar texto en este archivo (default: stdout)"
    )
    parser.add_argument(
        "--pages", "-p", action="store_true", help="Mostrar separadores de página"
    )
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        print(f"Error: no se encontró el archivo '{args.pdf}'", file=sys.stderr)
        sys.exit(1)

    if args.pages:
        pages = extract_pages(args.pdf)
        result_parts: list[str] = []
        for i, (obj_num, fragments) in enumerate(pages, 1):
            result_parts.append(f"{'='*60}\nPágina {i} (obj {obj_num})\n{'='*60}")
            result_parts.extend(fragments)
        result = "\n".join(result_parts)
    else:
        result = extract_full_text(args.pdf)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Texto guardado en '{args.output}' ({len(result)} caracteres).")
    else:
        print(result)


if __name__ == "__main__":
    main()
