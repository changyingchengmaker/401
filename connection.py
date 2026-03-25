import requests
from urllib.parse import quote

# 你的Cookie
cookie_str = "ASP.NET_SessionId=wq2qdak4fqitt1xrsnk5cxvc; UserInfo=H4sIAAAAAAAEAKtWKi5JLCktVrIy1FEKLU4t8nRRslIyMjAysTQwtDQyUYKIOuenpGIT90vMBYlvXnx50eaTQLGCxOLi8vyiFKCYBRQARYPyc4Cq8kpzcnSUXJw889LylayiY3WUglOTS4sySyphcj756Zl5IZUFqWDXOCYn55fmlXimpOaVgBUZGYAASCYlNzNPySotMac4tRYAj1EhfsIAAAAA=; lang=zh"

# 解析cookies
cookies = {}
for item in cookie_str.split('; '):
    if '=' in item:
        k, v = item.split('=', 1)
        cookies[k] = v

# 手动构建请求体
data = f"ConditionKey={quote('学院')}&ConditionValue={quote('运输工程学院')}&pageSize=15&pageIndexNow=1&dbID=9&dbCode=Etd1&dbName={quote('博硕士学位论文数据库')}"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
}

# 发送请求
response = requests.post(
    'https://lwtj.chd.edu.cn/SingleSearch/Search',
    headers=headers,
    cookies=cookies,
    data=data.encode('utf-8')  # 关键：以字节形式发送
)

print(f"状态码: {response.status_code}")
print(f"响应长度: {len(response.text)}")
print(f"响应前200字符: {response.text[:200]}")