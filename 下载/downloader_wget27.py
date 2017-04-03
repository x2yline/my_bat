#!/usr/bin/python
# encoding=utf-8
import requests, sys, os, re, time

class wget:
    def __init__(self, config = {}):
        self.config = {
            'block': int(config['block'] if config.has_key('block') else 1024),
        }
        self.total = 0
        self.size = 0
        self.filename = ''

    def touch(self, filename):
        with open(filename, 'w') as fin:
            pass

    def remove_nonchars(self, name):
        (name, _) = re.subn(ur'[\\\/\:\*\?\"\<\>\|]', '', name)
        return name

    def support_continue(self, url):
        headers = {
            'Range': 'bytes=0-4'
        }
        try:
            r = requests.head(url, headers = headers)
            crange = r.headers['content-range']
            self.total = int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
            return True
        except:
            pass
        try:
            self.total = int(r.headers['content-length'])
        except:
            self.total = 0
        return False


    def download(self, url, filename, headers = {}):
        finished = False
        block = self.config['block']
        local_filename = self.remove_nonchars(filename)
        tmp_filename = local_filename + '.downtmp'
        size = self.size
        total = self.total
        if self.support_continue(url):  # 支持断点续传
            try:
                with open(tmp_filename, 'rb') as fin:
                    self.size = int(fin.read())
                    size = self.size + 1
            except:
                self.touch(tmp_filename)
            finally:
                headers['Range'] = "bytes=%d-" % (self.size, )
        else:
            self.touch(tmp_filename)
            self.touch(local_filename)

        r = requests.get(url, stream = True, verify = False, headers = headers)
        if total > 0:
            print "[+] Size: %dKB" % (total / 1024)
        else:
            print "[+] Size: None"
        start_t = time.time()
        with open(local_filename, 'ab+') as f:
            f.seek(self.size)
            f.truncate()
            try:
                for chunk in r.iter_content(chunk_size = block): 
                    if chunk:
                        f.write(chunk)
                        size += len(chunk)
                        f.flush()
                    sys.stdout.write('\b' * 64 + 'Now: %d, Total: %s' % (size, total))
                    sys.stdout.flush()
                finished = True
                os.remove(tmp_filename)
                spend = int(time.time() - start_t)
                speed = int((size - self.size) / 1024 / spend)
                sys.stdout.write('\nDownload Finished!\nTotal Time: %ss, Download Speed: %sk/s\n' % (spend, speed))
                sys.stdout.flush()
            except:
                # import traceback
                # print traceback.print_exc()
                print "\nDownload pause.\n"
            finally:
                if not finished:
                    with open(tmp_filename, 'wb') as ftmp:
                        ftmp.write(str(size))




url = raw_input('\nPlease input your url:')

filename = raw_input("\nPlease Enter the filename for the file:")
if not filename:
        filename = url.split('/')[-1]

useragent = raw_input('\nPlease enter safari or ipad or android for useragent:')
if useragent.lower() == 'safari':
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
elif useragent.lower()=='ipad':
    useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
elif useragent.lower() == 'android':
    useragent = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
elif useragent.lower() == 'windows':
    useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
else:
    pass
referer = raw_input('\nPlease enter the referer url:')

cookie = raw_input('\nPlease enter the cookie:')
if not cookie:
    cookie = None
headers = {
        'User-Agent': useragent,
        'Referer': referer if referer else None,
        'Cookie': cookie,
        'Range': 'bytes=0-'
    }
wget().download(url, filename,headers = headers)

print 'all things done!'