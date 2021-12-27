import time
import sys
from io import BytesIO
import urllib.request
from urllib.request import urlopen
try:
    from lxml import etree
    from vincenty import vincenty
except Exception as e:
    print(e)
    print('\nDependencies required! Please "pip install" missing modules!')
    sys.exit()
import argparse
import gzip
args=argparse.Namespace()
args.suppress=None
args.store=None
import subprocess, os
import shutil
import urllib.parse
from subprocess import Popen, PIPE, STDOUT
#dwnld_lst=['350x350','350x350','350x350','350x350','350x350']
print('\nTesting Internet Connection. . .')
dwnld_lst=['2000x2000','4000x4000','3500x3500','4000x4000','3000x3000']
upSizes=[1024*1024*2,1024*1024*2,1024*1024*2,1024*1024*2]



def TestUpload():
    # Testing upload speed
        print('\n')

        url="upload.php"
        full_url=best[0]['url']+url
        prefixed = [filename for filename in os.listdir('.') if filename.startswith("random3")]
    ####PLACE WHERE YOU CAN SPECIFY WHICH FILE YOU WANT TO UPLOAD TEST. DEFAULT IS RANDOM4000X4000.JPG, OPTIONALLY YOU UPLOAD 100MB.TEST, uncomment next line if needed####
        filename=prefixed[0]
        for i in range(0, len(dwnld_lst)):

                full_url=best[i]['url']+url

                com = str('echo "scale=2; `curl -m 30 --progress-bar -w "%{speed_upload}" --data-binary @'+filename+' '+full_url+'`"')
                process = os.popen(com).read()
                if 'unavailable.' in str(process):
                    continue
                if 'Too Large'  in str(process):
                    print('bad serv, skipping...\n')
                else:

                    if 'size=500' in str(process):
                        speed = str('\033[92m'+str(round(int(process.strip().split('size=500')[-1].split('.')[0]) / 1048576, 2)))+"MB/s"+'\033[0;37;40m'
                        print('upload speed is '+speed+ '    uploaded   to  '+full_url)
                        speeds.append(str(round(int(process.strip().split('size=500')[-1].split('.')[0]) / 1048576, 2))+"MB/s")
                    elif 'size=' not in str(process):
                        speed = str('\033[92m'+str(round(int(process.strip().split(' ')[1].split('.')[0]) / 1048576, 2)))+"MB/s"+'\033[0;37;40m'
                        print('upload speed is '+speed+ '    uploaded   to  '+full_url)
                        speeds.append(str(round(int(process.strip().split(' ')[1].split('.')[0]) / 1048576, 2))+"MB/s")
                    elif 'size=' in str(process):
                        try:
                            speed = str('\033[92m'+str(round(int(process.strip().split('size=')[-1].split('.')[0][6:]) / 1048576, 2))) + "MB/s" + '\033[0;37;40m'
                        except:
                            speed = str('\033[92m'+str(round(int(process.strip().split('\n')[-1].split('.')[0]) / 1048576, 2))) + "MB/s" + '\033[0;37;40m'
                        print('upload speed is '+speed+ '    uploaded   to  ' + full_url)

                        #print('bad serv, skipping. . .')
        try:
            speeds.remove('0.0MB/s')
        except Exception as e:
            pass


def TestDownload():
       # Testing download speed

        for i in range(0, len(dwnld_lst)):
            url="random"+dwnld_lst[i]+".jpg?x=" + str( time.time() )
            full_url=best[i]['url']+url
            com = 'curl -m 60 --progress-bar -w "%{speed_download}" -O '+full_url
            process = os.popen(com).read()
            speed = str('\033[91m'+str(round(int(process.split('.')[0]) / 1048576, 2)))+"MB/s"+'\033[0;37;40m'
            print('download speed is '+speed+ '    downloaded   from  '+best[i]['url'])
            down_speeds.append(str(round(int(process.split('.')[0]) / 1048576, 2))+"MB/s")
            try:

                os.remove(url)
            except Exception:
                pass

        url="random"+dwnld_lst[-1]+".jpg"
        full_url=best[0]['url']+url
        if os.path.isfile(url):
            pass
        else:
            com = 'curl -m 90 --progress-bar -w "%{speed_download}" -O '+full_url
            process = os.popen(com).read()
            speed = str('\033[91m'+str(round(int(process.split('.')[0]) / 1048576, 2)))+"MB/s"+'\033[0;37;40m'
            down_speeds.append(str(round(int(process.split('.')[0]) / 1048576, 2))+"MB/s")
            print(full_url)
            print('download speed is '+speed+ '    downloaded   from  '+full_url)
def get_rqst(uri):
        req = urllib.request.Request(uri, headers=headers)
        return req


