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

	return parser.parse_args()


if __name__ == ("__main__"):
	arguments = parse_command_line()

	number_comments = arguments.number_comments

	for i in range(0, number_comments):
		generated_comment = erinhhbot.generate_comment()
		predicted_upvotes = 0

		# To do: predict upvotes
		# going to have to transform the data in /scored_comments to work, probably want to use pandas dataframes

		linear_regression_model = linear_model.LinearRegression()
		linear_regression_model.fit(X,y)

		print("generated_comment: {}, expected score: {}".format(generated_comment, predicted_upvotes))