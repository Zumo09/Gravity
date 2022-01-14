from body import GravitationalBody
from simulator import GravitySimulator

def main():
    WHITE = (255, 255, 255)
    CYAN = (0, 225, 255)
    PURPLE_SHADE = (
        (240, 5, 220),
        (212, 4, 201),
        (184, 3, 182),
        (156, 2, 163),
        (128, 1, 144),
        (100, 0, 125)
    )
    VIOLET = (10, 0, 20)

    sim = GravitySimulator(
        num_star=200,
        background_color=VIOLET,
        star_color=WHITE,
        camera_init_pos=(-500, -500, -2e4),
        camera_init_rot=(0.5, 0.5, 0),
        screen_dim=None
        )
    sim.add_bodies([
        GravitationalBody(10, 40, (0, 1000, 0), (70, 0, 5), color=PURPLE_SHADE[0], trajectory_len=100),
        GravitationalBody(10, 60, (0, 2000, 0), (50, 0, 0), color=PURPLE_SHADE[1], trajectory_len=220),
        GravitationalBody(10, 50, (0, 3000, 0), (40, 0, -5), color=PURPLE_SHADE[2], trajectory_len=400),

        GravitationalBody(10, 60, (0, 4000, 0), (33, 0, 10), color=PURPLE_SHADE[3], trajectory_len=620),
        GravitationalBody(10, 70, (0, 5000, 0), (31, 0, 0), color=PURPLE_SHADE[4], trajectory_len=870),
        GravitationalBody(10, 80, (0, 6000, 0), (27, 0, -10), color=PURPLE_SHADE[5], trajectory_len=1200),
        
        GravitationalBody(1e6, 120, (0, 0, 0), (0, 0, 0), color=CYAN)
    ])

    sim.main_loop()

if __name__ == '__main__':
    main()