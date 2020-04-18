import configparser

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

i = cfg.has_option('extractor', 'timeout')
# j = cfg.get('extractor', 'timeout')
print(i)
# print(j)