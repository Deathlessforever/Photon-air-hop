# Hardware / Software Interface Contract

This document is the integration boundary between the hardware prototype and the software protocol.

## Current status

The packet framing and graph-routing modules are implemented as a software prototype. No physical modulation, demodulation, or detector driver has been implemented or verified yet. The hardware measurements must determine the actual bit rate and framing timing.

## Minimum transmitter interface

The transmitter must accept a complete frame as bytes and emit it over the selected optical modulation method.

Conceptual API:

```python
transmitter.send_bytes(frame.encode())
```

The first physical prototype can use on-off keying (OOK) if the hardware supports it. A preamble/synchronization pattern and line coding are still to be specified based on the chosen microcontroller, LED driver, detector, and sampling rate.

## Minimum receiver interface

The receiver should return complete candidate frames as bytes, or provide sampled data to a separate decoder. Do not pass arbitrary sensor readings directly to the packet decoder.

Conceptual API:

```python
wire_bytes = receiver.receive_frame()
frame = Frame.decode(wire_bytes)  # rejects invalid length, magic, version, or CRC
```

## Required measurements from the hardware side

Please record these fields for each test run:
- Transmitter LED part number / wavelength if known and drive current.
- Receiver sensor and analogue front-end details.
- Optical power if measurable; otherwise clearly state the measurement method.
- Modulation method, symbol rate, sampling rate, and preamble design.
- Distance, transmitter/receiver angle, path geometry, and ambient illuminance.
- Total frames, valid frames, CRC failures, estimated bit errors, and test duration.
- Any reflections, direct-path leaks, or other possible confounders.

## Integration acceptance tests

1. Send a known byte sequence over the optical hardware and recover the exact bytes.
2. Send a valid encoded `Frame` and decode it on the receiver.
3. Flip one received payload bit and verify that CRC validation rejects it.
4. Test several distances and ambient-light conditions, retaining raw logs.
5. After single-hop is repeatable, connect two optical links through a relay node.

## Safety

Use an enclosed, current-limited, low-power LED setup. Do not use lasers or aim optical emitters at eyes, roads, aircraft, or the public. Do not create hazardous aerosols to simulate atmospheric scattering.
