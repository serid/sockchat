import socket
import time
from dataclasses import dataclass
from threading import Thread, Lock

from sockchat import common, loggers
from sockchat.network.message import DisconnectMessage, decode_message, encode_message, LoginMessage, TextMessage, Message, \
    AckMessage
from sockchat.network.message_channel import MessageChannel
from sockchat.util import apply_if_some

Users = dict[str, MessageChannel]


@dataclass(init=False, eq=False, match_args=False, slots=True)
class Server:
    # Сопоставление имени пользователя с каналом
    users: Users
    # Защита словаря [users]
    users_lock: Lock

    def __init__(self):
        self.users = {}
        self.users_lock = Lock()

    def client_handler(self, client_username: str, chan: MessageChannel):
        while True:
            data = chan.receive()

            # Декодирование сообщения если оно не None
            message: Message | None = apply_if_some(decode_message, data)
            if message is None or isinstance(message, DisconnectMessage):
                chan.send(encode_message(DisconnectMessage()))
                chan.close()
                self.server_print(f"closed channel for {client_username}")
                break

            match message:
                case TextMessage(username=username, text=text, id=id_):
                    # Имя клиента в сообщении должно совпадать с именем которое использовалось при создании канала
                    assert username == client_username

                    self.server_print(f"{client_username} says: {text}")

                    message_to_broadcast = TextMessage(client_username, text, id_)

                    # Переслать сообщение всем другим пользователям
                    with self.users_lock:
                        for (i_username, i_channel) in self.users.items():
                            # Пропускаем автора сообщения
                            if i_username == client_username:
                                continue
                            i_channel.send(encode_message(message_to_broadcast))
                case AckMessage(text_by_username=text_by_username,
                                acknowledged_by_username=acknowledged_by_username, id=id_):
                    # Переслать подтверждение автору изначального сообщения
                    with self.users_lock:
                        self.users[text_by_username].send(data)
                case _:
                    raise Exception()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", common.TCP_PORT))
        server_socket.listen(2)

        while True:
            (client_socket, address) = server_socket.accept()

            # Создание канала
            chan = MessageChannel(client_socket)

            # Получение имени пользователя
            login_message = chan.receive()

            username: str
            match decode_message(login_message):
                case LoginMessage(name=name2):
                    username = name2
                case _:
                    raise Exception()
            self.server_print(f"{username}: logs in with {login_message}")

            if username is None:
                self.server_print(f"{username}: login failed")
                continue

            # Сопоставление имени с каналом
            with self.users_lock:
                self.users[username] = chan

            thread = Thread(target=lambda: self.client_handler(username, chan))
            thread.start()

            # После открытия двух каналов, перестаем принимать соединения
            with self.users_lock:
                if len(self.users) == 2:
                    server_socket.close()
                    time.sleep(0.1)
                    self.server_print("stopped serving new connections")
                    break

    # noinspection PyMethodMayBeStatic
    def server_print(self, string: str):
        loggers.get_logger().log(string)
        print("server:", string)
