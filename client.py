import socket
import hmac
import hashlib
import json
import logging
from config import SECRET_KEY, HOST, PORT

# (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CLIENT - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("client.log"), logging.StreamHandler()]
)


def generate_hmac(message):
    """Krijon një HMAC duke përdorur çelësin sekret dhe SHA-256."""
    return hmac.new(SECRET_KEY, message.encode('utf-8'), hashlib.sha256).hexdigest()


def start_client():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        mac = generate_hmac(message)

        # Printimi në konsole siç kërkohet në detyrë
        print(f"Sending message with HMAC: [{message} | {mac}]")
        logging.info("Gjenerimi i HMAC përfundoi. Po dërgohet mesazhi te serveri...")

        # Përgatitja e protokollit të komunikimit (JSON)
        payload = json.dumps({"message": message, "hmac": mac})

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(payload.encode('utf-8'))

                # Marrja e përgjigjes nga serveri
                data = s.recv(2048)
                response = json.loads(data.decode('utf-8'))

                print(f"Server response: {response['message']}\n")
                logging.info(f"Përgjigjja nga serveri: {response['status']}")

        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?\n")
            logging.error("Lidhja u refuzua nga serveri. Kontrolloni nëse server.py është aktiv.")
        except Exception as e:
            print(f"An error occurred: {e}\n")
            logging.error(f"Gabim i papritur: {e}")


if __name__ == "__main__":
    start_client()