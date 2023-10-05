import signal
import sys
import socket

HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

products = [
    {
        "name": "Fluent Python: Clear, Concise, and Effective Programming",
        "author": "Luciano Ramalho",
        "price": 39.95,
        "description": "Don't waste time bending Python to fit patterns you've learned in other languages. Python's simplicity lets you become productive quickly, but often this means you aren't using everything the language has to offer. With the updated edition of this hands-on guide, you'll learn how to write effective, modern Python 3 code by leveraging its best ideas."
    },
    {
        "name": "Introducing Python: Modern Computing in Simple Packages",
        "author": "Bill Lubanovic",
        "price": 27.49,
        "description": "Easy to understand and fun to read, this updated edition of Introducing Python is ideal for beginning programmers as well as those new to the language. Author Bill Lubanovic takes you from the basics to more involved and varied topics, mixing tutorials with cookbook-style code recipes to explain concepts in Python 3. End-of-chapter exercises help you practice what you’ve learned."
    }
]

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_response(status_code, content_type, content):
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: {content_type}\n\n{content}'
    return response.encode('utf-8')

def handle_request(request_data):
    request_lines = request_data.split('\n')
    
    if not request_lines:
        return generate_response(400, 'text/html', "Bad request")
    
    request_line = request_lines[0].strip().split()
    
    if not request_line:
        return generate_response(400, 'text/html', "Bad request")
    
    method, path = request_line[:2]

    if method == "GET":
        if path == '/home':
            return generate_response(200, 'text/html', "<h1>Home Page</h1>")
        elif path == '/about':
            return generate_response(200, 'text/html', "<h1>About Page</h1>")
        elif path.startswith('/product/'):
            try:
                product_index = int(path[len('/product/'):])
                if 0 <= product_index < len(products):
                    product = products[product_index]
                    product_info = f'<h1>{product["name"]}</h1><h2>Author: {product["author"]}</h2><h2>Price: ${product["price"]}</h2><p>{product["description"]}</p>'
                    return generate_response(200, 'text/html', product_info)
                else:
                    return generate_response(404, 'text/html', "Product not found")
            except ValueError:
                return generate_response(400, 'text/html', "Invalid product number")
        elif path == '/products':
            product_list = [f'<a href="/product/{i}">Product {i}: {products[i]["name"]}</a><br>' for i in range(len(products))]
            return generate_response(200, 'text/html', ''.join(product_list))
        else:
            return generate_response(404, 'text/html', "Page not found")
    else:
        return generate_response(405, 'text/html', "Method not allowed")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    try:
        request_data = client_socket.recv(1024).decode('utf-8')
        response = handle_request(request_data)
        client_socket.send(response)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
