import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------
# Parameters
# --------------------------------

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


# --------------------------------
# Function to run field simulation
# --------------------------------

def run_field_simulation(geometry):

    sources = [
        mp.Source(
            mp.ContinuousSource(
                frequency=source_frequency
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

    # Let the electromagnetic wave propagate
    sim.run(
        until=100
    )

    # Extract Ez AFTER the simulation
    ez = sim.get_array(
        center=mp.Vector3(0, 0, 0),
        size=mp.Vector3(
            cell_x,
            cell_y,
            0
        ),
        component=mp.Ez
    )

    return ez


# ========================================
# BASELINE WAVEGUIDE
# ========================================

print()
print("================================")
print("BASELINE FIELD")
print("================================")

baseline_geometry = [
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

baseline_ez = run_field_simulation(
    baseline_geometry
)

print("Baseline simulation complete.")


plt.figure(
    figsize=(12, 6)
)

plt.imshow(
    np.transpose(baseline_ez),
    origin="lower",
    extent=[
        -cell_x / 2,
        cell_x / 2,
        -cell_y / 2,
        cell_y / 2
    ],
    aspect="equal",
    cmap="RdBu",
    interpolation="bilinear"
)

plt.colorbar(
    label="Ez"
)

plt.xlabel("x")
plt.ylabel("y")

plt.title(
    "Electric Field Ez: Baseline Waveguide"
)

plt.tight_layout()

plt.savefig(
    "baseline_field.png",
    dpi=200
)

plt.close()


# ========================================
# CAVITY
# ========================================

print()
print("================================")
print("CAVITY FIELD")
print("================================")

cavity_geometry = [

    # Waveguide
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

    # Outer cavity
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

    # Inner air region
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

cavity_ez = run_field_simulation(
    cavity_geometry
)

print("Cavity simulation complete.")


plt.figure(
    figsize=(12, 6)
)

plt.imshow(
    np.transpose(cavity_ez),
    origin="lower",
    extent=[
        -cell_x / 2,
        cell_x / 2,
        -cell_y / 2,
        cell_y / 2
    ],
    aspect="equal",
    cmap="RdBu",
    interpolation="bilinear"
)

plt.colorbar(
    label="Ez"
)

plt.xlabel("x")
plt.ylabel("y")

plt.title(
    "Electric Field Ez: Photonic Cavity"
)

plt.tight_layout()

plt.savefig(
    "cavity_field.png",
    dpi=200
)

plt.close()


print()
print("================================")
print("FIELD PICTURES COMPLETE")
print("================================")
print()
print("Created:")
print("  baseline_field.png")
print("  cavity_field.png")
