# HMAC-Client-Server-Sec

Markdown
# Klient-Server Komunikimi i Sigurt me HMAC (SHA-256)

Ky projekt implementon një sistem të thjeshtë klient-server duke përdorur *sockets* në Python. Qëllimi kryesor është sigurimi i integritetit dhe autenticitetit të mesazheve që shkëmbehen përmes rrjetit duke përdorur **HMAC (Hash-based Message Authentication Code)** me algoritmin **SHA-256**.

---

## 1. Udhëzimet e hollësishme për ekzekutimin e programit

Për të ekzekutuar këtë projekt, sigurohuni që keni Python të instaluar (Versioni 3.x ose më i ri). Nuk ka nevojë për instalim të librarive të jashtme pasi të gjitha modulet e përdorura janë pjesë e librarisë standarde të Python.

### Hapat për ekzekutim:

1. **Struktura e skedarëve:** Sigurohuni që në të njëjtën direktori (folder) të keni këta tre skedarë:
   * `config.py` (përmban konfigurimet si çelësin sekret, host-in dhe portën)
   * `server.py` (kodi i serverit)
   * `client.py` (kodi i klientit)

2. **Hapi i parë - Nisja e Serverit:**
   Hapni një terminal (ose Command Prompt / PowerShell) në direktorinë e projektit dhe ekzekutoni komandën:
   ```bash
   python server.py
Serveri do të nisë dhe do të qëndrojë në pritje të mesazheve nga klienti.

Hapi i dytë - Nisja e Klientit:
Hapni një terminal të ri (dritare të dytë) po në atë direktori dhe ekzekutoni komandën:

Bash
python client.py
Komunikimi:

Te terminali i klientit, shkruani një mesazh dhe shtypni Enter.

Për të mbyllur klientin, shkruani exit.

2. Përshkrimi i pjesëve të implementuara në program
Projekti është i ndarë në komponentë logjikë për të mundësuar një arkitekturë të pastër klient-server:

Konfigurimi (config.py): Përmban variablat globale si HOST, PORT dhe SECRET_KEY. Ky çelës sekret (SECRET_KEY) luaj një rol kyç, pasi përdoret nga të dyja palët për të garantuar që vetëm dikush që e di çelësin mund të gjenerojë apo verifikojë mesazhet.

Gjenerimi i HMAC (client.py): Klienti merr mesazhin nga përdoruesi dhe përmes funksionit generate_hmac(message) krijon një nënshkrim unik (hash) duke përdorur çelësin sekret dhe SHA-256. Ky nënshkrim dërgohet bashkë me mesazhin në format JSON.

Verifikimi i HMAC (server.py): Serveri pranon strukturën JSON, ndan mesazhin nga HMAC-u i pranuar dhe përmes funksionit verify_hmac() llogarit një HMAC të ri lokal mbi atë mesazh. Për krahasim përdoret hmac.compare_digest për të shmangur sulmet e bazuara në kohë (Timing Attacks). Nëse përputhen, integriteti i të dhënave konfirmohet.

Protokolli i Komunikimit (JSON & Sockets): Komunikimi realizohet përmes TCP Sockets (socket.AF_INET, socket.SOCK_STREAM). Të dhënat paketohen në formatin JSON për t'u strukturuar qartë dhe dekodohen nga binarë në tekst (utf-8).

Sistemi i Logimit (logging): Të dy skedarët përdorin modulin logging për të ruajtur historikun e eventeve (lidhet klienti, dështoi verifikimi, etj.) si në konzollë ashtu edhe në skedarë të dedikuar (server.log dhe client.log).

3. Shembuj të rezultateve të ekzekutimit
Më poshtë paraqitet një shembull real se si duket dritarja e serverit dhe e klientit gjatë një komunikimi të suksesshëm:

Pamja në terminalin e Klientit (Client.py):
Plaintext
Enter your message (or 'exit' to quit): Pershendetje Profesor
Sending message with HMAC: [Pershendetje Profesor | a6f8c7d8e9...gjenerohet_nje_hash_sha256...]
2026-05-16 19:30:15,123 - CLIENT - INFO - Gjenerimi i HMAC përfundoi. Po dërgohet mesazhi te serveri...
Server response: Message verified successfully.
2026-05-16 19:30:15,126 - CLIENT - INFO - Përgjigjja nga serveri: success

Enter your message (or 'exit' to quit): exit
Pamja në terminalin e Serverit (Server.py):
Plaintext
Server started and awaiting messages...
2026-05-16 19:29:50,442 - SERVER - INFO - Serveri po dëgjon në 127.0.0.1:65432
2026-05-16 19:30:15,124 - SERVER - INFO - U lidh klienti: ('127.0.0.1', 54321)
Message received with HMAC: [Pershendetje Profesor | a6f8c7d8e9...gjenerohet_nje_hash_sha256...]
2026-05-16 19:30:15,125 - SERVER - INFO - Mesazhi u pranua. Po fillon verifikimi i HMAC...
Validating HMAC...
Message verified successfully. Integrity and authenticity confirmed.

2026-05-16 19:30:15,125 - SERVER - INFO - Verifikimi i HMAC përfundoi me sukses.
(Shënim: Në rast se dikush do të ndërhynte në rrjet për të ndryshuar qoftë edhe një shkronjë të mesazhit, serveri do të shfaqte mesazhin: HMAC verification failed! Message may be tampered.)
