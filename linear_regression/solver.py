import configparser
import sys


def main():
    config = configparser.ConfigParser()
    config.read("parameters.ini")

    alpha = float(config["TRAINED"]["alpha"])
    beta = float(config["TRAINED"]["beta"])

    status = "READ"
    while status == "READ":
        print("Enter a Car mileage :")
        input = sys.stdin.readline()
        input = input.replace("\n", "")

        if input == "" or input == "exit":
            status = "STOP"

        if not input.isdigit():
            print("Input must be an integer\n")

        try:
            price = beta + (alpha * float(input))
            print(f"Average price is {price}")
        except ValueError:
            continue


if __name__ == "__main__":
    main()
