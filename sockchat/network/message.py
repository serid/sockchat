from dataclasses import dataclass
from enum import IntEnum, auto
from json import dumps, loads


# noinspection PyArgumentList
class MessageType(IntEnum):
    LOGIN = auto()
    TEXT = auto()
    ACK = auto()
    DISCONNECT = auto()


@dataclass(slots=True)
class Message:
    pass


@dataclass(slots=True)
class LoginMessage(Message):
    name: str


# id сообщения указывает порядковый номер сообщения в клиенте. id сообщений разных пользователей могут совпадать
@dataclass(slots=True)
class TextMessage(Message):
    username: str
    text: str
    id: int


@dataclass(slots=True)
class AckMessage(Message):
    """Подтверждение о доставке сообщения с id [id] пользователю [username]"""
    text_by_username: str  # Имя клиента который отправил изначальное сообщение
    acknowledged_by_username: str  # Имя клиента, получившего сообщение
    id: int  # id сообщения в клиенте [text_by_username]


@dataclass(slots=True)
class DisconnectMessage(Message):
    pass


def encode_message(message: Message) -> str:
    match message:
        case LoginMessage(name=name):
            return dumps({"type": MessageType.LOGIN, "name": name})
        case TextMessage(username=username, text=text, id=id_):
            return dumps({"type": MessageType.TEXT, "username": username, "text": text, "id": id_})
        case AckMessage(text_by_username=text_by_username, acknowledged_by_username=acknowledged_by_username, id=id_):
            return dumps({"type": MessageType.ACK, "text_by_username": text_by_username,
                          "acknowledged_by_username": acknowledged_by_username, "id": id_})
        case DisconnectMessage():
            return dumps({"type": MessageType.DISCONNECT})


def decode_message(s: str) -> Message:
    dictionary = loads(s)
    match dictionary["type"]:
        case MessageType.LOGIN:
            return LoginMessage(dictionary["name"])
        case MessageType.TEXT:
            return TextMessage(dictionary["username"], dictionary["text"], dictionary["id"])
        case MessageType.ACK:
            return AckMessage(dictionary["text_by_username"], dictionary["acknowledged_by_username"], dictionary["id"])
        case MessageType.DISCONNECT:
            return DisconnectMessage()
