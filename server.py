import socket
import threading

# Thiết lập thông số máy chủ
HOST = '127.0.0.1'  # Địa chỉ IP của máy chủ
PORT = 12345        # Cổng máy chủ

# Khởi tạo socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

# Hàm xử lý các tin nhắn từ client
def handle_client(client):
    while True:
        try:
            # Nhận dữ liệu từ client
            data = client.recv(1024)
            if not data:
                break

            # Phát tán dữ liệu đến tất cả client khác
            for c in clients:
                if c != client:
                    c.send(data)
        except:
            clients.remove(client)
            client.close()
            break

# Hàm chờ và xử lý kết nối từ các client mới
def receive_connections():
    while True:
        client, addr = server.accept()
        print(f"Client {addr} đã kết nối.")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Máy chủ đang chạy...")
receive_connections()
