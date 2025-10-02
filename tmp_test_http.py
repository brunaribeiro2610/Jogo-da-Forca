import http.client, json

conn = http.client.HTTPConnection('127.0.0.1',8000)
# First GET /state/ to initialize session and get cookies
conn.request('GET','/state/')
res = conn.getresponse()
body = res.read().decode()
print('GET /state/ status', res.status)
print('body', body)
cookies = res.getheader('Set-Cookie')
print('set-cookie:', cookies)

# Use same connection to POST guess
headers = {'Content-Type':'application/json'}
if cookies:
    headers['Cookie']=cookies

conn.request('POST','/guess/', body=json.dumps({'letter':'A'}), headers=headers)
res2 = conn.getresponse()
print('POST /guess/ status', res2.status)
print('body', res2.read().decode())
