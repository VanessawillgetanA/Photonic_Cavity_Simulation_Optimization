import meep as mp
import numpy as np
import matplotlib.pyplot as plt


# ========================================
# PARAMETERS
# ========================================

cell_x = 16
cell_y = 8
resolution = 20

waveguide_width = 1
waveguide_epsilon = 11.56

cavity_x = 1.6

outer_radius = 1.0
inner_radius = 0.65

outer_epsilon = 14.44
inner_epsilon = 1.0

positions = [
    1.1,
    1.3,
    1.5,
    1.7,
    1.9
]

frequencies = np.linspace(
    0.10,
    0.20,
    100
)


# ========================================
# SIMULATION FUNCTION
# ========================================

def run_simulation(geometry):

    sources = [
        mp.Source(
            mp.GaussianSource(
                0.15,
                fwidth=0.10
            ),
            component=mp.Ez,
            center=mp.Vector3(
                -6, 0, 0
            ),
            size=mp.Vector3(
                0,
                waveguide_width,
                0
            )
        )
    ]

    sim = mp.Simulation(
        cell_size=mp.Vector3(
            cell_x,
            cell_y,
            0
        ),
        geometry=geometry,
        sources=sources,
        resolution=resolution,
        boundary_layers=[
            mp.PML(1.0)
        ]
    )

    flux_region = mp.FluxRegion(
        center=mp.Vector3(
            6, 0, 0
        ),
        size=mp.Vector3(
            0,
            waveguide_width,
            0
        )
    )

    flux = sim.add_flux(
        0.15,
        0.10,
        100,
        flux_region
    )

    sim.run(
        until=200
    )

    return np.array(
        mp.get_fluxes(flux)
    )


# ========================================
# REFERENCE
# ========================================

reference_geometry = [
    mp.Block(
        center=mp.Vector3(
            0, 0, 0
        ),
        size=mp.Vector3(
            mp.inf,
            waveguide_width,
            mp.inf
        ),
        material=mp.Medium(
            epsilon=waveguide_epsilon
        )
    )
]

print("Running reference waveguide...")

reference_flux = run_simulation(
    reference_geometry
)

print("Reference complete.")


# ========================================
# POSITION SWEEP
# ========================================

results = []
spectra = []

for y in positions:

    print(
        f"Running cavity position y = {y}"
    )

    geometry = [

        mp.Block(
            center=mp.Vector3(
                0, 0, 0
            ),
            size=mp.Vector3(
                mp.inf,
                waveguide_width,
                mp.inf
            ),
            material=mp.Medium(
                epsilon=waveguide_epsilon
            )
        ),

        mp.Cylinder(
            radius=outer_radius,
            center=mp.Vector3(
                cavity_x,
                y,
                0
            ),
            material=mp.Medium(
                epsilon=outer_epsilon
            )
        ),

        mp.Cylinder(
            radius=inner_radius,
            center=mp.Vector3(
                cavity_x,
                y,
                0
            ),
            material=mp.Medium(
                epsilon=inner_epsilon
            )
        )
    ]

    cavity_flux = run_simulation(
        geometry
    )

    transmission = (
        cavity_flux /
        reference_flux
    )

    # Save complete spectrum
    spectra.append(
        transmission
    )

    index = np.argmin(
        transmission
    )

    f_res = frequencies[index]
    t_min = transmission[index]

    print(
        f"Minimum T = {t_min:.4f}"
    )

    print(
        f"Resonance frequency = {f_res:.4f}"
    )

    results.append(
        [
            y,
            f_res,
            t_min
        ]
    )


results = np.array(
    results
)


# ========================================
# SAVE DATA
# ========================================

np.savetxt(
    "position_sweep.csv",
    results,
    delimiter=",",
    header=(
        "y_position,"
        "resonance_frequency,"
        "minimum_transmission"
    ),
    comments=""
)


# ========================================
# GRAPH 1
# POSITION VS MINIMUM TRANSMISSION
# ========================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    results[:, 0],
    results[:, 2],
    marker="o"
)

plt.xlabel(
    "Cavity y-position"
)

plt.ylabel(
    "Minimum Transmission"
)

plt.title(
    "Cavity Position vs Minimum Transmission"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "coupling_sensitivity.png",
    dpi=200
)

plt.close()


# ========================================
# GRAPH 2
# POSITION VS RESONANCE FREQUENCY
# ========================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    results[:, 0],
    results[:, 1],
    marker="o"
)

plt.xlabel(
    "Cavity y-position"
)

plt.ylabel(
    "Resonance Frequency"
)

plt.title(
    "Cavity Position vs Resonance Frequency"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "position_resonance.png",
    dpi=200
)

plt.close()


# ========================================
# GRAPH 3
# FULL TRANSMISSION SPECTRA
# ========================================

plt.figure(
    figsize=(8, 5)
)

for i, y in enumerate(positions):

    plt.plot(
        frequencies,
        spectra[i],
        label=f"y = {y:.1f}"
    )

plt.xlabel(
    "Frequency"
)

plt.ylabel(
    "Transmission"
)

plt.title(
    "Transmission Spectrum vs Cavity Position"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    "position_transmission_sweep.png",
    dpi=200
)

plt.close()


print()
print("POSITION SWEEP COMPLETE")
print()
print("Generated:")
print("  position_sweep.csv")
print("  coupling_sensitivity.png")
print("  position_resonance.png")
print("  position_transmission_sweep.png")
