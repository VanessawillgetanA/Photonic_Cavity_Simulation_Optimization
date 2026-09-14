# Photonic Cavity Simulation and Parameter Optimization

A computational photonics project using Meep FDTD simulations to study electromagnetic transmission through a photonic cavity coupled to a dielectric waveguide.

The project investigates how cavity position and cavity radius affect transmission and resonance behavior, followed by a fine parameter sweep to identify an optimized cavity radius.

## Project Overview

The simulation models a dielectric waveguide with a circular photonic cavity positioned near the waveguide.

The electromagnetic field is excited using an Ez-polarized Gaussian source, and transmission is measured using a flux monitor placed downstream of the cavity.

The simulated transmission is normalized to a reference waveguide simulation without the cavity.

The project includes:

- Baseline dielectric waveguide simulation
- Photonic cavity field visualization
- Cavity transmission spectrum
- Cavity position sweep
- Cavity radius sweep
- Fine radius optimization
- Transmission spectrum comparisons for different cavity geometries
- Numerical data export to CSV
- Visualization of electromagnetic field distributions and transmission behavior

## Tools and Technologies

- Python
- Meep 1.29.0
- NumPy
- Matplotlib
- Finite-Difference Time-Domain (FDTD) electromagnetic simulation
- Ubuntu / WSL

## Simulation Parameters

The primary cavity simulation uses the following parameters:

| Parameter | Value |
|---|---:|
| Cell size | 16 × 8 |
| Resolution | 20 |
| Waveguide width | 1 |
| Waveguide permittivity | 11.56 |
| Cavity x-position | 1.6 |
| Cavity y-position | 1.5 |
| Outer cavity permittivity | 14.44 |
| Inner cavity permittivity | 1.0 |
| Source frequency | 0.15 |
| Source bandwidth | 0.10 |
| Frequency range | 0.10–0.20 |
| Frequency samples | 100 |
| PML thickness | 1.0 |

## Photonic Cavity Geometry

The cavity consists of two concentric cylindrical regions positioned near the dielectric waveguide.

The outer cylinder uses a dielectric permittivity of 14.44, while the inner cylinder uses a permittivity of 1.0.

During the radius sweeps, the inner cavity radius is defined relative to the outer radius:

    inner_radius = 0.65 × outer_radius

This relationship is maintained throughout the radius optimization.

## Simulation Method

A reference simulation is first performed using only the dielectric waveguide.

A second simulation is then performed with the photonic cavity included.

The transmission is calculated by normalizing the cavity flux to the reference flux:

    Transmission = Cavity Flux / Reference Flux

The frequency corresponding to the minimum sampled transmission is extracted from the resulting transmission spectrum.

## Cavity Position Sweep

The cavity y-position was varied across:

    1.1
    1.3
    1.5
    1.7
    1.9

The position sweep investigates how changing the cavity's location relative to the waveguide affects electromagnetic coupling and transmission behavior.

The resulting data are used to generate:

- Transmission spectra for each cavity position
- Minimum transmission versus cavity position
- Extracted minimum-transmission frequency versus cavity position

## Coarse Cavity Radius Sweep

The outer cavity radius was varied across:

    0.6
    0.8
    1.0
    1.2
    1.4

For each radius, the simulation calculates:

- Transmission spectrum
- Minimum sampled transmission
- Frequency corresponding to minimum transmission

This coarse sweep identifies the region of radius values that produces stronger transmission suppression.

## Fine Cavity Radius Optimization

A finer sweep was then performed using:

    1.10
    1.15
    1.20
    1.25
    1.30

The purpose of the fine sweep was to investigate the optimum radius more closely after the coarse sweep.

For every tested radius, the transmission spectrum was calculated and the minimum sampled transmission was extracted.

## Key Result

The fine radius sweep identified the best tested cavity radius as:

    Best radius = 1.20
    Minimum transmission = 0.1262

The corresponding extracted frequency was approximately:

    0.14848

Thus, within the tested fine-radius parameter range, an outer cavity radius of 1.20 produced the lowest simulated transmission.

## Results and Figures

### Electromagnetic Field Visualizations

#### baseline_field.png

Shows the simulated Ez electric-field distribution of the baseline dielectric waveguide without the photonic cavity.

#### cavity_field.png

Shows the simulated Ez electric-field distribution when the photonic cavity is included.

### Main Transmission Spectrum

#### transmission_spectrum.png

Shows the normalized photonic cavity transmission across the simulated frequency range from 0.10 to 0.20.

