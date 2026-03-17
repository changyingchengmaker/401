import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import quote, urlencode

# ===== 从cURL中提取的信息 =====
COOKIE_STRING = 'ASP.NET_SessionId=wq2qdak4fqitt1xrsnk5cxvc; UserInfo=H4sIAAAAAAAEAKtWKi5JLCktVrIy1FEKLU4t8nRRslIyMjAysTQwtDQyUYKIOuenpGIT90vMBYlvXnx50eaTQLGCxOLi8vyiFKCYBRQARYPyc4Cq8kpzcnSUXJw889LylayiY3WUglOTS4sySyphcj756Zl5IZUFqWDXOCYn55fmlXimpOaVgBUZGYAASCYlNzNPySotMac4tRYAj1EhfsIAAAA=; lang=zh'

# 解析Cookie
cookies = {}
for item in COOKIE_STRING.split('; '):
    if '=' in item:
        key, value = item.split('=', 1)
        cookies[key] = value

def get_form_data(page=2, college='运输工程学院'):
    """返回指定页码的表单数据"""
    return {
        'ConditionKey': '学院',
        'ConditionValue': college,
        'SubConditionQuery': '2',
        'beforeQueryValue': '2',
        'beforeConditionValue': college,
        'beforeConditionKey': '学院',
        'beforecheckedCatID': '',
        'beforeselectedCatTypeID': '',
        'currentSubid': '0',
        'checkedCatID': '',
        'selectedCatTypeID': '',
        'pageSize': '15',
        'pageIndexNow': str(page),
        'sortField': '',
        'sortFieldBefore': '',
        'sortInit': '',
        'sortDescAsc': '',
        'listOrabst': '',
        'dbID': '9',
        'dbCode': 'Etd1',
        'dbName': '博硕士学位论文数据库',
        'MediaType': '0',
        'AutoLoad': '0',
        'Field': '',
        'Value': '',
        'Sub': '',
        'SubConditionType0': '0',
        'SubConditionKey0': '学号',
        'SubConditionValue0': '',
        'X-Requested-With': 'XMLHttpRequest',
    }

# 请求头 - 确保所有值都是ASCII字符
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://lwtj.chd.edu.cn',
    'priority': 'u=1, i',
    # 关键修复：对referer中的中文进行URL编码
    'referer': 'https://lwtj.chd.edu.cn/SingleSearch/index?dbID=9&dbCode=Etd1&displayDBName=' + quote('博硕士学位论文数据库'),
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def fetch_page(page=2, college='运输工程学院'):
    """
    获取指定页码的论文列表
    """
    url = 'https://lwtj.chd.edu.cn/SingleSearch/Search'
    
    # 获取表单数据
    data = get_form_data(page, college)
    
    print(f"正在获取第{page}页，学院：{college}")
    
    # 创建一个新的会话
    session = requests.Session()
    session.cookies.update(cookies)
    
    # 关键修复：手动编码表单数据
    # 过滤掉空值
    filtered_data = {k: v for k, v in data.items() if v != ''}
    # 使用urlencode编码，确保中文被正确处理
    encoded_data = urlencode(filtered_data, encoding='utf-8')
    
    try:
        # 发送POST请求，使用编码后的数据
        response = session.post(
            url,
            headers=headers,
            data=encoded_data,  # 使用编码后的字符串
            timeout=30
        )
        
        # 设置正确的编码
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            if len(response.text) > 100:
                print(f"✓ 第{page}页获取成功，数据长度：{len(response.text)}")
                return response.text
            else:
                print(f"✗ 第{page}页返回数据太短：{len(response.text)}")
                print(f"返回内容：{response.text[:200]}")
                return None
        else:
            print(f"✗ 请求失败，状态码：{response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ 请求异常：{e}")
        return None

