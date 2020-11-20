import os
import configparser

from log import Log

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')


class Config:
    def __init__(self, section):
        self.section = section
        self.cfg = configparser.ConfigParser()
        self.log = Log('config')
        if os.path.exists(cfg_path):
            if os.path.getsize(cfg_path):
                self.cfg.read(cfg_path)
            else:  # 配置文件为空，恢复默认配置
                self.log.warning('配置文件为空')
                self.restore()
        else:  # 配置文件不存在，创建默认配置
            self.log.warning('配置文件不存在')
            self.restore()

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
            print(1)
            # self.log.error('配置文件，查无此[{}]'.format(self.section))

        except configparser.NoOptionError:
            print(2)
            # self.log.error('配置文件，查无此[{}]{}'.format(self.section, option))

        except ValueError:
            print(3)
            # self.log.error('装换类型不相符')

    def _write(self, option, value):
        if not self.cfg.has_section(self.section):  # 检查配置组是否不存在，不存在则添加配置组
            self.cfg.add_section(self.section)
            # self.log.info('已新增[{}]'.format(self.section))
        self.cfg.set(self.section, option, value)
        self.cfg.write(open(cfg_path, 'w'))
        # self.log.info('已设置[{}}]{}={}'.format(self.section, option, value))

    def _remove_option(self, option):
        if self.cfg.remove_option(self.section, option):
            self.cfg.write(open(cfg_path, 'w'))
            # self.log.info('已删除[{}]{}'.format(section, option))
        else:
            pass
            # self.log.error('删除失败，查无此[{}]{}'.format(section, option))

    def _remove_section(self):
        if self.cfg.remove_section(self.section):
            self.cfg.write(open(cfg_path, 'w'))

    def restore(self):
        backup = ''  # 添加默认配置
        with open(cfg_path, mode='w', encoding='utf-8') as f:
            f.write(backup)
        self.log.info('已恢复默认配置')
