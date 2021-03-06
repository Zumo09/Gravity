# Gravity Simulator

Physics simulation, with 3D rendering, using pygame and numpy.

## Requirements

```
pip install numpy pygame
```

## Run the program

```
cd src

python gravity.py
```

## Installation

```
pip install pyinstaller

cd src

pyinstaller --clean --windowed --onefile --name Gravity --icon saturn.ico gravity.py
```

Executable can be found in `src/dist/gravity.exe`

# Controls

## Main
* **SPACE BAR**: toggle time

* **R**: reset camera position

* **T**: toggle automatic camera movement

* **ESC**: quit the application

## Camera Movement
### Traslation

* **W, S**: Up, Down

* **A, D**: Left, Right

* **Q, E**: Back, Forward

### Rotation

* **J, L**: X-axis rotation

* **I, K**: Y-axis rotation

* **U, O**: Z-axis rotation

