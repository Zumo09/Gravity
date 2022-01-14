from body import GravitationalBody
from simulator import GravitySimulator

def main():
    CYAN = (0, 225, 255)
    PURPLE_LIGHT = (238, 5, 218)
    PURPLE = (215, 0, 255)
    PURPLE_DARK = (100, 0, 125)
    VIOLET = (10, 0, 20)

    sim = GravitySimulator(background_color=VIOLET)
    sim.add_bodies([
        GravitationalBody(10, 30, (0, 1000, 0), (70, 0, 30), color=PURPLE_LIGHT, trajectory_len=100),
        GravitationalBody(10, 60, (0, 2000, 0), (50, 0, 0), color=PURPLE, trajectory_len=220),
        GravitationalBody(10, 50, (0, 3000, 0), (0, 0, 30), color=PURPLE_DARK, trajectory_len=230),
        GravitationalBody(1e6, 100, (0, 0, 0), (0, 0, 0), color=CYAN)
    ])

    sim.main_loop()

if __name__ == '__main__':
    main()