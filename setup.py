import cx_Freeze as freeze

executables = [freeze.Executable("main.py")]
freeze.setup(
    name = "Boids",
    options = {"build_exe": { "packages":["pygame","numpy"],
                              "include_files":["blue_arrow.png"]}},
    executables = executables
)