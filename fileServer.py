import http.server, ssl, os

# absolute path of fileServer.py
thisScriptPath=os.path.dirname(os.path.abspath(__file__))+'/'
cert_path = thisScriptPath + 'cert.pem'
key_path = thisScriptPath + 'key.pem'

# generate self signed certificate using openssl command
def generate_selfsigned_cert():
    try:
        if os.path.exists(cert_path) and os.path.exists(key_path):
            print('[WARN]: Certificate already exists.')
            return

        OpenSslCommand = f'openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out "{cert_path}" -keyout "{key_path}" -subj "/C=IN/ST=Maharashtra/L=Satara/O=Wannabees/OU=KahiHiHa Department/CN=www.iamselfdepartment.com"'
        ret = os.system(OpenSslCommand)

        if ret == 0 and os.path.exists(cert_path) and os.path.exists(key_path):
            print('[INFO]: <<<<Certificate Generated>>>>>>')
        else:
            print('[ERROR]: Failed to generate certificate. Please Check Whether OpenSsl is installed and added in PATH')
            exit(1)
    except:
        print('[ERROR]: Exiting with error...')
        exit(1)

# starts server on provided host and port
def startServer(host,port):
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=thisScriptPath + "cert.pem", keyfile=thisScriptPath + "key.pem")

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("[INFO]: File Server started at https://" + server_address[0] + ":" + str(server_address[1]))
    httpd.serve_forever()

# entry point of script
def main():
    try:
        generate_selfsigned_cert()
        # you can change the host and port
        startServer('localhost',8000)
    except KeyboardInterrupt:
        print("\n[INFO]: File Server Stopped!")

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
