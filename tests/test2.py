import threading

from sockchat.network.client import Client
from sockchat.network.server import Server
from sockchat.ui_provider import MockUiProvider


# Тестирование общения Алисы и Боба, симулируемое с помощью класса MockUiProvider
def main():
    alice_messages = ["Hello", 1, "Word2", 1]
    bob_messages = [0.5, "Hi", 1, "Word3", 1]

    alice = threading.Thread(target=lambda: Client("alice", "localhost", MockUiProvider(alice_messages)).run())
    bob = threading.Thread(target=lambda: Client("bob", "localhost", MockUiProvider(bob_messages)).run())
    server = threading.Thread(target=lambda: Server().run())

    server.start()
    alice.start()
    bob.start()

    alice.join()
    bob.join()
    server.join()


if __name__ == "__main__":
    main()
