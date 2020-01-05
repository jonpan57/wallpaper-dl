import configparser

cfg = configparser.ConfigParser()


def getConfig(section, option):
    cfg.read('cfg.ini')
    value = cfg.get(section, option)
    return value


def setConfig(section, option):
    cfg.set('downloader', 'page', 12)
    cfg.write('cfg.ini')
