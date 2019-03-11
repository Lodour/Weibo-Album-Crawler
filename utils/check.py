from pathlib import Path
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import os
import sys

def verify_or_delete(filename):
    try:
        Image.open(filename).load()
    except OSError:
        return False
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Remove Broken Images\nUsage: python check.py <dir>')
        exit(-1)
    filenames = list(Path(sys.args[1]).rglob('*.*'))
    with ProcessPoolExecutor() as executor:
        broken, total = 0, len(filenames)
        jobs = executor.map(verify_or_delete, filenames)
        for i, (filename, verified) in enumerate(zip(filenames, jobs)):
            if not verified:
                broken += 1
                os.system('rm "%s"' % filename)
            print('Checking %d/%d, %d deleted...' %
                  (i + 1, total, broken), end='\r')
    print('\nDone.')
