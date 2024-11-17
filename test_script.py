import requests

url = 'http://127.0.0.1:8000/api/detect/'
files = {'image': open('test_image.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.json())  # Check the response for the output image URL
