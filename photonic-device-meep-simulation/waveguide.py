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

outer_radius = 1.0
inner_radius = 0.65

outer_epsilon = 14.44
inner_epsilon = 1.0

source_frequency = 0.15
source_width = 0.10

frequencies = np.linspace(0.10, 0.20, 100)


def make_geometry():

    return [

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
            radius=outer_radius,
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


def run_simulation(geometry):

    sources = [

        mp.Source(
            mp.GaussianSource(
                source_frequency,
                fwidth=source_width
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
        source_frequency,
        source_width,
        100,
        flux_region
    )

    sim.run(
        until=200
    )

    return np.array(
        mp.get_fluxes(flux)
    )


print("Running reference simulation...")

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

reference_flux = run_simulation(
    reference_geometry
)

print("Reference simulation complete.")

print("Running cavity simulation...")

cavity_flux = run_simulation(
    make_geometry()
)

print("Cavity simulation complete.")

transmission = (
    cavity_flux /
    reference_flux
)

minimum_index = np.argmin(
    transmission
)

minimum_transmission = (
    transmission[minimum_index]
)

resonance_frequency = (
    frequencies[minimum_index]
)

print()
print("==============================")
print("TRANSMISSION RESULTS")
print("==============================")
print(
    f"Minimum transmission: "
    f"{minimum_transmission:.4f}"
)
print(
    f"Frequency: "
    f"{resonance_frequency:.5f}"
)

np.savetxt(
    "transmission_results.csv",
    np.column_stack(
        (
            frequencies,
            transmission
        )
    ),
    delimiter=",",
    header="frequency,transmission",
    comments=""
)

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    frequencies,
    transmission
)

plt.xlabel("Frequency")
plt.ylabel("Transmission")

plt.title(
    "Photonic Cavity Transmission Spectrum"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "transmission_spectrum.png",
    dpi=200
)

plt.close()

print("Saved transmission_spectrum.png")
