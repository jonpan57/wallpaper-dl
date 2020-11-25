"""
 request(method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None)
    参数:
        method -- 请求方法
        url -- 网址
        params -- url中传递参数，字典类型{'key':'value'}，http://www.baidu.com？key=value
        data -- (optional) 字典、字节或文件对象的数据
        json -- (optional) JSON格式的数据
        headers -- (optional) 请求头
        cookies -- (optional) 字典或者CookieJar
        files -- (optional) 文件对象，上传文件
        auth -- (optional) 身份验证方案
        timeout (float or tuple) -- (optional) 超时参数
        allow_redirects (bool) -- (optional) 是否允许跳转，默认为True
        proxies -- (optional) 代理设置，字典类型
        stream -- (optional) 大文件下载，把文件一点一点的下载,如果这个值为false，则全部写到内存中
        verify -- (optional) 是否验证SSL，用于https
        cert -- (optional) 证书参数，告诉request去这个地方去下载cert

"""
