import requests
from PIL import Image

url = 'https://img.freepik.com/free-photo/classmates-friends-bag-school-education_53876-137717.jpg?w=1800&t=st=1676199328~exp=1676199928~hmac=7dc7b1e710262230176b6734c8a224a3ed43fe0bd3f5b2460815429383cd4826'
r = requests.get(url, stream=True).raw
img = Image.open(r)
img.show()
img.save('src.png')
