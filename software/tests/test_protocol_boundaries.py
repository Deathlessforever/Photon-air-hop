"""Boundary and forwarding regression tests for the experimental frame format."""
import unittest

from photon_air_hop import Frame, FrameError, OpticalMesh


class FrameBoundaryTests(unittest.TestCase):
    def test_empty_payload_round_trips(self):
        frame = Frame(0, 65535, 0, 0, b"")
        self.assertEqual(Frame.decode(frame.encode()), frame)

    def test_maximum_payload_round_trips(self):
        payload = bytes(range(256)) * 2
        frame = Frame(65535, 0, 0xFFFFFFFF, 255, payload)
        self.assertEqual(len(payload), 512)
        self.assertEqual(Frame.decode(frame.encode()), frame)

    def test_invalid_magic_is_rejected_before_crc(self):
        wire = bytearray(Frame(1, 2, 3, 4, b"SOS").encode())
        wire[0] ^= 0x01
        with self.assertRaisesRegex(FrameError, "invalid magic"):
            Frame.decode(bytes(wire))

    def test_unsupported_version_is_rejected(self):
        wire = bytearray(Frame(1, 2, 3, 4, b"SOS").encode())
        wire[4] = 2
        with self.assertRaisesRegex(FrameError, "unsupported version"):
            Frame.decode(bytes(wire))

    def test_truncated_frame_is_rejected(self):
        wire = Frame(1, 2, 3, 4, b"SOS").encode()
        with self.assertRaises(FrameError):
            Frame.decode(wire[:-1])

    def test_forwarding_changes_only_relay_fields(self):
        original = Frame(1, 9, 42, 3, b"HELP")
        forwarded = original.forwarded(relay_id=5)
        self.assertEqual(forwarded.source, 5)
        self.assertEqual(forwarded.destination, original.destination)
        self.assertEqual(forwarded.sequence, original.sequence)
        self.assertEqual(forwarded.ttl, 2)
        self.assertEqual(forwarded.payload, original.payload)

    def test_shortest_route_is_deterministic_for_equal_length_paths(self):
        mesh = OpticalMesh([(1, 3), (1, 2), (2, 4), (3, 4)])
        self.assertEqual(mesh.shortest_route(1, 4), (1, 2, 4))


if __name__ == "__main__":
    unittest.main()
