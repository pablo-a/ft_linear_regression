import configparser
import sys
import matplotlib.pyplot as plt


class LinearRegressionModel:
    def __init__(self, X, Y):
        self.config = get_default_config()

        # Dataset
        self.km = X
        self.price = Y
        self.length_dataset = len(self.km)
        self.max_value = max(*self.km, *self.price)

        # Regression coefficients
        self.alpha = int(self.config["UNTRAINED"]["alpha"])
        self.beta = int(self.config["UNTRAINED"]["beta"])

        # model parameters
        self.learning_rate = float(self.config["UNTRAINED"]["learning_rate"])
        self.max_loop = 10_000

    def scale_feature(self):
        self.km = [km / self.max_value for km in self.km]

    def hypothesis(self, x):
        return self.alpha * x + self.beta

    def prediction_list(self):
        return [self.hypothesis(x) for x in self.km]

    def error_list(self):
        return [pred - y for pred, y in zip(self.prediction_list(), self.price)]

    def gradient_alpha(self):
        return sum([cost * km for cost, km in zip(self.error_list(), self.km)])

    def gradient_beta(self):
        return sum([cost for cost in self.error_list()])

    def train(self):
        coeff = self.learning_rate / self.length_dataset
        for _ in range(self.max_loop):
            update_alpha = coeff * self.gradient_alpha()
            update_beta = coeff * self.gradient_beta()

            self.alpha -= update_alpha
            self.beta -= update_beta
        self.alpha /= self.max_value

    def save(self):
        self.config["TRAINED"]["alpha"] = str(self.alpha)
        self.config["TRAINED"]["beta"] = str(self.beta)
        with open("parameters.ini", "w") as trained_file:
            self.config.write(trained_file)


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


def get_default_config():
    config = configparser.ConfigParser()
    config.read("parameters.ini")
    return config


def plot_regression(data, model):
    plt.xlabel("kilometers")
    plt.ylabel("price")
    plt.scatter(data["km"], data["price"])
    x = [0, 250_000]
    y = list(map(model.hypothesis, x))
    plt.plot(x, y)
    plt.show()


def print_usage():
    print("\nUsage:\npython train.py --dataset <path/to/dataset> [--plot]\n")


def main(dataset, plot_option):
    try:
        data = parse_dataset(dataset)
    except Exception as e:
        exit(f"Error : {e}")

    linear_model = LinearRegressionModel(X=data["km"], Y=data["price"])
    linear_model.scale_feature()
    linear_model.train()
    linear_model.save()

    if plot_option:
        plot_regression(data, linear_model)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        exit(1)
    dataset_path = sys.argv[2]
    try:
        plot_option = sys.argv[3] == "--plot"
    except IndexError:
        plot_option = False
    main("./data_linear_reg.csv", plot_option)
