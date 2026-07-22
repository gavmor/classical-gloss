import sys
import json
import re
import argparse
import xml.etree.ElementTree as ET

def extract_targets(xml_path, pattern, chunk_size, out_prefix):
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip all xmlns attributes to completely avoid namespace issues in ET
    content = re.sub(r'\sxmlns(:\w+)?="[^"]+"', '', content)
    
    root = ET.fromstring(content)
    stream = []
    
    current_book = "?"
    current_page = "?"
    current_line = "?"
    
    def walk(node):
        nonlocal current_book, current_page, current_line
        
        # In Perseus TEI, books are often div type="textpart" subtype="book" n="1"
        if node.tag == 'div' and node.get('subtype') == 'book':
            current_book = node.get('n', '?')
            stream.append({"cite": True, "book": current_book, "page": current_page, "line": current_line})
        elif node.tag == 'milestone':
            unit = node.get('unit')
            if unit == 'page':
                current_page = node.get('n', '?')
            elif unit == 'line':
                current_line = node.get('n', '?')
            stream.append({"cite": True, "book": current_book, "page": current_page, "line": current_line})
        
        if node.text and node.text.strip():
            parts = re.split(r'([\s\.\;\·\,\·\·])', node.text)
            for p in parts:
                if p:
                    stream.append(p)
        
        for child in node:
            walk(child)
            if child.tail and child.tail.strip():
                parts = re.split(r'([\s\.\;\·\,\·\·])', child.tail)
                for p in parts:
                    if p:
                        stream.append(p)
    
    walk(root)
    
    sentences = []
    current_sentence = []
    sentence_start_cite = None
    
    regex = re.compile(pattern, re.IGNORECASE)
    
    for item in stream:
        if isinstance(item, dict):
            # Update citation context before sentence starts
            has_text = any(isinstance(x, str) and x.strip() for x in current_sentence)
            if not has_text:
                sentence_start_cite = item
        else:
            current_sentence.append(item)
            if item in ['.', ';', '·', '·']:
                text = "".join(current_sentence).strip()
                text = re.sub(r'\s+', ' ', text)
                
                if regex.search(text):
                    book = sentence_start_cite.get('book', '?') if sentence_start_cite else '?'
                    page = sentence_start_cite.get('page', '?') if sentence_start_cite else '?'
                    line = sentence_start_cite.get('line', '?') if sentence_start_cite else '?'
                    cite_str = f"Bk. {book} (Bekker {page}{line})"
                    sentences.append({
                        "citation": cite_str,
                        "greek": text
                    })
                
                current_sentence = []
                # Don't reset sentence_start_cite to None, keep the last known citation context
                sentence_start_cite = {"cite": True, "book": current_book, "page": current_page, "line": current_line}
    
    print(f"Extracted {len(sentences)} sentences matching '{pattern}'.")
    
    if len(sentences) > 0:
        for i in range(0, len(sentences), chunk_size):
            chunk = sentences[i:i+chunk_size]
            out_file = f"{out_prefix}_{i//chunk_size}.json"
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(sentences)//chunk_size + (1 if len(sentences)%chunk_size else 0)} chunks.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', required=True)
    parser.add_argument('--pattern', required=True)
    parser.add_argument('--chunk-size', type=int, default=10)
    parser.add_argument('--out-prefix', default='chunk')
    args = parser.parse_args()
    extract_targets(args.xml, args.pattern, args.chunk_size, args.out_prefix)
