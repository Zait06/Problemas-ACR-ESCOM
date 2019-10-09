from ftplib import FTP
ftp = FTP('ftp.debian.org') 
ftp.login()
ftp.cwd('debian')
ftp.retrlines('LIST')
ftp.retrbinary('RETR README', open('README', 'wb').write)
ftp.quit()