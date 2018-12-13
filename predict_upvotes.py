#!/usr/bin/env python3
import sys
import csv
import argparse
import erinhhbot
from sklearn import linear_model


def transform_scored_comments(data_file_path):
	word_list = []
	data_object_list = []

	print("read in start")

	with open(data_file_path, "r", encoding="utf-8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		for row in csv_reader:
			try:
				data_object_list.append(row)
				comment = row[0].split()
				for word in comment:
					word_list.append(word)
			except:
				pass

	print("read in done")

	word_list = list(set(word_list))
	number_features = len(word_list)
	new_data_object_list = []

	for data_object in data_object_list:
		new_data_object = [0] * (number_features+1)

		for i in range(0, len(word_list)):
			if word_list[i] in data_object[0].split():
				new_data_object[i] = 1
		new_data_object[-1] = data_object[-1]
		new_data_object_list.append(new_data_object)

	new_data_file_path=data_file_path[0:-4]+"_mod.csv"
	with open(new_data_file_path, "w+", encoding="utf-8") as output_file:
		for word in word_list:
			output_file.write("{},".format(word))
		output_file.write("score")
		output_file.write("\n")
		for data_object in new_data_object_list:
			for feature in data_object:
				output_file.write("{},".format(feature))
			output_file.write("\n")



def parse_command_line():
	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--number-comments",
						type=int,
						dest="number_comments",
						default=1,
						required=False)

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