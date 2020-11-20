import os
import configparser

from .log import Log

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')


class Config:
    def __init__(self, section):
        self.section = section
        self.cfg = configparser.ConfigParser()
        self.log = Log('config')
        if os.path.exists(cfg_path):
            size = os.path.getsize(cfg_path)
            if size:  # 配置文件不为空，恢复默认配置
                self.cfg.read(cfg_path)
            else:
                self.log.warning('配置文件为空')
                self.restore()
        else:
            self.log.warning('配置文件不存在')
            os.mknod(cfg_path)
            self.restore()


def _config(self, option=None, convert=None):  # 获取配置，同时可以修改配置
    self.option = option
    self.convert = convert


def _get(self):
    try:
        if self.convert == 'int':
            value = self.cfg.getint(self.section, self.option)
        elif self.convert == 'float':
            value = self.cfg.getfloat(self.section, self.option)
        elif self.convert == 'bool':
            value = self.cfg.getboolean(self.section, self.option)
        else:
            value = self.cfg.get(self.section, self.option)

    except configparser.NoSectionError:
        self.log.error('配置文件，查无此[{}]'.format(self.section))
        value = None

    except configparser.NoOptionError:
        self.log.error('配置文件，查无此[{}]{}'.format(self.section, self.option))
        value = None

    except ValueError as e:
        pass
    finally:
        return value


def _write(self, value):
    if not self.cfg.has_section(self.section):  # 检查配置组是否不存在，不存在则添加配置组
        self.cfg.add_section(self.section)
        self.lgo.info('已新增[{}]'.format(self.section))
    self.cfg.set(self.section, self.option, value)
    self.cfg.write(open(cfg_path, 'w'))
    self.log.info('已设置[{}}]{}={}'.format(self.section, self.option, value))


def _remove(self, section, option):
    if self.cfg.has_section(section):  # 检查配置组是否存在，存在则删除配置项，否则不操作
        if self.cfg.remove_option(section, option):
            self.cfg.write(open(cfg_path, 'w'))
            self.log.info('已删除[{}]{}'.format(section, option))
        else:
            self.log.error('删除失败，查无此[{}]{}'.format(section, option))
    else:
        self.log.error('删除失败，查无此[{}]'.format(section))


def restore(self):
    backup = ''  # 添加默认配置
    with open(cfg_path, mode='w', encoding='utf-8') as f:
        f.write(backup)
    self.log.info('已恢复默认配置')


config = _config
config = property(_get, _write, _remove)
