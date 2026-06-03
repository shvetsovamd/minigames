import tkinter as tk
import random

def create_snake():
    max_x, max_y = (W // CELL_SIZE) - 3, (H // CELL_SIZE) - 1

    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE

    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]


def create_food():
    while True:
        x = random.randint(0, (W - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (H - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)


def draw_food():
    canvas.create_rectangle(
        food[0], food[1],
        food[0] + CELL_SIZE, food[1] + CELL_SIZE,
        fill="red"
    )


def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE,
            segment[1] + CELL_SIZE,
            fill="green",
            outline="darkgreen"
        )


def move_snake():
    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0, new_head)

    if not check_food_collision():
        snake.pop()


def check_food_collision():
    global food, score
    if snake[0] == food:
        score += 1
        food = create_food()
        return True
    return False


def check_wall_collision():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= W or head_y < 0 or head_y >= H
    )


def check_self_collision():
    return snake[0] in snake[1:]


def end_game():
    global game_over
    game_over = True
    canvas.create_text(
        W // 2, H // 2,
        text=f"Game over! Score: {score}",
        fill="white",
        font=("Arial", 24)
    )


def update_title():
    root.title(f"Snake | Score: {score}")


def restart_game():
    global snake, direction, food, score, game_over

    snake, direction, food = create_snake(), "Right", create_food()
    score, game_over = 0, False

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)


def on_key_press(event):
    global direction, game_over

    key = event.keysym

    if key in DIRS and not game_over:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
    elif key == "space" and game_over:
        restart_game()


def game_loop():
    global snake, food, score

    if game_over:
        return

    move_snake()

    if check_wall_collision() or check_self_collision():
        end_game()
        return

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)


W, H, CELL_SIZE, DELAY, DIRS = 400, 400, 10, 100, ["Up", "Down", "Left", "Right"]

root = tk.Tk()
root.title("Snake | Score: 0")
root.resizable(False, False)

canvas = tk.Canvas(
    root, width=W, height=H,
    bg="black", highlightthickness=0
)
canvas.pack()

snake, direction, score, game_over = create_snake(), "Right", 0, False
food = create_food()

root.bind("<KeyPress>", on_key_press)
draw_food()
draw_snake()
root.after(DELAY, game_loop)
root.mainloop()
