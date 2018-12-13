#!/usr/bin/env python3
import argparse
import erinhhbot
from sklearn import linear_model


def parse_command_line():
	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--number-comments",
						type=int,
						dest="number_comments",
						default=1)
	parser.add_argument("-i", "--input-file",
						action="append",
						dest="input_files",
						required=True)

	parser.add_argument("-w", "--weight",
						type=float,
						action="append",
						dest="weights",
						required=True)
	parser.add_argument("-s", "--state-size",
						type=int,
						dest="state_size",
						default=2)


	return parser.parse_args()


if __name__ == ("__main__"):


	arguments = parse_command_line()

	input_files = arguments.input_files
	weights = arguments.weights
	state_size = arguments.state_size



	number_comments = arguments.number_comments

	if len(input_files) is not len(weights):
			raise ValueError("must specify the same number of input files and weights")

	input_file_weight_pairs = []
	for i in range(0,len(input_files)):
		input_file_weight_pairs.append((input_files[i],weights[i]))

	for i in range(0, number_comments):

		generated_comment = erinhhbot.generate_comment(input_file_weight_pairs, state_size)
		predicted_upvotes = 0

		# To do: predict upvotes
		# going to have to transform the data in /scored_comments to work, probably want to use pandas dataframes

		linear_regression_model = linear_model.LinearRegression()
		linear_regression_model.fit(X,y)

		print("generated_comment: {}, expected score: {}".format(generated_comment, predicted_upvotes))