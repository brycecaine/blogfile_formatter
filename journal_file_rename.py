import os
import re
import sys

print sys.argv

for filename in os.listdir(sys.argv[2]):
    try:
        date_str = re.search(r'(\d{2,4}[_.-]{1}\d{2}[_.-]{1}\d{2,4})', filename).group().replace('_', '-').replace('.', '-')
        extension = re.search(r'(\w{2,4})$', filename).group()
        filename_str = filename.replace('.%s' % extension, '')

        if extension == 'md':
            extension = 'txt'

        newname = '%s-journal-%s-%s.%s' % (date_str, sys.argv[1], filename_str, extension)

        if os.path.exists(newname):
            print 'Destination file %s exists; skipped' % newname
            continue

        else:
            print '%s to %s' % (filename, newname)
            os.rename(filename, newname)

    except AttributeError:
        print 'bad filename'