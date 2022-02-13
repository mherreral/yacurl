import re
import socket
import ssl
import requests
import os

buff_size = 1024

# Get parameters from console
def get_page_info():
    HOST = input("type the url ")
    #HOST = 'github.com'
    PORT = int(input("type the port "))
    #PORT = 443
    return HOST, PORT

# Create a wrapped socket when port is 443
def create_ssl_socket(HOST, PORT):
    ContextSSL = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_socket = ContextSSL.wrap_socket(cli_socket, server_hostname=HOST)
    cli_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cli_socket.connect((HOST, PORT))
    cli_socket.do_handshake()

    der = cli_socket.getpeercert(binary_form=True)
    pem_data = ssl.DER_cert_to_PEM_cert(der)

    http_request = create_http_req("/", HOST)
    print_info(http_request, "request")

    cli_socket.send(http_request.encode())  # send request

    data = ''
    # receive data
    while True:
        recv = cli_socket.recv(buff_size)
        if not recv:
            break
        data += recv.decode('utf-8')
        print(recv)
    cli_socket.close()
    return(data)

# Print received and transmitted http packages
def print_info(data, type):
    if type == "request":
        print("\n HTTP REQUEST PACKAGE\n")
        print(data)
    else:
        print("\n HTTP RESPONSE PACKAGE\n")
        print(data)

# Create http request depending on resource
def create_http_req(resource, HOST):
    http_request = \
        f"GET {resource} HTTP/1.1\r\n"\
        f"Host: {HOST}\r\n"\
        "User-Agent: Mozilla/5.0\r\n"\
        "Connection: close\r\n\r\n"
    return http_request

# Save transferred files in folder
def save_data(data, dir_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, "pages", dir_name)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    index_file = os.path.join(path, "index.html")
    with open(index_file, 'w') as file:
        file.write(data)

# Parse html to find static resources
def parse_html(data):
    resources = re.findall(
        'href = ".*\.tgz|.*\.tar\.gz|.*\.png|.*\.jpg|.*\.jpeg|.*\.png|.*\.pdf|.*\.js|.*\.css|.*\.html"', data)
    print("\n\nLIST OF STATIC RESOURCES IN PAGE\n\n")
    results = []
    for resource in resources:
        # Find all static resources with regex
        pattern = r'.*(http.+)(\.html|\.tgz|\.tar\.gz|\.png|\.jpg|\.jpeg|\.png|\.pdf|\.js|\.css)($)'
        prog = re.compile(pattern)
        results.append(prog.findall(resource))

    # Remove empty positions in array
    while [] in results:
        results.remove([])

    # Save complete links for downloading
    i = 0
    links = []
    for result in results:
        aux = str(result[i][0]) + str(result[i][1])
        links.append(aux)

    # Print found resources
    for link in links:
        print(link)

    return(links)

# Download files from links
def download_resources(links, dir_name):
    print("\nDownloading resources")
    parent_dir = os.getcwd()
    for link in links:
        filename = link.split('/')[-1]
        path = os.path.join(parent_dir, "pages", dir_name, filename)
        try:
            response = requests.get(link)
            file = open(path, "wb")
            file.write(response.content)
            file.close()
        except:
            pass

# Create a non wrapped socket
def create_socket(HOST, PORT):
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_socket.connect((HOST, PORT))
    http_request = create_http_req("/", HOST)
    print_info(http_request, "request")

    cli_socket.sendall(http_request.encode())

    data = ''
    # receive data
    while True:
        recv = cli_socket.recv(buff_size)
        if not recv:
            break
        data += recv.decode('utf-8')
        print(recv)
    if "301" in data:
        print(
            "\n\nWARNING: it might be a problem with the selected port or specified url\n\n")
        exit(1)
    cli_socket.close()
    return(data)

def main():
    # get parameters from console
    HOST, PORT = get_page_info()

    # create properly the socket depending on given port
    if PORT == 443:
        print("creating communication to ", HOST, " through port ", PORT)
        data = create_ssl_socket(HOST, PORT)
        save_data(data, HOST)
        links = parse_html(data)
        download_resources(links, HOST)
    elif PORT == 80:
        print("creating communication to ", HOST, " through port ", PORT)
        data = create_socket(HOST, PORT)
        save_data(data, HOST)
        links = parse_html(data)
        download_resources(links, HOST)
    else:
        print("Bad port for HTTP protocol")
        exit(1)

if __name__ == "__main__":
    main()
