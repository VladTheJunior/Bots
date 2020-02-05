import json
import xml.etree.ElementTree as ElementTree
import aiohttp

def get_sec(time_str):
    h, m, s = time_str.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def CalcDelta(X):
    return (
        -0.00000000003673 * X * X * X * X
        + 0.000000268594 * X * X * X
        - 0.000718416 * X * X
        + 0.819349 * X
        - 321.514
    )

def getends(n, s1, s2, s3):
    num = n % 100
    num1 = n % 10
    if num1 == 1 and num != 11:
        return s1
    if (num1 == 2 and num != 12) or (num1 == 3 and num != 13) or (num1 == 4 and num != 14):
        return s2
    return s3

def find_between(first, last, s):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

async def postDataJSON(URL, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data=data, timeout=5) as resp:
            return await resp.json()

async def getJSON(URL, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params, timeout=10) as resp:
            return await resp.json()

async def getXML(URL, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params, timeout=10) as resp:
            return ElementTree.fromstring(await resp.text())

# Сохранение JSON в файл
def saveJSON(Path, data):
    with open(Path, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True)

# Открытие JSON из файла
def openJSON(Path):
    with open(Path, encoding='utf-8') as data_file:
        return json.loads(data_file.read())