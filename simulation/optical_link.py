#!/usr/bin/env python3
"""Illustrative optical link-budget calculator; not a validated atmospheric model.

This estimates received optical power using a simple inverse-square geometric
term and exponential extinction. Real diffuse/NLOS paths require a measured
or validated radiative-transfer/channel model and may behave very differently.

Example:
  python simulation/optical_link.py --tx-mw 5 --distance-m 2 --beam-angle-deg 30 --extinction-per-m 0.05
"""
import argparse
import math


def estimate_received_power_w(tx_power_w, distance_m, beam_angle_deg, extinction_per_m):
    if tx_power_w <= 0:
        raise ValueError("tx power must be positive")
    if distance_m <= 0:
        raise ValueError("distance must be positive")
    if not 0 < beam_angle_deg < 179:
        raise ValueError("beam angle must be between 0 and 179 degrees")
    if extinction_per_m < 0:
        raise ValueError("extinction coefficient cannot be negative")

    # Approximate illuminated cone area at range r. Assumes a uniform beam,
    # on-axis receiver, and no reflections/scattering into the receiver.
    radius = distance_m * math.tan(math.radians(beam_angle_deg / 2))
    area = math.pi * radius * radius
    if area == 0:
        raise ValueError("beam footprint is zero; check beam angle")

    # A hypothetical receiver aperture is used to illustrate geometry.
    receiver_diameter_m = 0.01
    receiver_area = math.pi * (receiver_diameter_m / 2) ** 2
    geometric_fraction = min(1.0, receiver_area / area)
    transmission = math.exp(-extinction_per_m * distance_m)
    return tx_power_w * geometric_fraction * transmission


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tx-mw", type=float, default=5.0, help="transmitter optical power in mW")
    parser.add_argument("--distance-m", type=float, default=1.0, help="distance in metres")
    parser.add_argument("--beam-angle-deg", type=float, default=30.0, help="full-angle beam spread in degrees")
    parser.add_argument("--extinction-per-m", type=float, default=0.0, help="assumed extinction coefficient in 1/m")
    args = parser.parse_args()

    rx_w = estimate_received_power_w(
        args.tx_mw / 1000.0,
        args.distance_m,
        args.beam_angle_deg,
        args.extinction_per_m,
    )
    print("ILLUSTRATIVE ESTIMATE ONLY — not a measured result")
    print(f"Tx optical power:       {args.tx_mw:.6g} mW")
    print(f"Distance:               {args.distance_m:.6g} m")
    print(f"Beam full angle:        {args.beam_angle_deg:.6g} degrees")
    print(f"Assumed extinction:     {args.extinction_per_m:.6g} 1/m")
    print(f"Estimated Rx power:     {rx_w:.6g} W ({rx_w * 1e9:.6g} nW)")
    print("This model excludes detector sensitivity, receiver optics, alignment error,")
    print("ambient light, modulation bandwidth, and any NLOS scattering gain.")


if __name__ == "__main__":
    main()
