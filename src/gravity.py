from body import GravitationalBody
from simulator import GravitySimulator

def main():
    BLACK = (0, 0, 0)
    NAVY_BLUE = (0, 0, 10)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    DANDILION_YELLOW = (255,200,0)

    sim = GravitySimulator(NAVY_BLUE, WHITE)
    sim.add_bodies([
        GravitationalBody(10, 30, (0, 1000, 0), (70, 0, 30), color=RED, trajectory_len=100),
        GravitationalBody(10, 60, (0, 2000, 0), (50, 0, 0), color=GREEN, trajectory_len=220),
        GravitationalBody(10, 50, (0, 3000, 0), (0, 0, 30), color=BLUE, trajectory_len=230),
        GravitationalBody(1e6, 100, (0, 0, 0), (0, 0, 0), color=DANDILION_YELLOW)
    ])

    sim.main_loop()

if __name__ == '__main__':
    main()