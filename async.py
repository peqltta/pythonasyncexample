import asyncio
import aiohttp
import re
import urllib
clean = re.compile('<.*?>')
url = 'http://gimmeproxy.com/api/getProxy?protocol=http'
url2 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
f = urllib.request.urlopen(url2)
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
proxies = []
for line in f:
    decoded_line = line.strip().decode("utf-8")
    proxies.append(decoded_line)
f.close()
working = []
f = open('working.txt','r+')
for line in f:
    working.append(line.strip())
f.close()
new = []
async def check(ip):
    prox = ip
    ip = "http://" + ip
    try:
        session = aiohttp.ClientSession()
        response = await session.get(url, proxy=ip, headers=headers, timeout=20)
        out = await response.json()
        working.append(prox)
        print(prox + ' ------ working')
        newproxy = out['ipPort']
        newproxy = clean.sub('', newproxy)
        new.append(newproxy)
        proxies.append(newproxy)
        print(newproxy + ' ---- new')
        await session.close()
    except Exception as e:
        proxies.remove(prox)
        print(prox + ' -- dead')
        await session.close()
    await session.close()
tasks = []
def main():
    loop = asyncio.get_event_loop()
    for item in proxies:
        tasks.append(asyncio.ensure_future(check(item)))
    loop.run_until_complete(asyncio.wait(tasks))
checkmore = ' '
def writefiles():
    with open('proxies.txt', 'w+') as f:
        for i in proxies:
            f.write("%s\n" % i)
        f.close()
    with open('working.txt', 'w+') as f:
        for i in working:
            f.write("%s\n" % i)
        f.close()
    print('Saved')
while checkmore != 'y':
        main()
        working = [*{*working}]
        print(str(len(working)) + '  total working proxies')
        proxies = [*{*proxies}]
        writefiles()