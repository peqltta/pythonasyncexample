import asyncio
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import re
import urllib
print('Loading...')
headers = {'accept': 'application/json',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?1',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'}
clean = re.compile('<.*?>')
url = 'http://gimmeproxy.com/api/getProxy?protocol=http'
url2 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
urlsocks4 = 'http://gimmeproxy.com/api/getProxy?protocol=socks4'
url2socks4 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all'
urlsocks5 = 'http://gimmeproxy.com/api/getProxy?protocol=socks5'
url2socks5 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all'
proxies = []
socks4 = []
socks5 = []
f = urllib.request.urlopen(url2)
for line in f:
    decoded_line = line.strip().decode("utf-8")
    proxies.append(decoded_line)
f.close()
f = urllib.request.urlopen(url2socks4)
for line in f:
    decoded_line = line.strip().decode("utf-8")
    socks4.append(decoded_line)
f.close()
f = urllib.request.urlopen(url2socks5)
for line in f:
    decoded_line = line.strip().decode("utf-8")
    socks5.append(decoded_line)
f.close()
working = []
workingsocks4 = []
workingsocks5 = []
try:
    f = open('working.txt','r+')
    for line in f:
        working.append(line.strip())
    f.close()
except:
    f = open('working.txt', 'w+')
    f.close()
try:
    f = open('workingsocks4.txt','r+')
    for line in f:
        workingsocks4.append(line.strip())
    f.close()
except:
    f = open('workingsocks4.txt', 'w+')
    f.close()
try:
    f = open('workingsocks5.txt','r+')
    for line in f:
        workingsocks5.append(line.strip())
    f.close()
except:
    f = open('workingsocks5.txt', 'w+')
    f.close()
new = []
newsocks4 = []
newsocks5 = []
async def checkhttp(ip):
    prox = ip
    ip = "http://" + ip
    try:
        conn = aiohttp.TCPConnector(limit=0)
        session = aiohttp.ClientSession(connector=conn)
        response = await session.get(url, proxy=ip, headers=headers, timeout=120)
        out = await response.json()
        working.append(prox)
        newproxy = out['ipPort']
        newproxy = clean.sub('', newproxy)
        new.append(newproxy)
        proxies.append(newproxy)
        print(newproxy + ' ---- new - http')
        await session.close()
    except Exception as e:
        proxies.remove(prox)
        await session.close()
    await session.close()
async def checksocks4(ip):
    prox = ip
    ip = "socks4://" + ip
    connector = ProxyConnector.from_url(ip, limit=0)
    try:
        session = aiohttp.ClientSession(connector = connector)
        response = await session.get(urlsocks4, headers=headers, timeout=120)
        out = await response.json()
        workingsocks4.append(prox)
        newproxysocks4 = out['ipPort']
        newproxysocks4 = clean.sub('', newproxysocks4)
        newsocks4.append(newproxysocks4)
        socks4.append(newproxysocks4)
        print(newproxysocks4 + ' ---- new - socks4')
        await session.close()
    except Exception as e:
        socks4.remove(prox)
        await session.close()
    await session.close()
async def checksocks5(ip):
    prox = ip
    ip = "socks5://" + ip
    connector = ProxyConnector.from_url(ip, limit=0)
    try:
        session = aiohttp.ClientSession(connector = connector)
        response = await session.get(urlsocks5, headers=headers, timeout=120)
        out = await response.json()
        workingsocks5.append(prox)
        newproxysocks5 = out['ipPort']
        newproxysocks5 = clean.sub('', newproxysocks5)
        newsocks5.append(newproxysocks5)
        socks5.append(newproxysocks5)
        print(newproxysocks5 + ' ---- new - socks5')
        await session.close()
    except Exception as e:
        socks5.remove(prox)
        await session.close()
    await session.close()
tasks = []
def main():
    print('Creating Jobs')
    loop = asyncio.get_event_loop()
    for item in proxies:
        tasks.append(asyncio.ensure_future(checkhttp(item)))
    for item in socks4:
        tasks.append(asyncio.ensure_future(checksocks4(item)))
    for item in socks5:
        tasks.append(asyncio.ensure_future(checksocks5(item)))
    loop.run_until_complete(asyncio.wait(tasks))
    print('Jobs Created')
def writefiles():
    with open('proxies.txt', 'w+') as f:
        for i in proxies:
            f.write("%s\n" % i)
        f.close()
    with open('working.txt', 'w+') as f:
        for i in working:
            f.write("%s\n" % i)
        f.close()
    with open('socks4.txt', 'w+') as f:
        for i in socks4:
            f.write("%s\n" % i)
        f.close()
    with open('workingsocks4.txt', 'w+') as f:
        for i in workingsocks4:
            f.write("%s\n" % i)
        f.close()
    with open('socks5.txt', 'w+') as f:
        for i in socks5:
            f.write("%s\n" % i)
        f.close()
    with open('workingsocks5.txt', 'w+') as f:
        for i in workingsocks5:
            f.write("%s\n" % i)
        f.close()
    print('Saved')
checkmore = 0
print('Loaded')
while checkmore != 1:
        main()
        working = [*{*working}]
        print(str(len(working)) + '  total working proxies')
        proxies = [*{*proxies}]
        workingsocks4 = [*{*workingsocks4}]
        print(str(len(workingsocks4)) + '  total working socks4')
        socks4 = [*{*socks4}]
        workingsocks5 = [*{*workingsocks5}]
        print(str(len(workingsocks5)) + '  total working socks5')
        socks5 = [*{*socks5}]
        writefiles()