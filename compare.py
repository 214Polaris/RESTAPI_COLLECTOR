import json

# 读取两个JSON文件
with open('a.json', 'r') as file1, open('b.json', 'r') as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# 创建用于存储清洗后数据的列表
cleaned_data1 = []
cleaned_data2 = []

# 将数据按照 domain 和 path 进行匹配
for api1 in data1:
    for api2 in data2:
        if api1["Domain"] == api2["Domain"] and api1["Path"].split('?')[0] == api2["Path"].split('?')[0]:

            # 转换参数为集合以便比较
            params_set1 = {(param["key"]) for param in api1["Params"]}
            params_set2 = {(param["key"]) for param in api2["Params"]}

            # 去重
            flag = False
            for entry in cleaned_data1:
                if entry['Path'] == api1["Path"]:
                    flag = True
                    break

            if flag is True:
                break

            # 检查参数是否不同
            if params_set1 != params_set2:
                # 参数不同，保留这个API
                cleaned_data1.append(api1)
                cleaned_data2.append(api2)
                break

with open('a_new.json', 'w') as outfile1, open('b_new.json', 'w') as outfile2:
    json.dump(cleaned_data1, outfile1, indent=4)
    json.dump(cleaned_data2, outfile2, indent=4)
