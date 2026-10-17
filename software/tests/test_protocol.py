import unittest

from photon_air_hop import Frame, FrameError, OpticalMesh, crc16_ccitt


class PacketTests(unittest.TestCase):
    def test_crc_known_vector(self):
        self.assertEqual(crc16_ccitt(b"123456789"), 0x29B1)

    def test_round_trip(self):
        original = Frame(source=1, destination=9, sequence=42, ttl=4, payload=b"SOS")
        self.assertEqual(Frame.decode(original.encode()), original)

    def test_corruption_is_detected(self):
        wire = bytearray(Frame(1, 2, 3, 4, b"SOS").encode())
        wire[-3] ^= 0x01
        with self.assertRaisesRegex(FrameError, "CRC mismatch"):
            Frame.decode(bytes(wire))

    def test_bad_length_is_rejected(self):
        wire = Frame(1, 2, 3, 4, b"SOS").encode() + b"extra"
        with self.assertRaisesRegex(FrameError, "length"):
            Frame.decode(wire)

    def test_ttl_cannot_be_forwarded_when_exhausted(self):
        with self.assertRaisesRegex(FrameError, "TTL exhausted"):
            Frame(1, 3, 7, 1, b"SOS").forwarded(2)


class MeshTests(unittest.TestCase):
    def test_three_node_relay(self):
        mesh = OpticalMesh([(1, 2), (2, 3)])
        frame = Frame(1, 3, 10, 4, b"SOS")
        result = mesh.transmit(frame)
        self.assertTrue(result.delivered)
        self.assertEqual(result.route, (1, 2, 3))
        self.assertEqual(result.hops, 2)

    def test_no_direct_or_relay_route(self):
        mesh = OpticalMesh([(1, 2)])
        result = mesh.transmit(Frame(1, 3, 11, 4, b"SOS"))
        self.assertFalse(result.delivered)
        self.assertEqual(result.reason, "no route in current link graph")

    def test_ttl_limits_route(self):
        mesh = OpticalMesh([(1, 2), (2, 3), (3, 4)])
        result = mesh.transmit(Frame(1, 4, 12, 2, b"SOS"))
        self.assertFalse(result.delivered)
        self.assertEqual(result.reason, "TTL would be exhausted")


if __name__ == "__main__":
    unittest.main()
