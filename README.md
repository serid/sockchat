## Инструкция по установке

Для запуска приложения sockchat требуется выполнить следующие шаги:
1. Установить Python 3.9. На дистрибутиве Oracle Linux он идет предустановленным.
2. Установить пакетный менеджер pip, для этого необходимо выполнить команды

```
alias python=python3
python -m ensurepip --upgrade
```
3. Установить пакет sockchat

```
alias python=python3
python -m ensurepip --upgrade
python -m pip install sockchat
```

## Пример использования приложения

### Запуск сервера
```
python -m sockchat –-server
```
### Подключение к серверу.
[username] необходимо заменить на имя пользователя, а [address] на адрес сервера (можно использовать localhost).
```
python -m sockchat [username] [address]
```
### Получение справки по командам
```
python -m sockchat –-help
```
