import tkinter as tk
import random

class BlockBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title('블럭깨기 게임')
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.is_paused = False
        self.is_game_over = False

        self.paddle_width = 240
        self.paddle_height = 15
        self.paddle_speed = 40
        self.paddle = self.canvas.create_rectangle(0, 0, self.paddle_width, self.paddle_height, fill='white')
        self.reset_paddle()

        self.ball_radius = 10
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius*2, self.ball_radius*2, fill='yellow')
        self.ball_dx = 6
        self.ball_dy = -6
        self.reset_ball()

        self.brick_rows = 6
        self.brick_cols = 10
        self.brick_width = 70
        self.brick_height = 22
        self.bricks = []
        self.create_bricks()

        self.text_score = self.canvas.create_text(10, 10, anchor='nw', fill='white', font=('Arial', 16), text='점수: 0')
        self.text_lives = self.canvas.create_text(self.width-10, 10, anchor='ne', fill='white', font=('Arial', 16), text='목숨: 3')
        self.message_id = None

        self.root.bind('<Left>', self.on_left)
        self.root.bind('<Right>', self.on_right)
        self.root.bind('<a>', self.on_left)
        self.root.bind('<d>', self.on_right)
        self.root.bind('<Escape>', self.on_escape)
        self.root.bind('<space>', self.on_space)

        self.running = True
        self.game_loop()

    def reset_paddle(self):
        x = (self.width - self.paddle_width) / 2
        y = self.height - self.paddle_height - 8
        self.canvas.coords(self.paddle, x, y, x + self.paddle_width, y + self.paddle_height)

    def reset_ball(self):
        self.ball_dx = random.choice([-6, 6])
        self.ball_dy = -6
        paddle_coords = self.canvas.coords(self.paddle)
        x_center = (paddle_coords[0] + paddle_coords[2]) / 2
        y = paddle_coords[1] - 2 * self.ball_radius - 1
        self.canvas.coords(self.ball, x_center - self.ball_radius, y, x_center + self.ball_radius, y + self.ball_radius * 2)

    def create_bricks(self):
        padding_x = 35
        padding_y = 45
        gap = 6
        colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251']
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                x1 = padding_x + col * (self.brick_width + gap)
                y1 = padding_y + row * (self.brick_height + gap)
                x2 = x1 + self.brick_width
                y2 = y1 + self.brick_height
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)], outline='white')
                self.bricks.append(brick)

    def on_left(self, event=None):
        if not self.is_game_over:
            dx = -self.paddle_speed
            self.move_paddle(dx)

    def on_right(self, event=None):
        if not self.is_game_over:
            dx = self.paddle_speed
            self.move_paddle(dx)

    def on_escape(self, event=None):
        self.running = False
        self.root.destroy()

    def on_space(self, event=None):
        if self.is_game_over:
            self.restart_game()
        else:
            self.is_paused = not self.is_paused
            self.show_message('paused' if self.is_paused else '')

    def move_paddle(self, dx):
        if self.is_paused or self.is_game_over:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        new_x1 = max(0, x1 + dx)
        new_x2 = min(self.width, x2 + dx)
        if new_x2 - new_x1 < self.paddle_width:
            if new_x1 <= 0:
                new_x1, new_x2 = 0, self.paddle_width
            else:
                new_x1, new_x2 = self.width - self.paddle_width, self.width
        self.canvas.coords(self.paddle, new_x1, y1, new_x2, y2)

    def update_score(self):
        self.canvas.itemconfigure(self.text_score, text=f'점수: {self.score}')
        self.canvas.itemconfigure(self.text_lives, text=f'목숨: {self.lives}')

    def show_message(self, message):
        if self.message_id:
            self.canvas.delete(self.message_id)
            self.message_id = None
        if message:
            self.message_id = self.canvas.create_text(self.width / 2, self.height / 2, text=message, fill='white', font=('Arial', 26, 'bold'))

    def game_loop(self):
        if not self.running:
            return
        if not self.is_paused and not self.is_game_over:
            self.move_ball()

        self.root.after(16, self.game_loop)

    def move_ball(self):
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        if x1 <= 0 or x2 >= self.width:
            self.ball_dx = -self.ball_dx

        if y1 <= 0:
            self.ball_dy = abs(self.ball_dy)

        if y2 >= self.height:
            self.lives -= 1
            self.update_score()
            if self.lives <= 0:
                self.gameover(False)
                return
            self.reset_ball()
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        ball_coords = self.canvas.coords(self.ball)
        overlap = self.canvas.find_overlapping(*ball_coords)
        if self.paddle in overlap:
            self.ball_dy = -abs(self.ball_dy)
            paddle_coords = self.canvas.coords(self.paddle)
            paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
            ball_center = (ball_coords[0] + ball_coords[2]) / 2
            offset = (ball_center - paddle_center) / (self.paddle_width / 2)
            self.ball_dx = 8 * offset

        hit_brick = None
        for brick in self.bricks:
            if brick in overlap:
                hit_brick = brick
                break

        if hit_brick:
            self.canvas.delete(hit_brick)
            self.bricks.remove(hit_brick)
            self.score += 10
            self.update_score()
            self.ball_dy = -self.ball_dy
            if not self.bricks:
                self.gameover(True)
            return

    def gameover(self, is_win):
        self.is_game_over = True
        msg = '게임 승리! 스페이스로 재시작' if is_win else '게임 오버! 스페이스로 재시작'
        self.show_message(msg)

    def restart_game(self):
        self.canvas.delete('all')
        self.score = 0
        self.lives = 30
        self.is_paused = False
        self.is_game_over = False

        self.paddle = self.canvas.create_rectangle(0, 0, self.paddle_width, self.paddle_height, fill='white')
        self.reset_paddle()
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius*2, self.ball_radius*2, fill='yellow')
        self.reset_ball()
        self.bricks = []
        self.create_bricks()
        self.text_score = self.canvas.create_text(10, 10, anchor='nw', fill='white', font=('Arial', 16), text='점수: 0')
        self.text_lives = self.canvas.create_text(self.width-10, 10, anchor='ne', fill='white', font=('Arial', 16), text='목숨: 3')
        self.message_id = None


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    game = BlockBreaker(root)
    root.mainloop()
