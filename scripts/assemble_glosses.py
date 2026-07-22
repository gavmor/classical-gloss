import os
import argparse
import glob

def assemble(chunks_pattern, target_file, heading):
    files = sorted(glob.glob(chunks_pattern))
    if not files:
        print(f"No files matching {chunks_pattern} found.")
        return
        
    content = f"\n## {heading}\n\n"
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as inf:
            content += inf.read() + "\n"
            
    with open(target_file, 'a', encoding='utf-8') as outf:
        outf.write(content)
        
    print(f"Appended {len(content)} bytes to {target_file} from {len(files)} chunk(s).")
    
    # Clean up the output markdown chunks and json chunks
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--chunks', required=True, help='Glob pattern for markdown chunks, e.g. praxis_out_*.md')
    parser.add_argument('--target', required=True, help='Target markdown file to append to')
    parser.add_argument('--heading', required=True, help='Heading to insert before the assembled content')
    args = parser.parse_args()
    assemble(args.chunks, args.target, args.heading)
