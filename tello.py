import socket


class Drone:
    def __init__(self, debug=True):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.bind(("", 9000))
        self.addr = ("192.168.10.1", 8889)
        self.socket = _socket

        self.debug = debug

        self.failure = False
        self.airlift = False
        self.monitoring = False
        self.thread = None

    def send(self, command):
        if self.debug:
            print("> ", command)
        self.socket.sendto(command.encode("utf-8"), self.addr)
        result = self.recv().strip()
        if self.debug:
            print("< ", result)
        if result == "error":
            self.emergency()
        return result

    def recv(self):
        while True:
            resp, addr = self.socket.recvfrom(1024)
            if addr != self.addr:
                continue
            return resp.decode("utf-8")

    def emergency(self):
        self.socket.sendto(b"emergency", self.addr)
        raise RuntimeError("EMERGENCY")

    def status(self):
        print(f"Time: {self.time}\tToF: {self.tof}")
        print(f"Battery: {self.battery}\tTemperature: {self.temp}")
        print(f"Height: {self.speed}\tHeight: {self.acceleration}")
        print(f"Height: {self.height}")
        print(f"Attitude: {self.attitude}")
        print(f"Baro: {self.baro}")

    def command(self):
        self.send("command")

    def takeoff(self):
        self.airlift = True
        self.send("takeoff")

    def land(self):
        self.send("land")
        self.airlift = False

    def __del__(self):
        if self.monitoring:
            self.monitoring = False

        if self.airlift:
            self.emergency()

    def move(self, move, amount):
        if move in {"up", "down", "left", "right", "forward", "back"}:
            if 20 > amount > 500:
                raise ValueError("amount must be 20-500")
        elif move in {"cw", "ccw"}:
            if 1 > amount > 360:
                raise ValueError("amount must be 1-360")
        else:
            raise ValueError("unknown move")

        self.send(f"{move} {amount}")

    def up(self, amount):
        self.move("up", amount)

    def down(self, amount):
        self.move("down", amount)

    def left(self, amount):
        self.move("left", amount)

    def right(self, amount):
        self.move("right", amount)

    def forward(self, amount):
        self.move("forward", amount)

    def backward(self, amount):
        self.move("back", amount)

    def flip(self, direction):
        if direction in {"l", "r", "f", "b"}:
            self.send(f"flip {direction}")
        else:
            raise ValueError("unknown direction")

    def left_flip(self):
        self.flip("l")

    def right_flip(self):
        self.flip("r")

    def front_flip(self):
        self.flip("f")

    def back_flip(self):
        self.flip("b")

    def query(self, attribute):
        return self.send(f"{attribute}?")

    @property
    def time(self):
        return self.query("time")

    @property
    def tof(self):
        return self.query("tof")

    @property
    def battery(self):
        return self.query("battery")

    @property
    def temp(self):
        return self.query("temp")

    @property
    def height(self):
        return self.query("height")

    @property
    def attitude(self):
        return self.query("attitude")

    @property
    def baro(self):
        return self.query("baro")

    @property
    def acceleration(self):
        return self.query("acceleration")

    @property
    def speed(self):
        return self.query("speed")

    @property
    def wifi(self):
        return self.query("wifi")

    @property
    def sdk(self):
        return self.query("sdk")

    @property
    def sn(self):
        return self.query("sn")