def decmprs_rspns(response):

        data = BytesIO(response.read())
        gzipper = gzip.GzipFile(fileobj=data)
        try:
            return gzipper.read()
        except Exception as e:
            # Response isn't gzipped, therefore return the data.
            return data.getvalue()

def dstnce(one, two):
        km = vincenty((two),(one))

        return km

def load_cnfg():
    print("Loading configuration...\n")
    uri = "http://speedtest.net/speedtest-config.php?x=" + str( time.time() )
    request = get_rqst(uri)
    #print(get_rqst())
    response = None
    try:
        response = urlopen(request)
    except:
        print   ("Failed to get config file.\n")
        sys.exit(1)

    config = etree.fromstring(decmprs_rspns(response))
    ip=config.find("client").attrib['ip']
    lat=float(config.find("client").attrib['lat'])
    lon=float(config.find("client").attrib['lon'])
    return { 'ip': ip, 'lat': lat, 'lon': lon }

def ltncy(servers):
        print("Testing latency...\n")
        po = []
        for server in servers:
            now= sngl_ltncy(server['url'] + "latency.txt?x=" + str(time.time())) * 1000
            #print(now)
            now=now/2
            if now == -1 or now == 0:
                continue
            print("%0.0f ms TO %s (%s, %s, %s) [%0.2f kylometers]" %
                (now, server['url'], server['sponsor'], server['name'], server['country'], server['distance']))

            server['latency']=now
            if int(len(po)) < int(5):
                po.append(server)
            else:
                largest = -1

                for x in range(len(po)):
                    if largest < 0:
                        if now < po[x]['latency']:
                            largest = x
                    elif po[largest]['latency'] < po[x]['latency']:
                        largest = x

                if largest >= 0:
                    po[largest]=server

        return po

def sngl_ltncy(dest_addr):


        averagetime=0
        total=0
        for i in range(10):
            error=0
            startTime = time.time()
            try:
                req = get_rqst(dest_addr)
                response = urlopen(req)
            except:
                error=1

            if error==0:
                averagetime = averagetime + (time.time() - startTime)
                total=total+1

            if total==0:
                return False
        return averagetime/total

def nearest(center, points, num=5):
        closest={}
        for p in range(len(points)):
            now = dstnce(center, [points[p]['lat'], points[p]['lon']])
            points[p]['distance']=now
            while True:
                if now in closest:
                    now=now+00.1
                else:
                    break
            closest[now]=points[p]
        n=0
        ret=[]
        for key in sorted(closest):
            ret.append(closest[key])
            n+=1
            if n >= num and num!=0:
                break
        return ret


headers = {
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; OS X; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
                    'Connection' : 'keep-alive',
                    }


payload = { 'ip': '', 'lat': '', 'lon': '' }
try:
    uri = "http://speedtest.net/speedtest-servers.php"
    request = get_rqst(uri)
    response = urlopen(request)

    servers_xml = etree.fromstring(decmprs_rspns(response))
    servers=servers_xml.find("servers").findall("server")
    server_list = []
except Exception as e:
    uri = "http://c.speedtest.net/speedtest-servers-static.php"
    request = get_rqst(uri)
    response = urlopen(request)

    servers_xml = etree.fromstring(decmprs_rspns(response))
    servers=servers_xml.find("servers").findall("server")
    server_list = []

for server in servers:
    server_list.append({
            'lat': float(server.attrib['lat']),
            'lon': float(server.attrib['lon']),
            'url': server.attrib['url'].rsplit('/', 1)[0] + '/',
            'name': server.attrib['name'],
            'country': server.attrib['country'],
            'sponsor': server.attrib['sponsor'],
            'id': server.attrib['id'],
            })
config = load_cnfg()


for item in  server_list:
    item['distance'] = vincenty((config['lon'], config['lat']), (item['lon'], item['lat']))

newlist = sorted(server_list, key=lambda k: k['distance'])

best=ltncy(newlist[:5])
best = sorted(best, key=lambda k: k['latency'])

down_speeds=[]
speeds=[]
print('\033[4m'+'\033[1m'+'\nif you want to skip download/upload test, – simply do keyboard interrupt using Ctrl+C!+''\033[0;37;40m'+'\n\n')

try:
    print('\ntesting download speed.  .  .  .  .   .\n\n')
    TestDownload()
except KeyboardInterrupt as e:
    print('\nSkipping test!')
    pass

try:
    print('\n\ntesting upload speed. . . . . .\n')
    TestUpload()
except KeyboardInterrupt as e:
    print('\nSkipping test!!')
    pass

try:
    down_speeds.remove('0.0MB/s')
except Exception as e:
    pass
print('downloads_speeds list: ',down_speeds,'uploads_speeds list: ', speeds)

