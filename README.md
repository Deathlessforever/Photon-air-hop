# Photon-Air-Hop

**Research project:** atmospheric optical communication and adaptive multi-hop optical links.

Photon-Air-Hop investigates whether low-cost optical transmitters and sensitive receivers can exchange short messages through atmospheric paths, including non-line-of-sight (NLOS) paths where direct visibility is obstructed. A longer-term research question is whether several optical nodes can relay a message across multiple viable links.

> **Status:** early research and feasibility testing. This repository does not claim a working long-range system, a new physical effect, or proven novelty. Experiments and simulations must be clearly distinguished from measured results.

## Why investigate this?

Radio links can be unavailable, congested, damaged, or undesirable in some scenarios. Optical links offer a different physical layer and may be useful for short-range, directional, or infrastructure-light communication. Atmospheric scattering can redirect some light, but it also causes substantial path loss and background-noise challenges. The central question is not whether photons exist in air; it is whether a measurable, decodable signal can reach a receiver with useful reliability and energy cost.

## Research questions

1. Can a low-power, eye-safe LED transmitter send a simple encoded message to a photodetector over a controlled optical path?
2. How do distance, angle, ambient light, receiver field of view, and scattering conditions affect signal-to-noise ratio and bit-error rate?
3. Can a receiver detect a deliberately reflected or scattered path without confusing ambient light for data?
4. What routing and acknowledgement strategy would be needed for a network of optical relay nodes?
5. Under what conditions would this complement, rather than outperform, conventional radio or established free-space optical systems?

## Proposed architecture (hypothesis)

- **Transmitter:** modulated, low-power LED; framed digital bits with preamble, payload, and checksum.
- **Optical channel:** direct, reflected, or controlled-scattering path. These are different test cases and must not be treated as interchangeable.
- **Receiver:** photodiode or light sensor, analogue front-end, sampling, threshold/timing recovery, and frame validation.
- **Link layer:** node ID, sequence number, CRC, acknowledgements, retry limits, and link-quality estimate.
- **Multi-hop layer:** forward only when a relay has a validated frame and a route/duplicate policy. Each hop is a separate optical link; relaying is not automatic propagation between air molecules.

## First milestone

Prove a short, repeatable **line-of-sight (LOS)** optical data link indoors before attempting NLOS/scattering experiments. Use an eye-safe LED, not a laser. Log received signal, successful frames, bit errors, range, angle, ambient-light conditions, and power. Then add controlled reflection/scattering and compare against the LOS baseline.

See:
- [Experiment plan](docs/EXPERIMENT_PLAN.md)
- [Novelty, assumptions, and risks](docs/NOVELTY_AND_RISKS.md)
- [Simple optical link budget model](simulation/optical_link.py)

## Safety and scientific integrity

- Use low-power LEDs and enclosed test setups; never aim optical sources at eyes, roads, aircraft, or people.
- Do not claim kilometre-scale range, emergency readiness, or superiority over radio without independently repeatable measurements.
- Label simulated values as illustrative. The simple model in this repository is not a substitute for optical design, calibrated measurements, or a validated atmospheric propagation model.
- Check applicable electrical, optical-safety, privacy, and radio/telecom rules before field testing.

## Development stages

1. **Bench link:** transmitter, receiver, framed bits, CRC, repeatable measurements.
2. **Channel characterization:** distance, angle, ambient light, and controlled optical scatter/reflection.
3. **Robustness:** adaptive thresholds, coding, acknowledgements, retries, and energy measurements.
4. **Two-hop proof:** three nodes; A sends to B, B validates and forwards to C.
5. **Research review:** compare with published VLC, free-space optical, NLOS optical, and UV communication work before making novelty claims.

## Contributions

Keep experiments reproducible. Every result should state hardware, circuit/software version, environment, test count, raw measurements, and uncertainty. Failed tests are valuable results too.

## Software prototype

The first software modules are intentionally small and testable:

- `software/photon_air_hop/packet.py`: versioned binary frame, length validation, CRC-16/CCITT-FALSE, and TTL-aware forwarding helper.
- `software/photon_air_hop/network.py`: deterministic graph-based multi-hop simulator. Edges represent links you explicitly declare usable.
- `software/tests/test_protocol.py`: unit tests for packet integrity, malformed frames, TTL, and a three-node route.

Run tests from the repository root:

```bash
PYTHONPATH=software python -m unittest discover -s software/tests -v
```

**Important:** the graph simulator is not a physical optical-channel simulator. It does not predict atmospheric scattering, receiver sensitivity, packet error rates, or real-world range. Those need hardware measurements and a validated channel model.
