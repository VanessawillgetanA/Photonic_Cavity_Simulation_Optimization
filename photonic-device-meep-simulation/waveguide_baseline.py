import meep as mp

cell_x = 16
cell_y = 8
resolution = 20

waveguide_width = 1
waveguide_epsilon = 11.56

geometry = [
    mp.Block(
        center=mp.Vector3(0, 0, 0),
        size=mp.Vector3(mp.inf, waveguide_width, mp.inf),
        material=mp.Medium(epsilon=waveguide_epsilon)
    )
]

sources = [
    mp.Source(
        mp.ContinuousSource(frequency=0.15),
        component=mp.Ez,
        center=mp.Vector3(-6, 0, 0),
        size=mp.Vector3(0, waveguide_width, 0)
    )
]

sim = mp.Simulation(
    cell_size=mp.Vector3(cell_x, cell_y, 0),
    geometry=geometry,
    sources=sources,
    resolution=resolution,
    boundary_layers=[
        mp.PML(1.0)
    ]
)

sim.run(
    mp.at_beginning(
        mp.output_png(
            mp.Ez,
            "-S3",
            "-Zc"
        )
    ),
    until=100
)
