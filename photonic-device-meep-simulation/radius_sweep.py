import meep as mp
import numpy as np
import matplotlib.pyplot as plt


cell_x = 16
cell_y = 8
resolution = 20

waveguide_width = 1
waveguide_epsilon = 11.56

cavity_x = 1.6
cavity_y = 1.5

outer_epsilon = 14.44
inner_epsilon = 1.0

radii = [
    0.6,
    0.8,
    1.0,
    1.2,
    1.4
]

frequencies = np.linspace(
    0.10,
    0.20,
    100
)


def run_simulation(geometry):

    sources = [

        mp.Source(
            mp.GaussianSource(
                0.15,
                fwidth=0.10
            ),
            component=mp.Ez,
            center=mp.Vector3(-6, 0, 0),
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
        center=mp.Vector3(6, 0, 0),
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


reference_geometry = [

    mp.Block(
        center=mp.Vector3(0, 0, 0),
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

print("Running reference simulation...")

reference_flux = run_simulation(
    reference_geometry
)

print("Reference complete.")


results = []
spectra = []


for radius in radii:

    inner_radius = 0.65 * radius

    print(
        f"Running radius = {radius}"
    )

    geometry = [

        mp.Block(
            center=mp.Vector3(0, 0, 0),
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
            radius=radius,
            center=mp.Vector3(
                cavity_x,
                cavity_y,
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
                cavity_y,
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
        f"Frequency = {f_res:.4f}"
    )

    results.append(
        [
            radius,
            f_res,
            t_min
        ]
    )


results = np.array(
    results
)


np.savetxt(
    "radius_sweep.csv",
    results,
    delimiter=",",
    header=(
        "radius,"
        "resonance_frequency,"
        "minimum_transmission"
    ),
    comments=""
)


# Radius vs minimum transmission

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    results[:, 0],
    results[:, 2],
    marker="o"
)

plt.xlabel("Outer Cavity Radius")
plt.ylabel("Minimum Transmission")

plt.title(
    "Radius Sweep: Minimum Transmission"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "radius_sweep.png",
    dpi=200
)

plt.close()


# Radius vs resonance frequency

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    results[:, 0],
    results[:, 1],
    marker="o"
)

plt.xlabel("Outer Cavity Radius")
plt.ylabel("Resonance Frequency")

plt.title(
    "Radius Sweep: Resonance Frequency"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "radius_resonance.png",
    dpi=200
)

plt.close()


# Full transmission spectra

plt.figure(
    figsize=(8, 5)
)

for i, radius in enumerate(radii):

    plt.plot(
        frequencies,
        spectra[i],
        label=f"R = {radius:.1f}"
    )

plt.xlabel("Frequency")
plt.ylabel("Transmission")

plt.title(
    "Transmission Spectrum vs Cavity Radius"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    "radius_transmission_sweep.png",
    dpi=200
)

plt.close()


print()
print("RADIUS SWEEP COMPLETE")
print()
print("Saved:")
print("radius_sweep.png")
print("radius_resonance.png")
print("radius_transmission_sweep.png")
