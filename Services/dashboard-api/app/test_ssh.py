import socket

def is_tunnel_forwarder_active(local_port):
    try:
        # Attempt to open a socket connection to the local port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set a timeout for the connection attempt
            s.connect(('localhost', local_port))
        return True  # If connection succeeds, tunnel is active
    except Exception:
        return False  # If connection fails, tunnel is not active

# Replace 'local_port' with the port number being forwarded locally
local_port = 5433  # Replace with your local port number

if is_tunnel_forwarder_active(local_port):
    print("SSH tunnel forwarder is active.")
else:
    print("SSH tunnel forwarder is not active.")
