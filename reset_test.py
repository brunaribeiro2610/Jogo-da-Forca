import http.client, json

conn = http.client.HTTPConnection('127.0.0.1',8000)
# GET /state/
conn.request('GET','/state/')
res = conn.getresponse()
print('GET /state/ status', res.status)
body = res.read().decode()
print('body', body)
set_cookie = res.getheader('Set-Cookie')
print('set-cookie:', set_cookie)

# POST /guess/ (letter A)
headers = {'Content-Type':'application/json'}
if set_cookie:
    headers['Cookie'] = set_cookie
conn.request('POST','/guess/', body=json.dumps({'letter':'A'}), headers=headers)
res2 = conn.getresponse()
print('\nPOST /guess/ status', res2.status)
print(res2.read().decode())

# POST /reset/
headers = {'Content-Type':'application/json'}
if set_cookie:
    headers['Cookie'] = set_cookie
conn.request('POST','/reset/', headers=headers)
res3 = conn.getresponse()
print('\nPOST /reset/ status', res3.status)
print('body', res3.read().decode())

# GET /state/ after reset
conn.request('GET','/state/', headers={'Cookie': set_cookie} if set_cookie else {})
res4 = conn.getresponse()
print('\nGET /state/ after reset status', res4.status)
print(res4.read().decode())
