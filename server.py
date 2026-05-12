import socket
import hmac
import hashlib
import json
import logging
from config import SECRET_KEY, HOST, PORT

# (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SERVER - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("server.log"), logging.StreamHandler()]
)


def verify_hmac(message, received_mac):
    """Gjeneron HMAC-un për mesazhin e marrë dhe e krahason me atë të dërguarin."""
    # Gjenerojmë HMAC me SHA-256
    calculated_mac = hmac.new(SECRET_KEY, message.encode('utf-8'), hashlib.sha256).hexdigest()

    # Përdorim compare_digest për të parandaluar Timing Attacks
    return hmac.compare_digest(calculated_mac, received_mac)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server started and awaiting messages...")
        logging.info(f"Serveri po dëgjon në {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                logging.info(f"U lidh klienti: {addr}")
                try:
                    data = conn.recv(2048)
                    if not data:
                        break

                    # Parsimi i protokollit të komunikimit (JSON)
                    payload = json.loads(data.decode('utf-8'))
                    message = payload.get('message')
                    received_mac = payload.get('hmac')

                    # Printimi në konsole siç kërkohet në detyrë
                    print(f"Message received with HMAC: [{message} | {received_mac}]")
                    logging.info("Mesazhi u pranua. Po fillon verifikimi i HMAC...")
                    print("Validating HMAC...")

                    if verify_hmac(message, received_mac):
                        print("Message verified successfully. Integrity and authenticity confirmed.\n")
                        logging.info("Verifikimi i HMAC përfundoi me sukses.")
                        response = {"status": "success", "message": "Message verified successfully."}
                    else:
                        print("HMAC verification failed! Message may be tampered.\n")
                        logging.warning("Kujdes: Verifikimi i HMAC dështoi. Mesazhi mund të jetë modifikuar!")
                        response = {"status": "error", "message": "HMAC verification failed. Integrity compromised."}

                    # Dërgimi i përgjigjes te klienti
                    conn.sendall(json.dumps(response).encode('utf-8'))

                except json.JSONDecodeError:
                    logging.error("U pranua një format i pavlefshëm të dhënash.")
                except Exception as e:
                    logging.error(f"Gabim gjatë komunikimit: {e}")


if __name__ == "__main__":
    start_server()