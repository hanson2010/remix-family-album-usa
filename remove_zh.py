#!/usr/bin/env python

import re
import os, sys

from zhon.hanzi import punctuation


def get_files(top):
   ret = []
   for root, dirs, files in os.walk(top):
       for filename in files:
           ret.append(os.path.join(root, filename))
   return ret


def process(text):
    ret = re.sub(r'[\u4e00-\u9fa5]+.*$', '', text, flags=re.MULTILINE)
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
        path = sys.argv[0]
        command = path[path.rfind('/')+1:]
        sys.exit(f'Usage: {command} input_dir output_dir')
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_dir):
        sys.exit(f'Directory not found: {input_dir}')

    input_files = get_files(input_dir)
    for input_file in input_files:
        text = ''
        with open(input_file) as f:
	        print(f'Processing input file: {input_file}')
	        text = process(f.read())

        output_file = output_dir + '/' + input_file[input_file.rfind('/')+1:]
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            print(f'Writing to output file: {output_file}')
            f.write(text)
            f.close()

    print(f'\nProcessed {len(input_files)} file(s)')

