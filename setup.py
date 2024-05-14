import cx_Freeze as freeze # import cx freeze

executables = [freeze.Executable("main.py")] # executable files
freeze.setup(
    name = "Boids",
    options = {"build_exe": { "packages":["pygame","numpy"],
                              "include_files":["blue_arrow.png"]}},
    executables = executables
) # setup exe build