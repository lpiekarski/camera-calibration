#!/usr/bin/env python3

import cv2
import numpy as np
import struct

MAGIC_STRING = b'deadbeef+deadbeef&deadbeef@deadbeef\n'
MAGIC_PACKET_LEN = len(MAGIC_STRING) + 3 * 4

SEQ_MOD = 2 ** 32
SEQ_CLEAN_DIST = 100000


class FrameBuilder:
    def __init__(self):
        self.store = {}
        self.active_frames = []
        self.ready_frames = []

    def check_seqs(self, start, end):
        for seq in range(start, end + 1):
            if seq not in self.store:
                return False
        return True

    def check_complete(self):
        i = 0
        while i < len(self.active_frames):
            magic_seq, packet_to, _ = self.active_frames[i]
            if self.check_seqs(magic_seq + 1, packet_to):
                img_bytes = b''
                for seq in range(magic_seq + 1, packet_to + 1):
                    img_bytes += self.store[seq]
                    del self.store[seq]
                img = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                self.ready_frames.append(img)
                del self.active_frames[i]

                to_del = [key for key in self.store.keys() if abs(magic_seq - key) > SEQ_CLEAN_DIST]
                for key in to_del:
                    del self.store[key]

                to_del = [i for i in range(len(self.active_frames))
                          if abs(magic_seq - self.active_frames[i][0]) > SEQ_CLEAN_DIST]
                for i in reversed(to_del):
                    del self.active_frames[i]
            else:
                i += 1

    def take_packet(self, data):
        if len(data) < 4:
            return

        if len(data) == MAGIC_PACKET_LEN and MAGIC_STRING == data[:len(MAGIC_STRING)]:
            img_size = struct.unpack_from("<I", data, len(MAGIC_STRING))[0]
            seq = struct.unpack_from("<I", data, len(MAGIC_STRING) + 4)[0]
            packet_to = struct.unpack_from("<I", data, len(MAGIC_STRING) + 8)[0]

            self.store[seq] = 0
            self.active_frames.append((seq, packet_to, img_size))
        else:
            seq = struct.unpack_from("<I", data)[0]
            if (seq - 1) % SEQ_MOD not in self.store:
                print(f"INVERSION DETECTED on seq {seq}")
            self.store[seq] = data[4:]

    def frames_available(self):
        self.check_complete()
        return len(self.ready_frames)


class SimpleFrameBuilder:
    def __init__(self, use_seqs=False):
        self.store = b''
        self.target_len = 0
        self.use_seqs = use_seqs
        self.last_seq = None
        self.ready_frames = []

    def detect_inversion(self, seq):
        if self.last_seq is not None and (self.last_seq + 1) % SEQ_MOD != seq:
            print(f"INVERSION DETECTED on seq {seq}")
        self.last_seq = seq

    def take_packet(self, data):
        if len(data) < 4:
            return

        if len(data) == MAGIC_PACKET_LEN and MAGIC_STRING == data[:len(MAGIC_STRING)]:
            img_size = struct.unpack_from("<I", data, len(MAGIC_STRING))[0]

            self.store = b''
            self.target_len = img_size

            if self.use_seqs:
                seq = struct.unpack_from("<I", data, len(MAGIC_STRING) + 4)[0]
                self.detect_inversion(seq)
        else:
            if self.use_seqs:
                seq = struct.unpack_from("<I", data)[0]
                self.detect_inversion(seq)
                self.store += data[4:]
            else:
                self.store += data

            if len(self.store) > self.target_len:
                print(f"Overrun detected, wanted {self.target_len}, got {len(self.store)}, last {len(data) - 4}")
            elif len(self.store) == self.target_len:
                img = cv2.imdecode(np.frombuffer(self.store, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                self.ready_frames.append(img)

    def frames_available(self):
        return len(self.ready_frames)
