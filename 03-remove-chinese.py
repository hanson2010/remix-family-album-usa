#!/usr/bin/env python

import re
import os, sys

from zhon.hanzi import punctuation


def get_files(top):
    ret = []
    for root, _, files in os.walk(top):
        for filename in files:
            ret.append(os.path.join(root, filename))
    return ret


def process(text):
    ret = re.sub(r'[一-龥]+.*$', '', text, flags=re.MULTILINE)
    ret = re.sub(fr'[{punctuation}]+.*$', '', ret, flags=re.MULTILINE)
    ret = re.sub(r'(^[ \t]*|[ \t]*$)','', ret, flags=re.MULTILINE)
    ret = re.sub(r'\n\s*\n','\n\n', ret, flags=re.MULTILINE)
    return ret


if __name__ == '__main__':
    title = '** Remove Chinese characters and followings **'
    print('*' * len(title))
    print(title)
    print('*' * len(title) + '\n')

    if len(sys.argv) < 3:
        command = os.path.basename(sys.argv[0])
        sys.exit(f'Usage: {command} input_dir output_dir')
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_dir):
        sys.exit(f'Directory not found: {input_dir}')

    input_files = get_files(input_dir)
    for input_file in input_files:
        with open(input_file, encoding='utf-8') as f:
            print(f'Processing input file: {input_file}')
            text = process(f.read())

        output_file = os.path.join(output_dir, os.path.basename(input_file))
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            print(f'Writing to output file: {output_file}')
            f.write(text)

    print(f'\nProcessed {len(input_files)} file(s)')

