import os
import configparser

import log

log = log.Log('config')
dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')


def restore():
    backup = ''  # 添加默认配置
    with open(cfg_path, mode='w', encoding='utf-8') as f:
        f.write(backup)
    log.info('已恢复默认配置')


def _initial():
    if os.path.exists(cfg_path):
        if not os.path.getsize(cfg_path):
            log.warning('配置文件为空')
            restore()
    else:
        log.warning('配置文件不存在')
        restore()


_initial()


class Config:
    def __init__(self, section):
        self.section = section
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    def get(self, option, convert=None):
        self._get(option, convert)

    def set(self, option, value):
        self._write(option, value)

    def delete(self, option):
        self._remove_option(option)

    def __getitem__(self, option):
        if type(option) is str:
            return self._get(option, None)
        elif type(option) is tuple:
            return self._get(option[0], option[1])

    def __setitem__(self, option, value):
        self._write(option, value)

    def __delitem__(self, option):
        self._remove_option(option)

    def _get(self, option, convert):
        try:
            if convert in ['int', 'Int', 'INT', 'integer', 'Integer', 'INTEGER', 'i', 'I']:
                return self.cfg.getint(self.section, option)
            elif convert in ['float', 'Float', 'FLOAT', 'f', 'F']:
                return self.cfg.getfloat(self.section, option)
            elif convert in ['bool', 'Bool', 'BOOL', 'boolean', 'Boolean', 'BOOLEAN', 'b', 'B']:
                return self.cfg.getboolean(self.section, option)
            else:
                return self.cfg.get(self.section, option)

        except configparser.NoSectionError:
            log.error('配置文件，查无此[{}]'.format(self.section))

        except configparser.NoOptionError:
            log.error('配置文件，查无此[{}]{}'.format(self.section, option))

        except ValueError:
            log.error('装换类型不相符')

    def _write(self, option, value):
        if not self.cfg.has_section(self.section):  # 检查配置组是否不存在，不存在则添加配置组
            self.cfg.add_section(self.section)
            log.info('已新增[{}]'.format(self.section))
        self.cfg.set(self.section, option, value)
        self.cfg.write(open(cfg_path, 'w'))
        log.info('已设置[{}}]{}={}'.format(self.section, option, value))

    def _remove_option(self, option):
        if type(option) is str:
            if self.cfg.remove_option(self.section, option):
                self.cfg.write(open(cfg_path, 'w'))
                log.info('已删除[{}]{}'.format(self.section, option))
            else:
                log.error('删除失败，查无此[{}]{}'.format(self.section, option))
        else:
            log.error('输入参数异常')

    def _remove_section(self):
        if self.cfg.remove_section(self.section):
            self.cfg.write(open(cfg_path, 'w'))
        else:
            log.error('删除失败，查无此[{}]'.format(self.section))

    def remove(self):
        self._remove_section()
