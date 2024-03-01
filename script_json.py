import mitmproxy
import urllib.parse
import json

data_table1 = []


def response(flow: mitmproxy.http.HTTPFlow):
    # 获取请求的域名、路径和查询参数
    method = flow.request.method
    domain = flow.request.host
    path = flow.request.path
    query_params = flow.request.query

    # 获取请求的 cookies
    cookies = flow.request.cookies

    content_type = flow.request.headers.get("Content-Type")

    # 去除路径中'?'符号以后的内容
    if '?' in path:
        path = path.split('?')[0]

    # 将 cookies 添加到 params 列表中
    params = []
    for key, value in query_params.items():
        params.append({'key': key, 'value': value})

    for key, value in cookies.items():
        params.append({'key': f'{key}', 'value': f'{value}'})

    if method == "POST":
        if content_type == "application/json":
            data = flow.request.content.decode('utf-8')
            data = json.loads(data)
            for key, value in data.items():
                params.append({'key': f'{key}', 'value': f'{value}'})
        elif content_type == "application/x-www-form-urlencoded":
            data = flow.request.content.decode('utf-8', errors='ignore')
            data = urllib.parse.parse_qs(data)
            for key, values in data.items():
                for value in values:
                    params.append({'key': f'{key}', 'value': f'{value}'})


    # 更新数据，按路径，参数去重
    for entry in data_table1:
        if entry['Path'] == path and entry['Params'] == params:
            # break掉
            break
    else:
        # 如果路径不存在，创建新的记录
        data_table1.append({'Domain': domain, 'Path': path, 'Params': params})


# 最后，保存数据为JSON文件
def done():
    with open('result.json', 'w', encoding='utf-8') as file1:
        json.dump(data_table1, file1, ensure_ascii=False, indent=4)
