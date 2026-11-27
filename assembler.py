#!/usr/bin/env python3
"""Hack assembler (Nand2Tetris Project 6) - two-pass. Usage: python assembler.py File.asm"""
import sys

COMP = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000',
        '!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111',
        'A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011',
        'A-D':'0000111','D&A':'0000000','D|A':'0010101'}
# a=1 variants: replace A by M and set the a-bit
COMP.update({k.replace('A', 'M'): '1' + v[1:] for k, v in list(COMP.items()) if 'A' in k})
# commutative forms
for k, v in list(COMP.items()):
    if k in ('D+A', 'D&A', 'D|A', 'D+M', 'D&M', 'D|M'):
        COMP[k[2] + k[1] + k[0]] = v
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}


def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(lines):
    sym = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384, 'KBD': 24576}
    sym.update({'R%d' % i: i for i in range(16)})
    code = [l for l in map(clean, lines) if l]

    # Pass 1: labels -> address of the next real instruction
    instrs, pc = [], 0
    for l in code:
        if l.startswith('('):
            sym[l[1:-1]] = pc
        else:
            instrs.append(l)
            pc += 1

    # Pass 2: translate; unseen symbols become variables from RAM[16]
    nxt, out = 16, []
    for l in instrs:
        if l.startswith('@'):
            v = l[1:]
            if v.isdigit():
                n = int(v)
            else:
                if v not in sym:
                    sym[v] = nxt
                    nxt += 1
                n = sym[v]
            out.append(format(n, '016b'))
        else:
            dest, rest = l.split('=', 1) if '=' in l else ('', l)
            comp, jmp = rest.split(';', 1) if ';' in rest else (rest, '')
            out.append('111' + COMP[comp] + DEST[dest] + JUMP[jmp])
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python assembler.py File.asm')
    path = sys.argv[1]
    with open(path) as f:
        result = assemble(f)
    outpath = path.rsplit('.', 1)[0] + '.hack'
    with open(outpath, 'w') as f:
        f.write('\n'.join(result) + '\n')
    print('Wrote %s (%d instructions)' % (outpath, len(result)))
