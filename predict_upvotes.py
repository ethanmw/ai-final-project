#!/usr/bin/env python3
import os
import sys
import csv
import argparse
import erinhhbot
from sklearn import linear_model
from sklearn.decomposition import PCA


def transform_scored_comments(data_file_path):

	new_data_file_path=data_file_path[0:-4]+"_mod.csv"

	if os.path.isfile(new_data_file_path):
		print("Train file already exists")
		return new_data_file_path

	word_list = []
	data_object_list = []

	print("read in start")

	with open(data_file_path, "r", encoding="utf-8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter="\t")
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

	
	with open(new_data_file_path, "w+", encoding="utf-8") as output_file:
		for word in word_list:
			output_file.write("{}\t".format(word))
		output_file.write("score")
		output_file.write("\n")
		for data_object in new_data_object_list:
			for feature in data_object:
				output_file.write("{}\t".format(feature))
			output_file.write("\n")

	print("Done")
	return new_data_file_path

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
	parser.add_argument("-t", "--train_file",
						type=str,
						dest="train_file",
						required=True)


	return parser.parse_args()


if __name__ == ("__main__"):


	arguments = parse_command_line()

	input_files = arguments.input_files
	weights = arguments.weights
	state_size = arguments.state_size
	train_file = arguments.train_file

	number_comments = arguments.number_comments

	new_train_file = transform_scored_comments(train_file)

	features = list()
	scores = list()
	labels = None
	with open(new_train_file, "r", encoding="utf-8") as csv_file:
		i = 0
		csv_reader = csv.reader(csv_file, delimiter="\t")
		labels = next(csv_reader)
		for row in csv_reader:
			features.append(list())
			for feature in row[0:-1]:
				features[i].append(feature)
			scores.append(0 if row[-1] == '' else int(row[-1]))
			i = i + 1

	if len(input_files) is not len(weights):
			raise ValueError("must specify the same number of input files and weights")

	input_file_weight_pairs = []
	for i in range(0,len(input_files)):
		input_file_weight_pairs.append((input_files[i],weights[i]))

	print("start pca")

	pca = PCA(n_components=len(features[0]))
	transformed_features = pca.fit_transform(features)
	explained_variance_ratio = pca.explained_variance_ratio_

	for i in range(0, len(transformed_features[0])):
		if explained_variance_ratio[i] < 0.01:
			break

	new_transformed_features = []
	for feature_list in transformed_features:
		new_feature_list = []
		for n in range(0, j):
			new_feature_list.append(feature_list[n])
		new_transformed_features.append(new_feature_list)

	print(new_transformed_features[0])

	print("Starting fit")
	linear_regression_model = linear_model.LinearRegression()
	linear_regression_model.fit(features,scores, verbosity = 10)

	print("Done fitting")
	for i in range(0, number_comments):

		generated_comment = erinhhbot.generate_comment(input_file_weight_pairs, state_size,verbosity = 2)
		predicted_upvotes = 0

		comment_features = list()
		for l in labels:
			if l in generated_comment.split():
				comment_features.append('1,')
			else:
				comment_features.append('0,')
		print("Predicting")
		print(linear_regression_model.predict(comment_features))
		# To do: predict upvotes
		# going to have to transform the data in /scored_comments to work, probably want to use pandas dataframes

		

		#print("generated_comment: {}, expected score: {}".format(generated_comment, predicted_upvotes))