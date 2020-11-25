def parse_bytes(value, default=0, suffixes='bkmgtp'):
    # 将输入的内容（500K，2.5M）转化为字节的int
    try:
        last = value[-1].lower()
    except(TypeError, KeyError, IndexError):
        return default

    if last in suffixes:
        mul = 1024 ** suffixes.index(last)
        value = value[:-1]
    else:
        mul = 1

    try:
        return round(float(value) * mul)
    except ValueError:
        return default
