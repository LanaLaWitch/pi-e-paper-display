class PicoLogger:

    def __init__(self, sock):
        self.sock = sock

    def _send(self, level, message):
        log = f"[{level}] {self.name}: {message}"
        self.sock.sendto(log.encode(), (self.host, self.port))

    def info(self, message):
        self._send("INFO", message)

    def error(self, message):
        self._send("ERROR", message)

    def debug(self, message):
        self._send("DEBUG", message)