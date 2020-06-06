import os
import configparser

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')
cfg = configparser.ConfigParser()
cfg.read(cfg_path)


def get(section, option, convert):
    try:
        if convert == 'str':
            value = cfg.get(section, option)
        elif convert == 'int':
            value = cfg.getint(section, option)
        elif convert == 'float':
            value = cfg.getfloat(section, option)
        elif convert == 'bool':
            value = cfg.getboolean(section, option)
        else:
            raise ValueError('Invalid typecast' + convert)
    except ValueError as e:
        if 'Not a boolean'.find(str(e)):
            print(1)
    finally:
        pass

get('downloader', 'temp', 'bool')
