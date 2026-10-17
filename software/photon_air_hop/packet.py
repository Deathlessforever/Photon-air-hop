"""Binary frame format for Photon-Air-Hop's software prototype.

This is an experimental application-layer framing format, not a standard.
All multibyte integers are big-endian. CRC-16/CCITT-FALSE covers header+payload.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import ClassVar

MAGIC = b"PAH1"
VERSION = 1
MAX_PAYLOAD = 512
# magic, version, src, dst, sequence, ttl, payload length
_HEADER = struct.Struct(">4sBHHIBH")
_CRC = struct.Struct(">H")
CRC_INIT = 0xFFFF
CRC_POLY = 0x1021


class FrameError(ValueError):
    """Raised when a frame is malformed or fails integrity checks."""


def crc16_ccitt(data: bytes, initial: int = CRC_INIT) -> int:
    """CRC-16/CCITT-FALSE: poly=0x1021, init=0xFFFF, no reflection/xorout."""
    crc = initial
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ CRC_POLY) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


@dataclass(frozen=True, slots=True)
class Frame:
    source: int
    destination: int
    sequence: int
    ttl: int
    payload: bytes
    version: int = VERSION

    MAGIC: ClassVar[bytes] = MAGIC

    def __post_init__(self) -> None:
        if not 0 <= self.source <= 0xFFFF:
            raise FrameError("source must fit in uint16")
        if not 0 <= self.destination <= 0xFFFF:
            raise FrameError("destination must fit in uint16")
        if not 0 <= self.sequence <= 0xFFFFFFFF:
            raise FrameError("sequence must fit in uint32")
        if not 0 <= self.ttl <= 0xFF:
            raise FrameError("ttl must fit in uint8")
        if self.version != VERSION:
            raise FrameError(f"unsupported version: {self.version}")
        if not isinstance(self.payload, bytes):
            raise FrameError("payload must be bytes")
        if len(self.payload) > MAX_PAYLOAD:
            raise FrameError(f"payload exceeds {MAX_PAYLOAD} bytes")

    def encode(self) -> bytes:
        header = _HEADER.pack(
            MAGIC, self.version, self.source, self.destination,
            self.sequence, self.ttl, len(self.payload)
        )
        body = header + self.payload
        return body + _CRC.pack(crc16_ccitt(body))

    @classmethod
    def decode(cls, wire: bytes) -> "Frame":
        if len(wire) < _HEADER.size + _CRC.size:
            raise FrameError("frame is too short")
        magic, version, source, destination, sequence, ttl, length = _HEADER.unpack_from(wire)
        if magic != MAGIC:
            raise FrameError("invalid magic")
        if version != VERSION:
            raise FrameError(f"unsupported version: {version}")
        if length > MAX_PAYLOAD:
            raise FrameError("payload length exceeds limit")
        expected_size = _HEADER.size + length + _CRC.size
        if len(wire) != expected_size:
            raise FrameError("frame length does not match header")
        expected_crc = _CRC.unpack_from(wire, expected_size - _CRC.size)[0]
        actual_crc = crc16_ccitt(wire[:-_CRC.size])
        if expected_crc != actual_crc:
            raise FrameError("CRC mismatch")
        payload = wire[_HEADER.size:-_CRC.size]
        return cls(source, destination, sequence, ttl, payload, version)

    def forwarded(self, relay_id: int) -> "Frame":
        """Return a copy with relay as source and TTL decremented."""
        if self.ttl <= 1:
            raise FrameError("TTL exhausted; frame must not be forwarded")
        return Frame(
            source=relay_id,
            destination=self.destination,
            sequence=self.sequence,
            ttl=self.ttl - 1,
            payload=self.payload,
            version=self.version,
        )
