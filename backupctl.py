#!/usr/bin/env python3

from os import getcwd, path
import sys
from datetime import datetime, timezone
from shutil import make_archive
import csv
import argparse

# архивируемая папка 
src_dir = None
# папка назначения
dst_dir = None
# имя архива
arc_name = None
# имя с расширением
full_arc_name = None
# zip, default:gztar
arc_type = 'gztar'
# имя лога
log_name = 'journal.csv'
# путь к логу
full_log_name = None
backup_result = None

log_fields = {
    'source_dir_path' : '',
    'archived_file_path' : '',
    'run_time' : '',
    'result' : ''
}


def get_arc_name(src_dir: str) -> str:
    
    name = path.basename(src_dir) \
           + "_" \
           + datetime.now(timezone.utc).isoformat(sep='_', timespec='seconds')
    return name


def pack_dir(src_dir: str, full_arc_name: str, arc_type: str) -> bool:

    types = ('gztar', 'zip')
    if not arc_type in types:
        print('Неподдерживаемый тип архива:', arc_type,
              'Будет использован gztar')
        arc_type = 'gztar'
    
    try:
        make_archive(full_arc_name, arc_type, root_dir = src_dir)
    except Exception as e:
        print('Ошибка при создании архива:\n', str(e))
        return False
    else:
        print('Создан архив:\n', full_arc_name + "." + arc_type)
        return True


def write_log(full_log_name: str, log_fields: dict) -> bool:

    try:
        with open(full_log_name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=log_fields)
            writer.writeheader()
            writer.writerow(log_fields)
    except Exception as e:
        print('Ошибка при создании файла журнала:\n', str(e))
        return False
    else:
        print(f'Создан файл журнала:\n {full_log_name}')
        return True


parser = argparse.ArgumentParser(
             description='Скрипт для создания резервной копии папки с файлами.')
parser.add_argument('dir_from', metavar='DIR_FROM',  
                    help='Путь (без кавычек) до папки, \
                    которую надо архивировать')
parser.add_argument('dir_to', metavar='DIR_TO', 
                    help='Путь (без кавычек) до папки, \
                    в которую положить архив')
parser.add_argument('-a', default='gztar', metavar='arc_type', dest='arc_type', 
                    help='Алгоритм сжатия (gztar, zip. default: gztar)')
parser.add_argument('-j', metavar='path_to_log', dest='log_path', 
                    help='Путь (без кавычек, должен существовать) \
                    до журнала вызовов journal.csv, default: каталог скрипта')

args = vars(parser.parse_args())

src_dir = path.abspath(args['dir_from'])
dst_dir = path.abspath(args['dir_to'])
arc_type = args['arc_type']

if args['log_path'] is not None:
    # в указанный каталог
    full_log_name = path.join(path.abspath(args['log_path']), log_name)
else:
    # в каталог по умолчанию
    full_log_name = path.join(path.abspath(path.dirname(sys.argv[0])), log_name)

arc_name = get_arc_name(src_dir)
full_arc_name = path.join(dst_dir, arc_name)
backup_result = pack_dir(src_dir, full_arc_name, arc_type)

log_fields['source_dir_path'] = src_dir
log_fields['run_time'] = datetime.now(timezone.utc).\
                         isoformat(sep='_', timespec='minutes')
if backup_result:
    log_fields['archived_file_path'] =  full_arc_name + "." + arc_type
    log_fields['result'] = 'success'
else:
    log_fields['archived_file_path'] =  ""
    log_fields['result'] = 'fail'

write_log(full_log_name, log_fields)
