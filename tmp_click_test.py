import http.client, json

conn = http.client.HTTPConnection('127.0.0.1',8000)
# GET /state/
conn.request('GET','/state/')
res = conn.getresponse()
print('GET /state/ status', res.status)
body = res.read().decode()
print('body', body)
cookies = res.getheader('Set-Cookie')
print('set-cookie:', cookies)

# POST /guess/
headers = {'Content-Type':'application/json'}
if cookies:
    headers['Cookie'] = cookies
conn.request('POST','/guess/', body=json.dumps({'letter':'A'}), headers=headers)
res2 = conn.getresponse()
print('POST /guess/ status', res2.status)
print('body', res2.read().decode())

# POST /reset/
conn.request('POST','/reset/', headers=headers)
res3 = conn.getresponse()
print('POST /reset/ status', res3.status)
print('body', res3.read().decode())

# GET /state/ again
conn.request('GET','/state/', headers={'Cookie': cookies} if cookies else {})
res4 = conn.getresponse()
print('GET /state/ status', res4.status)
print('body', res4.read().decode())
