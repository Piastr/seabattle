import socket


def listen(host: str = '127.0.0.1', port: int = 2000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    members = []
    while True:
        msg, addr = s.recvfrom(4096)

        if addr not in members:
            members.append(addr)
        if not msg:
            continue

        client_id = addr[1]
        msg_text = msg.decode('ascii')
        if msg_text == '__join':
            print(f"Client {client_id} joined")
            continue

        if msg_text.startswith('__inwait'):
            port_to = msg_text[-4:]
            s.sendto(f'__inwait {client_id}'.encode('ascii'), ('127.0.0.1', int(port_to)))

        if msg_text.startswith('__no'):
            port_to = msg_text[-4:]
            s.sendto(f'__no {client_id}'.encode('ascii'), ('127.0.0.1', int(port_to)))

        if msg_text.startswith('__ok'):
            port_to = msg_text[-4:]
            s.sendto(f'__ok {client_id}'.encode('ascii'), ('127.0.0.1', int(port_to)))

        message_template = '{}__{}'
        if msg_text == '__members':
            print(f'Client {client_id} requested members')
            if len(members) == 0:
                s.sendto('Only you'.encode('ascii'), addr)
                continue
            else:
                active_members = [f'client{m[1]}' for m in members if m != addr]
                member_message = ';'.join(active_members)
                s.sendto(message_template.format('members', member_message).encode('ascii'), addr)
                continue

        if msg_text == '__exit':
            members.remove(addr)
            print(f'Client {client_id} disconnected')

        msg = f'client{client_id}: {msg.decode("ascii")}'

        for member in members:
            if member == addr:
                continue

            s.sendto(msg.encode('ascii'), member)


listen()
