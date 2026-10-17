# Experiment Plan

## Objective

Establish the simplest measurable optical communication link, then test whether a non-line-of-sight optical path offers any useful, repeatable communication capability.

## Stage 0 — Define the setup

Record:
- LED type, wavelength if known, drive current, modulation method, and measured electrical power.
- Receiver/sensor model, active area, field of view, analogue gain, sample rate, and filtering.
- Room dimensions, transmitter/receiver positions, path distance, angle, ambient-light conditions, and any optical surfaces or scattering medium.
- Firmware/software commit, frame format, payload, and test procedure.

Use a low-power LED in an enclosed setup. Do not use lasers for the initial experiment.

## Stage 1 — LOS baseline

1. Encode a short repeating bit sequence and a small text payload.
2. Use a frame with preamble, length, sequence number, payload, and CRC.
3. Start at short range and increase distance gradually.
4. At each condition, send at least 1,000 frames or bits and log successful frames, CRC failures, estimated bit errors, received amplitude, and power.
5. Repeat each point several times; keep the receiver and lighting configuration documented.

**Pass criterion:** reliable decoding at a stated short distance with repeatable results. Choose numeric thresholds before collecting data rather than after seeing the result.

## Stage 2 — Channel factors

Vary one factor at a time:
- Distance.
- Receiver angle and transmitter angle.
- Ambient illumination.
- Receiver field of view / optical filter, if available.
- Reflected path using a safe, matte target.
- Controlled scattering only after the baseline works.

Never infer “communication through air scattering” from a signal that may actually be a direct leak, reflection, or electrical coupling. Use opaque baffles and control tests to identify the real path.

## Stage 3 — NLOS/scattering test

- Block the direct optical path with an opaque barrier.
- Keep transmitter and receiver electrically isolated.
- Compare the target path against a dark/no-transmitter control and a blocked-path control.
- Record the optical geometry and medium; do not aerosolize chemicals or create unsafe airborne particles.
- Report the receiver noise floor, signal-to-noise ratio where measurable, packet success rate, bit-error rate, and uncertainty.

If decoding fails, report the upper bound implied by the measurement sensitivity. Do not interpret a sensor reading alone as successful data communication.

## Stage 4 — Two-hop relay

Use three nodes: A, B, and C. Ensure A cannot communicate directly with C. B must verify CRC, suppress duplicate sequence numbers, and forward the message under a documented rule. Measure end-to-end delivery rate, latency, energy per delivered message, and duplicate/loss behavior.

## Data table

Recommended CSV columns:

`timestamp,run_id,tx_id,rx_id,mode,distance_m,tx_angle_deg,rx_angle_deg,ambient_lux,tx_power_mW,rx_amplitude,noise_rms,frames_sent,frames_valid,crc_failures,bit_errors,bits_sent,notes`

Do not fabricate or fill measured columns with simulated values. Keep simulations in separate files.

## Safety

Use an eye-safe LED, current limiting, and enclosed optical paths. Do not point any source at eyes, traffic, aircraft, or the public. Avoid improvised high-power optical emitters and hazardous aerosol generation.