def parse_papers(html):
    """
    解析论文列表HTML
    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    papers = []
    
    # 查找tbody
    tbody = soup.find('tbody')
    if not tbody:
        print("未找到tbody，尝试直接查找tr")
        rows = soup.find_all('tr')
    else:
        rows = tbody.find_all('tr')
    
    print(f"找到 {len(rows)} 行数据")
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            try:
                # 提取序号
                num_td = cols[0]
                num_text = num_td.get_text(strip=True)
                # 提取数字
                import re
                num_match = re.search(r'\d+', num_text)
                num = num_match.group() if num_match else num_text
                
                # 提取学号和详情链接
                student_td = cols[1]
                link = student_td.find('a')
                if link:
                    student_id = link.get_text(strip=True)
                    detail_url = link.get('href', '')
                    if detail_url and not detail_url.startswith('http'):
                        detail_url = f"https://lwtj.chd.edu.cn{detail_url}"
                else:
                    student_id = student_td.get_text(strip=True)
                    detail_url = ''
                
                # 提取标题、作者、日期
                title = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                author = cols[3].get_text(strip=True) if len(cols) > 3 else ''
                date = cols[4].get_text(strip=True) if len(cols) > 4 else ''
                
                # 只有当标题存在时才添加
                if title and len(title) > 2:
                    paper = {
                        '序号': num,
                        '学号': student_id,
                        '标题': title,
                        '作者': author,
                        '日期': date,
                        '详情链接': detail_url
                    }
                    papers.append(paper)
            except Exception as e:
                print(f"解析某行时出错：{e}")
                continue
    
    return papers

def save_to_csv(papers, filename='运输工程学院_论文列表.csv'):
    """
    保存到CSV文件
    """
    if not papers:
        print("没有数据可保存")
        return False
    
    fieldnames = ['序号', '学号', '标题', '作者', '日期', '详情链接']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers)
        
        print(f"✓ 数据已保存到 {filename}")
        print(f"  共 {len(papers)} 条记录")
        return True
    except Exception as e:
        print(f"保存文件时出错：{e}")
        return False

def main():
    """
    主函数：获取多个页面的论文
    """
    print("=" * 60)
    print("长安大学博硕士学位论文爬虫")
    print("=" * 60)
    
    college = "运输工程学院"
    all_papers = []
    
    # 从第2页开始测试
    print("\n测试第2页...")
    test_html = fetch_page(page=2, college=college)
    
    if test_html:
        test_papers = parse_papers(test_html)
        if test_papers:
            print(f"\n✓ 测试成功！第2页有 {len(test_papers)} 篇论文")
            print("\n前3篇论文预览：")
            for i, p in enumerate(test_papers[:3]):
                print(f"{i+1}. {p['标题']}")
            
            # 如果测试成功，获取更多页
            print("\n" + "=" * 60)
            print("开始批量获取数据...")
            
            # 添加到总列表
            all_papers.extend(test_papers)
            
            # 获取第3-10页
            for page in range(3, 11):
                print(f"\n{'-' * 40}")
                html = fetch_page(page=page, college=college)
                
                if html:
                    papers = parse_papers(html)
                    print(f"第{page}页解析出 {len(papers)} 篇论文")
                    
                    if papers:
                        all_papers.extend(papers)
                    
                    # 暂停一下，避免请求过快
                    time.sleep(1)
                else:
                    print(f"第{page}页获取失败")
            
            # 保存所有结果
            if all_papers:
                print(f"\n{'=' * 60}")
                print(f"总共获取到 {len(all_papers)} 篇论文")
                
                # 按日期排序
                all_papers.sort(key=lambda x: x['日期'], reverse=True)
                
                # 保存到CSV
                save_to_csv(all_papers)
                
                # 显示统计信息
                authors = set(p['作者'] for p in all_papers)
                print(f"涉及作者数量：{len(authors)}")
                
                # 显示最近的5篇论文
                print("\n最近5篇论文：")
                for i, paper in enumerate(all_papers[:5]):
                    print(f"{i+1}. {paper['标题']} - {paper['作者']} ({paper['日期']})")
        else:
            print("测试失败：无法解析论文")
    else:
        print("测试失败：无法获取数据")

if __name__ == "__main__":
    main()