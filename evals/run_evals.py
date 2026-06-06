#!/usr/bin/env python3
from pathlib import Path
print('Manual eval prompts available:')
for p in Path(__file__).resolve().parent.joinpath('prompts').glob('*.md'):
    print('-', p.name)
