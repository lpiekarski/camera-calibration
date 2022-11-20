#!/usr/bin/env python3

import socket
import time

from cam.frame_builders import FrameBuilder

RESOLUTIONS = {
    0: (96, 96),
    1: (160, 120),
    2: (176, 144),
    3: (240, 176),
    4: (240, 240),
    5: (320, 240),
    6: (400, 296),
    7: (480, 320),
    8: (640, 480),
    9: (800, 600),
    10: (1024, 768),
    11: (1280, 720),
    12: (1280, 1024),
    13: (1600, 1200)
}

RECV_BUFFER_SIZE = 2048
CONTROL_PORT = 4242
MIN_KEEPALIVE_DELAY = 0.1


def listen_udp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def connect_tcp(ip, port, nodelay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    if nodelay:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    return sock


class Camera:
    def __init__(self, quality=9, camera_ip="192.168.4.1", my_ip="192.168.4.2", recv_port=4545):
        self.quality = quality
        self.my_ip = my_ip
        self.recv_port = recv_port

        self.sock_control = connect_tcp(camera_ip, CONTROL_PORT)
        self.sock_stream = listen_udp(my_ip, recv_port)

        self.builder = FrameBuilder()

        self.last_keepalive = 0
        self.keep_stream_alive()

    def get_frame(self):
        while not self.builder.frames_available():
            self.keep_stream_alive()
            data, _ = self.sock_stream.recvfrom(RECV_BUFFER_SIZE)
            self.builder.take_packet(data)

        img = self.builder.ready_frames[-1]
        self.builder.ready_frames = []
        return img

    def get_quality(self):
        return self.quality

    def set_quality(self, quality):
        self.quality = quality

    def keep_stream_alive(self):
        now = time.time()
        if now > self.last_keepalive + MIN_KEEPALIVE_DELAY:
            self.last_keepalive = now
            self.sock_control.send(f"stream {self.my_ip} {self.recv_port} {self.quality}\n".encode())

    # def __del__(self):
    #     self.sock_control.close()
    #     self.sock_stream.close()
