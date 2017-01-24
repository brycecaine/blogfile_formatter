from dateutil.parser import parse
import os
import re
import sys


def get_date_str(filename):
    date_str = ''
    regex = '(\d{2,4}[_.-]{1}\d{2}[_.-]{1}\d{2,4})'

    try:
        date_str = re.search(regex, filename).group()
    except AttributeError:
        pass

    return date_str


def get_date(date_str):
    filename_date = ''
    clean_date_str = date_str.replace('_', '-').replace('.', '-')

    try:
        filename_date = parse(clean_date_str)
    except ValueError:
        pass

    return filename_date


def is_formatted(filename):
    date_str = ''
    formatted = False

    regex = '^(\d{4}[-]{1}\d{2}[-]{1}\d{2})'

    try:
        date_str = re.search(regex, filename).group()
    except AttributeError:
        pass

    if date_str:
        formatted = True

    return formatted


folder = sys.argv[1] 

try:
    edit_mode = sys.argv[2].lower() == 'y'
except IndexError:
    edit_mode = False

path, folder_name = os.path.split(folder)
filenames = os.listdir(folder)

for filename in filenames:
    newname = 'n/a'

    if not is_formatted(filename):
        date_str = get_date_str(filename)

        if date_str:
            raw_filename = filename.replace(date_str, '')
            extension = re.search(r'(\w{2,4})$', raw_filename).group()
            trim_filename = raw_filename.replace('.%s' % extension, '')
            clean_filename = trim_filename.replace('_', '-').replace('.', '-') \
                .replace(' ', '-').replace('--', '-').rstrip('-').lower()
            file_date = get_date(date_str)

            if file_date:
                file_date_str = file_date.strftime('%Y-%m-%d')
                newname = '%s-journal-%s-%s.%s' % (
                    file_date_str, folder_name, clean_filename, extension)

                if os.path.exists(newname):
                    outcome = 'Destination file exists;   not renamed  '
                    continue

                else:
                    if edit_mode:
                        filename_full_path = '%s/%s' % (folder, filename)
                        newname_full_path = '%s/%s' % (folder, newname)
                        os.rename(filename_full_path, newname_full_path)
                        outcome = 'Renamed'

                    else:
                        outcome = 'Not in edit mode;          not renamed  '
            else:
                outcome = 'Invalid date;              not renamed  '
        else:
            outcome = 'No date found;             not renamed  '
    else:
        outcome = 'Already formatted;         not renamed  '

    print('%s: %s -- to -- %s' % (outcome, filename, newname))
