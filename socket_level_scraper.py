import socket, ssl, re, sys
from week5cheflib import utils
from bs4 import BeautifulSoup

def parse_link(hostname, trunc_len=None):
    if trunc_len:
        hostname = hostname[trunc_len:]
    
    page_link = "/".join(hostname.split("/")[1:])
    hostname = hostname.split("/")[0]
    return hostname, page_link

def parse_port(hostname, trunc_len=None):
    page_link = hostname.split(trunc_len)[0]
    hostname = hostname.split(trunc_len)[1]
    return hostname, page_link


# Global variables
context = ssl.SSLContext()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.set_alpn_protocols(['http/1.1'])

buffer = ""

print("If it blocks, press ctrl-C, It's a sock.recv blocking bug")
hostname = utils.questions("Input Website addr")

# Check for port
pattern = r"\:\d{1,5}"
scanPort = re.findall(pattern, hostname)
PORT_INPUT = scanPort[0][1:]

if PORT_INPUT:
    if PORT_INPUT == "80":
        PORT = 80
        hostname, page_link = parse_port(hostname, scanPort[0])

    elif PORT_INPUT == "443":
        PORT = 443
        hostname, page_link = parse_port(hostname, scanPort[0])

    else:
        print("ONLY PORT IN 80 and 443")
        sys.exit(1)
else:
    if hostname.startswith("http://"):
        PORT = 80
        hostname, page_link = parse_link(hostname, 7)

    elif hostname.startswith("https://"):
        PORT = 443
        hostname, page_link = parse_link(hostname, 8)
    else:
        # Default goes to the html link
        hostname, page_link = parse_link(hostname)
        PORT = 80

query = 'GET /%s HTTP/1.1\r\nHOST: %s \r\n\r\n' % ( page_link, hostname)

if PORT == 443:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        s_ssl = context.wrap_socket(sock)
        s_ssl.server_hostname = hostname
    
        s_ssl.connect((hostname, PORT))


        s_ssl.send(query.encode())
 
        while True:
            try:
                buffered_data = s_ssl.recv(1024).decode("utf-8") 
            except Exception as exc:
                break

            buffer += buffered_data

            
            # Every HTML page most posses the closing end tag which signifies end of page
            if "</html>" in buffered_data:
                break

elif PORT == 80:        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, PORT))

        sock.send(query.encode())

        while True:
            buffered_data = sock.recv(8024).decode("utf-8")                 
            buffer += buffered_data
            
            # Every HTML page most posses the closing end tag which signifies end of page
            if "</html>" in buffered_data:
                break



def display_links(buffer):
    html_soup = BeautifulSoup(buffer, 'html.parser')
    all_links = html_soup.find_all("a")
    for link in all_links:
        print(link.get("href"))

display_links(buffer)