import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, stop_event):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            # Філософ думає
            self.think()
            # Філософ голодний і хоче поїсти
            self.eat()

    def think(self):
        print(f"{self.name} розмірковує про сутність буття...")
        time.sleep(random.uniform(1, 5))

    def eat(self):
        print(f"{self.name} починає їсти")
        # Філософ спробує спочатку взяти ліву вилку
        self.left_fork.acquire()
        print(f"{self.name} взяв ліву вилку")
        # Якщо філософ не зміг взяти праву вилку, він поверне ліву і почне думати знову
        if not self.right_fork.acquire(blocking=False):
            print(f"{self.name} не може взяти праву вилку зараз")
            self.left_fork.release()
            return
        print(f"{self.name} взяв праву вилку, тепер він їсть")
        time.sleep(random.uniform(1, 5))
        self.right_fork.release()
        print(f"{self.name} повернув праву вилку")
        self.left_fork.release()
        print(f"{self.name} повернув ліву вилку і закінчив їсти")

def main():
    # Створюємо виделки
    forks = [threading.Lock() for i in range(5)]

    # Створюємо філософів та запускаємо їх у вічний цикл
    stop_event = threading.Event()
    philosophers = []
    for i in range(5):
        philosopher = Philosopher(f"Філософ {i+1}", forks[i], forks[(i+1) % 5], stop_event)
        philosophers.append(philosopher)
        philosopher.start()

    # Чекаємо поки користувач натисне Enter
    input("Натисніть Enter, щоб завершити програму\n")
    stop_event.set()

    # Чекаємо поки всі філософи закінчать їсти
    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()
