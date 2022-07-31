import subprocess


def main():
    client = subprocess.Popen(["python3", "src/sockchat/__main__.py", "doge", "localhost"])
    server = subprocess.Popen(["python3", "src/sockchat/__main__.py", "--server"])
    client.wait()
    server.wait()

    # print(client.stdout)


if __name__ == "__main__":
    main()
