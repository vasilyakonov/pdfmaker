#requires pydrive installation to work, bud
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()

# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = GoogleDrive(gauth)

# Create GoogleDriveFile instance with title 'Hello.txt'.
file1 = drive.CreateFile({'title': 'Hello.txt'})
file1.Upload() # Upload the file.
print('title: %s, id: %s' % (file1['title'], file1['id']))
# title: Hello.txt, id: {{FILE_ID}}