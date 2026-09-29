import urllib.request
from pathlib import Path

def test_upload():
    url = 'http://127.0.0.1:8000/api/upload'
    filepath = Path('sample_onions_tray.jpg')
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    with open(filepath, 'rb') as f:
        file_bytes = f.read()
        
    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filepath.name}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode('utf-8')
    
    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    body = header + file_bytes + footer
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        res_text = response.read().decode('utf-8')
        print("Upload Response:", res_text)

if __name__ == '__main__':
    test_upload()
