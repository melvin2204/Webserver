#Content-Type: image/png
img = open("public/profilePicture.png","rb")
#self.wfile.write(img.read())
print(img.read())
img.close()