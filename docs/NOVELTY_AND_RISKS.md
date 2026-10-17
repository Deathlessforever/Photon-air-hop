# Novelty, Assumptions, and Risks

## What is already known?

Photon-Air-Hop is entering an established research area. Related fields include visible-light communication (VLC), free-space optical (FSO) communication, non-line-of-sight optical communication, ultraviolet (UV) communication, optical wireless sensor networks, and relay/routing protocols. Atmospheric scattering and optical relaying are not, by themselves, new discoveries.

A proper literature and patent search has not yet been completed. Therefore, no patentability, originality, or freedom-to-operate conclusion is made here.

## Possible differentiation hypotheses

These are directions to investigate, not novelty claims:

- A low-cost, reproducible optical node for short emergency messages.
- Adaptive selection between direct, reflected, and scattering-assisted links based on measured link quality.
- A robust multi-hop protocol that accounts for intermittent optical visibility, duplicates, acknowledgements, energy, and node mobility.
- An experimental dataset comparing LOS and NLOS performance under controlled conditions using affordable components.

A differentiator only becomes credible when it is specific, compared with existing methods, and supported by measurements.

## Critical physical constraint

Scattering redirects only a fraction of transmitted optical energy toward a receiver. The received signal can fall rapidly with geometry and distance and can be overwhelmed by ambient light and detector noise. Air molecules do not automatically pass a digital message from one to another. Any “hop” requires a receiver/detector and a transmitter/relay, or a physically justified propagation mechanism.

## Main risks

| Risk | How to test or reduce it |
|---|---|
| Received light is too weak | Measure receiver noise floor and link budget; start at short range |
| Apparent NLOS signal is a reflection or direct leak | Use opaque baffles, blocked-path controls, and repeatable geometry |
| Ambient light causes false bits | Test lighting conditions, filters, modulation, and decision thresholds |
| Relay network is unreliable | Validate CRC, sequence numbers, acknowledgements, retries, and loop prevention |
| Claimed novelty already exists | Review papers, patents, standards, and commercial products before making claims |
| Simulation is mistaken for evidence | Label assumptions and simulated data; publish measured raw data separately |
| Safety hazard | Use low-power enclosed LEDs; avoid lasers and unsafe scattering media |

## Literature review checklist

Search and summarize papers/patents for:
1. NLOS visible-light communication and diffuse reflections.
2. UV scattering communication and atmospheric channel models.
3. FSO/VLC relay networks and routing.
4. Optical modulation, photodiode receiver sensitivity, and ambient-light rejection.
5. Existing disaster/emergency optical communication systems.

For each source record title, authors, year, venue/patent number, link, mechanism, reported range/data rate, equipment, and what differs from this project. Novelty must be assessed against the closest prior art, not just a broad keyword search.
