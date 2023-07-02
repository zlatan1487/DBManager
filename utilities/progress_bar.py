from tqdm import tqdm
import time


def progress_bar(total_iterations, message):
    """
    Отображает прогресс выполнения итераций с помощью полосы прогресса.

    Аргументы:
    - total_iterations (int): Общее количество итераций.
    - message (str): Сообщение, отображаемое перед полосой прогресса.
    """
    with tqdm(total=total_iterations, desc=message) as pbar:
        for _ in range(total_iterations):
            time.sleep(0.5)
            pbar.update(1)