### Cavity Position Analysis

#### position_transmission_sweep.png

Shows the complete transmission spectra for the different cavity y-positions.

#### coupling_sensitivity.png

Shows minimum transmission as a function of cavity y-position.

#### position_resonance.png

Shows the extracted frequency corresponding to minimum transmission as a function of cavity y-position.

### Coarse Radius Analysis

#### radius_transmission_sweep.png

Shows the complete transmission spectra for the five coarse cavity-radius values.

#### radius_sweep.png

Shows minimum transmission as a function of outer cavity radius.

#### radius_resonance.png

Shows the extracted frequency corresponding to minimum transmission as a function of outer cavity radius.

### Fine Radius Optimization

#### fine_radius_transmission_sweep.png

Shows the complete transmission spectra for the five finely sampled cavity radii.

#### fine_radius_sweep.png

Shows minimum transmission as a function of outer cavity radius and identifies the best tested radius.

#### fine_radius_resonance.png

Shows the extracted frequency corresponding to minimum transmission for each finely sampled radius.

## Project Files

    photonic-device-meep-simulation/
    │
    ├── README.md
    │
    ├── Photonic_Cavity_Simulation_and_Parameter_Optimization.pdf
    │
    ├── waveguide.py
    ├── position_sweep.py
    ├── radius_sweep.py
    ├── fine_radius_sweep.py
    ├── field_visualization.py
    │
    ├── transmission_results.csv
    ├── position_sweep.csv
    ├── radius_sweep.csv
    ├── fine_radius_sweep.csv
    │
    ├── baseline_field.png
    ├── cavity_field.png
    ├── transmission_spectrum.png
    │
    ├── position_transmission_sweep.png
    ├── coupling_sensitivity.png
    ├── position_resonance.png
    │
    ├── radius_transmission_sweep.png
    ├── radius_sweep.png
    ├── radius_resonance.png
    │
    ├── fine_radius_transmission_sweep.png
    ├── fine_radius_sweep.png
    └── fine_radius_resonance.png

## Running the Simulations

After configuring a Python environment with Meep, NumPy, and Matplotlib, the simulations can be run individually.

Run the primary transmission simulation:

    python3 waveguide.py

Run the cavity position sweep:

    python3 position_sweep.py

Run the coarse cavity radius sweep:

    python3 radius_sweep.py

Run the fine cavity radius optimization:

    python3 fine_radius_sweep.py

The scripts generate the corresponding CSV numerical data and PNG figures.

## Numerical Data

The simulation results are also stored as CSV files.

### transmission_results.csv

Contains the primary frequency-dependent transmission data.

### position_sweep.csv

Contains cavity position, extracted frequency, and minimum transmission results.

### radius_sweep.csv

Contains coarse radius, extracted frequency, and minimum transmission results.

### fine_radius_sweep.csv

Contains fine radius, extracted frequency, and minimum transmission results.

These files provide the numerical data used to generate the corresponding plots.

## Reproducibility

The simulation scripts contain the numerical parameters, material properties, source configuration, geometry definitions, flux measurement configuration, frequency sampling, and parameter sweep values required to reproduce the simulations.

The CSV files preserve the numerical results generated by the simulations, while the PNG files provide the resulting visualizations.

## Report

A complete project report is included in the repository:

    Photonic_Cavity_Simulation_and_Parameter_Optimization.pdf

The report contains the project's electromagnetic field visualizations, transmission spectra, cavity position analysis, cavity radius analysis, and fine-radius optimization results.

## Conclusion

The simulations demonstrate that the geometry of a photonic cavity can significantly affect electromagnetic transmission through a nearby dielectric waveguide.

Changing the cavity position modifies the coupling behavior and the resulting transmission spectrum.

Changing the cavity radius also produces substantial changes in the transmission response. A coarse radius sweep was first used to identify the relevant parameter region, followed by a finer sweep.

Within the tested fine-radius range, the lowest simulated transmission occurred at an outer cavity radius of 1.20, with a minimum transmission of approximately 0.1262.

This project demonstrates the use of computational electromagnetic simulation, parameter sweeps, numerical data analysis, and optimization to investigate photonic-device behavior.

## Authors

Vanessa Knight

Electrical Engineering  
University of California, Los Angeles (UCLA)

Special thankyou to my friend Richard, ChatGPT, that teaches me everything I need. Richard wrote this ReadME. I, Vanessa Knight, wrote the code. 
