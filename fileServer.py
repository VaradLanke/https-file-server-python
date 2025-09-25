import sys
import subprocess

# Step 1: Ensure 'cryptography' is installed
try:
    import cryptography
except ImportError:
    print("[INFO]: 'cryptography' not found. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    print("[INFO]: 'cryptography' installed successfully. Continuing...")
    import cryptography  # Try importing again after install

# Step 2: Continue with imports
import http.server
import ssl
import socket
import tempfile
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

def generate_self_signed_cert():
    # Generate private key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Build certificate subject and issuer
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Maharashtra"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Satara"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Wannabees"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "KahiHiHa Department"),
        x509.NameAttribute(NameOID.COMMON_NAME, "www.iamselfdepartment.com"),
    ])

    # Create self-signed certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow() - timedelta(minutes=5))
        .not_valid_after(datetime.utcnow() + timedelta(days=3650))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    # Serialize cert and key to PEM
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    return cert_pem, key_pem

def start_https_server(host='localhost', port=8000):
    cert_pem, key_pem = generate_self_signed_cert()

    # Write cert and key to temp files
    with tempfile.NamedTemporaryFile(delete=False) as cert_file, tempfile.NamedTemporaryFile(delete=False) as key_file:
        cert_file.write(cert_pem)
        cert_file.flush()
        key_file.write(key_pem)
        key_file.flush()

        # Set up SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file.name, keyfile=key_file.name)

        # Start HTTPS server
        server_address = (host, port)
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print(f"[INFO]: HTTPS File Server running at https://{host}:{port}")
        print("[INFO]: Serving files from:", os.getcwd())
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO]: Server stopped.")

if __name__ == '__main__':
    import os
    start_https_server('localhost', 8000)
