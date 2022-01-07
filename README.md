#### Скрипт для создания резервной копии папки с файлами.

##### usage: backupctl.py [-h] [-a arc_type] [-j path_to_log] DIR_FROM DIR_TO

##### positional arguments:
#####   DIR_FROM        Путь (без кавычек) до папки, которую надо архивировать
#####   DIR_TO          Путь (без кавычек) до папки, в которую положить архив
#####
##### optional arguments:
#####   -h, --help      show this help message and exit
#####   -a arc_type     Алгоритм сжатия (gztar, zip. default: gztar)
#####   -j path_to_log  Путь (без кавычек, должен существовать) до журнала вызовов journal.csv, default: каталог скрипта
