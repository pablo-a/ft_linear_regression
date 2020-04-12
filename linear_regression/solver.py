import configparser
import sys

def main():
    config = configparser.ConfigParser()
    config.read("parameters.ini")

    alpha = float(config['DEFAULT']['Alpha'])
    beta = float(config['DEFAULT']['Beta'])

    status = "READ"
    while status == "READ":
        print("Enter a Car mileage :")
        input = sys.stdin.readline()
        input = input.replace("\n", "")

        if input == "" or input == "exit":
            status = "STOP"

        if not input.isdigit():
            print("Input must be an integer\n")
        
        price = beta + (alpha*float(input))
        print(f"Average price is {price}")

if __name__ == "__main__":
    main()
