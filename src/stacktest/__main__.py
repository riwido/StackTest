import pathlib

static = pathlib.Path(__file__).parent / "static"

for file in static.iterdir():
    print(f"Static file: {file}")
