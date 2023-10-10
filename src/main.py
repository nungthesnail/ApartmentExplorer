from multiprocessing import Process
from analyzer import analyzer
from bot import bot


if __name__ == "__main__":
    process_analyzer = Process(target=analyzer.main, daemon=True)
    process_bot = Process(target=bot.run, daemon=True)

    process_analyzer.start()
    process_bot.start()

    process_analyzer.join()
    process_bot.join()
