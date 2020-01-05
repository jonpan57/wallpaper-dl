import configparser

cfg_path = 'cfg.ini'  # 配置文件路径


class Config:
    def __init__(self, section, option):
        self.__cfg = configparser.ConfigParser()  # 创建ConfigParser对象
        self.__cfg.read(cfg_path)  # 读取配置文件

        self.__section = section  # 配置组
        self.__option = option  # 配置项

    @property
    def value(self):  # gettter方式获取配置值
        # 检查配置项是否存在，存在返回配置值，否则返回空值
        if self.__cfg.has_option(self.__section, self.__option):
            return self.__cfg.get(self.__section, self.__option)
        else:
            return None

    @value.setter
    def value(self, value):  # settter方式设置配置值
        # 检查配置组是否不存在，不存在则添加配置组
        if not self.__cfg.has_section(self.__section):
            self.__cfg.add_section(self.__section)
        self.__cfg.set(self.__section, self.__option, value)  # 设置配置值
        self.__cfg.write(open(cfg_path, 'w'))  # 写入配置文件


test = Config('test', 'test')
test.value = 'hahaha'
print(test.value)
