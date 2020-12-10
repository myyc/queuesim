import arcade
import numpy as np
import sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
EP = 1.0
NQ = 4
EXP = 0.6
R = 20


class PQueue(arcade.Window):
    queues = [arcade.SpriteList() for i in range(NQ)]
    t = 0
    e = None
    n = 0

    exp_p = EP
    p_exp = EXP

    colours = [
        arcade.color.PURPLE_HEART,
        arcade.color.RED_PURPLE,
        arcade.color.PINK_LAVENDER,
        arcade.color.INDIGO,
        arcade.color.NEON_FUCHSIA,
        arcade.color.PURPLE_PIZZAZZ
    ]

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        for q in self.queues:
            q.draw()

        arcade.draw_text(f"λ = {self.exp_p:.1f}", 20, 0.04*SCREEN_HEIGHT,
                         arcade.color.BRIGHT_LAVENDER, 28)
        arcade.draw_text(f"α = {self.p_exp:.2f}", 20, -0.01*SCREEN_HEIGHT,
                         arcade.color.BRIGHT_LAVENDER, 28)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.exp_p += 0.2
        elif key == arcade.key.DOWN:
            self.exp_p -= 0.2
        elif key == arcade.key.LEFT:
            self.p_exp -= 0.05
        elif key == arcade.key.RIGHT:
            self.p_exp += 0.05
        elif key == arcade.key.Q or key == arcade.key.ESCAPE:
            sys.exit(0)

    def update(self, delta_time):
        if self.p_exp <= 0.0:
            self.p_exp = 0.05
        if self.exp_p <= 0.0:
            self.exp_p = 0.2

        if self.e is None:
            self.e = np.random.exponential(self.exp_p)

        if self.t >= self.e:
            self.t = 0
            self.e = np.random.exponential(self.exp_p)
            colour = self.colours[np.random.randint(0, len(self.colours))]
            c = arcade.SpriteCircle(R, colour)
            q = sorted([(i, len(q)) for i, q in enumerate(self.queues)],
                       key=lambda x: x[1])[0][0]
            c.center_y = SCREEN_HEIGHT*0.2 + q*(0.6*SCREEN_HEIGHT)/(NQ-1)
            c.num = self.n
            self.n += 1
            c.lifetime = np.random.pareto(self.p_exp) + sum(p.lifetime for p in self.queues[q])
            self.queues[q].append(c)
            
        for peeps in self.queues:
            kill_list = []
            for c in peeps:
                c.lifetime -= delta_time
                if c.lifetime <= 0:
                    kill_list.append(c)

            if len(kill_list) > 0:
                for s in kill_list:
                    peeps.remove(s)

            for i, c in enumerate(peeps):
                c.center_x = 3*R + i*(2*R + R/5)

        self.t += delta_time


game = PQueue(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
arcade.run()
