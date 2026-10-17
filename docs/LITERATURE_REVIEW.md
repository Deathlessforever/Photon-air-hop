# Starter Literature Review

This is a **starter bibliography**, not an exhaustive literature or patent search. Read the full papers and record the closest prior art before making novelty claims.

## 1. Non-line-of-sight visible-light communication

**“Non-line of sight visible light communications: A technical and application based survey.”** *Optik*, volume 259, June 2022, article 168982.  
Publisher page: https://www.sciencedirect.com/science/article/abs/pii/S0030402622003588

Why it matters: surveys NLOS VLC channel modeling and performance issues. It highlights metrics such as bit-error rate (BER), signal-to-noise ratio (SNR), and channel impulse response. These should inform our experimental measurements.

## 2. Optical wireless communication progress and challenges

**“Optical Wireless Communication—Recent Progresses and Future Perspectives.”** *Journal of Lightwave Technology*. Manuscript accepted September 2025; published September 9, 2025.  
Publisher page: https://opg.optica.org/jlt/abstract.cfm?uri=jlt-44-3-806

Why it matters: covers VLC and longer-reach optical wireless systems, including atmospheric attenuation, beam divergence, pointing errors, and turbulence. These constraints are directly relevant to link-budget assumptions.

## 3. Ultraviolet NLOS scattering communication

**“Fundamentals, Key Technologies and Networking of Ultraviolet Non-Line-of-Sight Scattering Communication: A Review.”** *Photonics*, 2026.  
Publisher page: https://www.mdpi.com/2304-6732/13/6/558

Why it matters: reviews UV scattering channels, modulation/demodulation, coding, detectors, networking, and topology control. It is especially relevant to the scattering hypothesis, but UV hardware has different safety and component constraints from a visible LED prototype.

## 4. Free-space optical communication

**“A contemporary survey on free space optical communication: Potentials, technical challenges, recent advances and research direction.”** *Journal of Network and Computer Applications*, volume 200, April 2022, article 103311.  
Publisher page: https://www.sciencedirect.com/science/article/pii/S108480452100299X

Why it matters: surveys FSO link budgets, channel modeling, relay transmission, atmospheric impairments, and mitigation approaches. It helps establish a baseline against which any proposed relay design must be compared.

## Implications for Photon-Air-Hop

- Atmospheric optical communication, NLOS propagation, and optical relaying are established topics.
- Our potential contribution must be a precise engineering method or experimentally demonstrated system—not the general idea of photons travelling through air.
- Begin with a visible, low-power LED LOS data link. Investigate NLOS scattering only with a controlled setup and explicit blocked-path controls.
- Do not claim long range or emergency-grade reliability without repeatable measurements and comparison against established approaches.

## Next literature-review tasks

- Obtain and read the full texts where accessible.
- Follow their references for the closest NLOS optical link experiments and relay-network implementations.
- Search patent databases and standards separately; this document is not a patentability or freedom-to-operate opinion.
- Maintain a comparison table with mechanism, wavelength, transmitter, detector, geometry, distance, data rate, BER, power, and key limitation.
