from body import GravitationalBody
from simulator import GravitySimulator, shades


def main():
    VIOLET = (10, 0, 20)
    WHITE = (255, 255, 255)
    CYAN = (0, 210, 255)
    PINK = (240, 5, 220)
    PURPLE = (100, 0, 125)
    purple_shades = shades(PINK, PURPLE, 6)

    sim = GravitySimulator(
        num_star=400,
        background_color=VIOLET,
        star_color=WHITE,
        camera_init_pos=(500, 500, 7500),
        camera_init_rot=(0.5, 0.5, 0),
        screen_dim=None,
        start_time=False,
        start_movement=True
    )
    sim.add_bodies(
        [
            GravitationalBody(
                10,
                40,
                (0, 1000, 0),
                (70, 0, 5),
                color=purple_shades[0],
                trajectory_len=70,
            ),
            GravitationalBody(
                20,
                60,
                (0, 2000, 0),
                (50, 0, 0),
                color=purple_shades[1],
                trajectory_len=220,
            ),
            GravitationalBody(
                30,
                50,
                (0, 3000, 0),
                (40, 0, -5),
                color=purple_shades[2],
                trajectory_len=400,
            ),
            GravitationalBody(
                50,
                70,
                (0, 4000, 0),
                (35, 0, 0),
                color=purple_shades[3],
                trajectory_len=620,
            ),
            GravitationalBody(
                70,
                85,
                (0, 5000, 0),
                (31, 0, 2),
                color=purple_shades[4],
                trajectory_len=870,
            ),
            GravitationalBody(
                100,
                100,
                (0, 6000, 0),
                (27, 0, -10),
                color=purple_shades[5],
                trajectory_len=1200,
            ),
            GravitationalBody(1e6, 120, (0, 0, 0), (0, 0, 0), color=CYAN),
        ]
    )

    sim.main_loop()


if __name__ == "__main__":
    main()
