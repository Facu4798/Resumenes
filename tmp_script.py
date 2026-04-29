python3 << 'PYEOF'
import re, zlib

with open('/mnt/c/Users/facum/Resumenes/7_semestre/deep_learning/teoria por clases/Clase 3.pdf', 'rb') as f:
    data = f.read()

def parse_cmap(cmap_data):
    mapping = {}
    for section in re.findall(rb'beginbfchar(.*?)endbfchar', cmap_data, re.DOTALL):
        for cid_hex, uni_hex in re.findall(rb'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', section):
            cid = int(cid_hex, 16)
            uni_bytes = bytes.fromhex(uni_hex.decode())
            try:
                if len(uni_bytes) == 4:
                    high = int.from_bytes(uni_bytes[:2], 'big')
                    low = int.from_bytes(uni_bytes[2:], 'big')
                    if 0xD800 <= high <= 0xDBFF and 0xDC00 <= low <= 0xDFFF:
                        mapping[cid] = chr(0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00))
                    else:
                        mapping[cid] = uni_bytes.decode('utf-16-be')
                else:
                    mapping[cid] = uni_bytes.decode('utf-16-be')
            except:
                pass
    return mapping

obj_pattern = re.compile(rb'(\d+)\s+0\s+obj\b')
obj_positions = {}
pos = 0
while True:
    m = obj_pattern.search(data, pos)
    if not m:
        break
    obj_positions[int(m.group(1))] = m.start()
    pos = m.end()

def get_obj_content(obj_num):
    if obj_num not in obj_positions:
        return b''
    pos = obj_positions[obj_num]
    endobj = data.find(b'endobj', pos)
    return data[pos:endobj] if endobj != -1 else b''

def get_stream_content(obj_num):
    if obj_num not in obj_positions:
        return None
    pos = obj_positions[obj_num]
    endobj = data.find(b'endobj', pos)
    stream_m = re.search(rb'stream\r?\n', data[pos:endobj])
    if not stream_m:
        return None
    stream_start = pos + stream_m.end()
    stream_end = data.find(b'\nendstream', stream_start)
    if stream_end == -1:
        return None
    content = data[stream_start:stream_end]
    try:
        return zlib.decompress(content)
    except:
        return content

# Build everything
cmap_by_obj = {}
for obj_num in obj_positions:
    sc = get_stream_content(obj_num)
    if sc and (b'beginbfchar' in sc or b'beginbfrange' in sc):
        cmap_by_obj[obj_num] = parse_cmap(sc)

font_objs = {}
for obj_num in obj_positions:
    oc = get_obj_content(obj_num)
    if b'/Type /Font' in oc or b'/Type\n/Font' in oc:
        tou_m = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', oc)
        if tou_m:
            font_objs[obj_num] = int(tou_m.group(1))

def parse_font_dict_from_obj(res_obj_num):
    oc = get_obj_content(res_obj_num)
    font_m = re.search(rb'/Font\s*<<(.*?)>>', oc, re.DOTALL)
    if not font_m:
        return {}
    result = {}
    for fname, fobj_num in re.findall(rb'/(F\d+)\s+(\d+)\s+0\s+R', font_m.group(1)):
        fobj = int(fobj_num)
        if fobj in font_objs and font_objs[fobj] in cmap_by_obj:
            result[fname.decode()] = cmap_by_obj[font_objs[fobj]]
    return result

def decode_hex_string(hex_str, cmap):
    result = []
    hs = hex_str.decode() if isinstance(hex_str, bytes) else hex_str
    for i in range(0, len(hs), 4):
        if i + 4 <= len(hs):
            cid = int(hs[i:i+4], 16)
            ch = cmap.get(cid, '')
            result.append(ch)
    return ''.join(result)

def decode_stream(dec, font_cmaps):
    """Full stream decoder - returns list of text items"""
    results = []
    current_cmap = None
    current_y = None
    prev_y = None
    
    for line in dec.split(b'\n'):
        line = line.strip()
        if not line:
            continue
        
        # Font switch
        tf_m = re.match(rb'/(F\d+)\s+[\d.]+\s+Tf', line)
        if tf_m:
            current_cmap = font_cmaps.get(tf_m.group(1).decode())
            continue
        
        # TJ
        tj_m = re.match(rb'\[(.*)\]\s*TJ', line, re.DOTALL)
        if tj_m and current_cmap:
            parts = []
            for hex_m in re.finditer(rb'<([0-9a-fA-F]+)>', tj_m.group(1)):
                decoded = decode_hex_string(hex_m.group(1), current_cmap)
                parts.append(decoded)
            text = ''.join(parts).strip()
            if text:
                results.append(text)
    
    return results

# Process all pages
pages = []
for obj_num in sorted(obj_positions.keys()):
    oc = get_obj_content(obj_num)
    if b'/Type /Page\n' not in oc and b'/Type /Page ' not in oc:
        continue
    if b'/Type /Pages' in oc:
        continue
    
    # Get resources
    res_m = re.search(rb'/Resources\s+(\d+)\s+0\s+R', oc)
    if not res_m:
        continue
    res_obj = int(res_m.group(1))
    font_cmaps = parse_font_dict_from_obj(res_obj)
    
    if not font_cmaps:
        continue
    
    # Get contents
    contents_m = re.search(rb'/Contents\s+\[?((?:\d+\s+0\s+R\s*)+)\]?', oc)
    if not contents_m:
        continue
    
    content_objs = [int(x) for x in re.findall(rb'(\d+)\s+0\s+R', contents_m.group(1))]
    
    page_text = []
    for cobj in content_objs:
        dec = get_stream_content(cobj)
        if dec:
            texts = decode_stream(dec, font_cmaps)
            page_text.extend(texts)
    
    if page_text:
        pages.append((obj_num, res_obj, page_text))

print(f"Pages decoded: {len(pages)}")
# Print all pages
for page_obj, res_obj, texts in pages:
    print(f"\n{'='*60}")
    print(f"Page obj {page_obj} (resources: {res_obj}):")
    print('\n'.join(texts))
PYEOF