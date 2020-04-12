import sys
import configparser
from plot import plot_dataset, main as truc


class Model:
    def __init__(self, km_list, price_list, max_x):
        self.config = get_default_config()
        self.alpha = int(self.config["UNTRAINED"]["alpha"])
        self.beta = int(self.config["UNTRAINED"]["beta"])
        self.learning_rate = float(self.config["UNTRAINED"]["learning_rate"])
        # self.theta = [[self.beta], [self.alpha]]

        self.dataset_len = len(km_list)
        self.price = price_list
        # self.km = [[1, km] for km in km_list]
        self.km = km_list
        self.max = max_x
        self.max_loop = 100

    def train(self):
        for _ in range(self.max_loop):

            cost_beta, cost_alpha = self.compute_cost()

            tmp_beta = (self.learning_rate / self.dataset_len) * cost_beta
            tmp_alpha = (self.learning_rate / self.dataset_len) * cost_alpha

            self.beta = self.beta - tmp_beta
            self.alpha = self.alpha - tmp_alpha
            print(self.beta, self.alpha / self.max)

    def compute_cost(self):
        theta_0 = 0
        theta_1 = 0
        # compute sum
        for i in range(self.dataset_len):
            distance = self.hypothesis(self.km[i]) - self.price[i]
            theta_0 += distance
            theta_1 += distance * self.km[i]
        return (theta_0, theta_1)

    def hypothesis(self, x):
        res = self.beta + self.alpha * x
        return res

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


def print_usage():
    print("python3 train_model.py <dataset_path.csv>")


def main(dataset):
    try:
        data = parse_dataset(dataset)
    except Exception as e:
        exit(f"Error : {e}")

    # Plot the dataset
    truc()
    max_km = max(data["km"])
    data["km"] = [k / max_km for k in data["km"]]
    data["price"] = [k / max_km for k in data["price"]]

    model = Model(data["km"], data["price"], max_km)
    model.train()
    model.save()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
    else:
        main(sys.argv[1])
