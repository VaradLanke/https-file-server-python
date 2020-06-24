import http.server, ssl, os

# absolute path of pyServer.py
thisScriptPath=os.path.dirname(os.path.abspath(__file__))+'/'

# generate self signed certificate using openssl command
def generate_selfsigned_cert():
    try:
        OpenSslCommand = 'openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out '+thisScriptPath+'cert.pem -keyout '+thisScriptPath+'key.pem -subj "/C=IN/ST=Maharashtra/L=Satara/O=Wannabees/OU=KahiHiHa Department/CN=www.iamselfdepartment.com"'
        os.system(OpenSslCommand)
        print('<<<<Certificate Generated>>>>>>')
    except:
        print('error while generating certificate')

# starts server on provided host and port
def startServer(host,port):
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                server_side=True,
                                certfile = thisScriptPath+"cert.pem",
                                keyfile = thisScriptPath+"key.pem",
                                ssl_version=ssl.PROTOCOL_TLSv1
                                )
    print("File Server started at https://" + server_address[0]+":"+str(server_address[1]))
    httpd.serve_forever()

# entry point of script
def main():
    try:
        generate_selfsigned_cert()
        # you can change the host and port
        startServer('localhost',8000)
    except KeyboardInterrupt:
        print("\nFile Server Stopped!")

# call to main function
main()

'''
Command reference for signed certificate generation: 
1) openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out cert.pem \
            -keyout key.pem \
            -subj "/C=IN/ST=Maharashtra/L=Satara/O=Wannabees/OU=KahiHiHa Department/CN=www.iamselfdepartment.com"
            
2) openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out cert.pem -keyout key.pem -subj "/C=IN/ST=Maharashtra/L=Satara/O=Wannabees/OU=KahiHiHa Department/CN=www.iamselfdepartment.com"
'''
