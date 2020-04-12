import pandas as pd
import sys
import matplotlib.pyplot as plt
import configparser


def main():
    data = parse_dataset("./data_linear_reg.csv")
    plot_dataset(data)
    # plot_regression(data)
    plt.show()


def plot_dataset(data):
    # dic to pandas Dataframe.
    dataset = pd.read_csv("data_linear_reg.csv")
    plt.scatter(dataset.km, dataset.price)
    # create plot

    plt.show()


def plot_regression(data):
    config = get_default_config()
    alpha = float(config["DEFAULT"]["Alpha"])
    beta = float(config["DEFAULT"]["Beta"])

    min_x = min(data["km"])
    max_x = max(data["km"])
    x_list = [min_x, max_x]

    y_list = map(lambda x: alpha + x + beta, x_list)
    dataset = pd.DataFrame(y_list, x_list)

    # sns.lineplot(data=dataset)


def get_default_config():
    config = configparser.ConfigParser()
    config.read("parameters.ini")
    return config


def parse_dataset(training_file):
    data = {}
    with open(training_file, "r") as f:

        # SETUP headers
        header_line = f.readline()
        # remove line breaking
        header_line = header_line.replace("\n", "")
        header_list = header_line.split(",")
        for header in header_list:
            data[header] = []

        # FILL Data
        for line in f:
            line = line.strip()
            new_data = line.split(",")
            for column, feature in enumerate(new_data):
                according_header = header_list[column]
                data[according_header].append(int(feature))

    return data


if __name__ == "__main__":
    main()
