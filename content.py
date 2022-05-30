from os import path, makedirs, rmdir, remove, walk
from os.path import splitext
from time import time
from log import logger


DIR = 'users-data/'
SAVE_TIME = 10


@logger.catch
def save_image(username: str, chat_id: int, filename: str, file: bytes) -> str:
    dir_name = DIR + username + '_' + str(chat_id)
    if not path.exists(dir_name):
        makedirs(dir_name)

    new_filename = dir_name + '/' + str(int(time())) + '_' + filename
    with open(new_filename, 'wb' ) as new_file:
        new_file.write(file)

    return new_filename


@logger.catch
def save_text(username: str, chat_id: int, msg: str) -> None:
    dir_name = DIR + username + '_' + str(chat_id)
    if not path.exists(dir_name):
        makedirs(dir_name)

    with open(dir_name + '/text.txt', 'a' ) as text_file:
        text_file.write(msg + '\n')


@logger.catch
def get_content(username: str, chat_id: int) -> dict:
    IMG_FORMATS = ('.png', '.jpg')
    VIDEO_FORMATS = ('.mp4', '.avi', '.gif')
    result = {
        'text': None,
        'photos': [],
        'videos': []
    }

    dir_name = DIR + username + '_' + str(chat_id)
    for _, _, files in walk(dir_name):
        for name in files:
            filename = dir_name + '/' + name
            _, ext = splitext(name)
            ext = ext.lower()

            if ext == '.txt':
                with open(filename) as textfile:
                    result['text'] = textfile.read()
            elif ext in IMG_FORMATS:
                result['photos'].append(filename)
            elif ext in VIDEO_FORMATS:
                result['videos'].append(filename)

    return result


@logger.catch
def remove_content(username: str, chat_id: int) -> None:
    dir_name = DIR + username + '_' + str(chat_id)

    try:
        for _, _, files in walk(dir_name):
            for name in files:
                filename = dir_name + '/' + name
                remove(filename)

        rmdir(dir_name)
    except Exception as e:
        logger.exception('Ошибка удаления файлов: %s' % e)


def isEmptyContent(username: str, chat_id: int) -> bool:
    _content = get_content(username, chat_id)
    return _content['text'] is None and len(_content['photos']) == 0 and len(_content['videos']) ==  0


def count_user_media(username: str, chat_id: int) -> int:
     _content = get_content(username, chat_id)
     return len(_content['photos']) + len(_content['videos'])


def set_save_media_time(username: str, chat_id: int) -> bool:
    dir_name = DIR + username + '_' + str(chat_id)
    if not path.exists(dir_name + '/time'):
        with open(dir_name + '/time', 'w') as timefile:
            timefile.write( str(time()) )
        return True

    with open(dir_name + '/time') as timefile:
        old_time = float( timefile.read() )

    if time() - old_time < SAVE_TIME:
        return False

    with open(dir_name + '/time', 'w') as timefile:
        timefile.write( str(time()) )

    return True
