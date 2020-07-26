from sys import argv
from numpy import mean, std
from math import pow, sqrt, pi, e
from csv import reader

# For marker:
# If you want to run this file, please use the run.sh file.
# In that file, you will be able to run normal and cross validation
# mode.
# Thank you.


final_array = []


def nearest_neighbour(train_array, test_array,
                      k, length_number, do_print=True):
    for line_of_test in test_array:
        distances = []
        for line_of_train in train_array["yes"]:
            sum = 0
            for index in range(length_number):
                sum += pow(float(line_of_train[index])
                           - float(line_of_test[index]), 2)
            distances.append((sqrt(sum), "yes"))

        for line_of_train in train_array["no"]:
            sum = 0
            for index in range(length_number):
                sum += pow(float(line_of_train[index])
                           - float(line_of_test[index]), 2)
            distances.append((sqrt(sum), "no"))

        distances = sorted(distances)[:k]
        no = 0
        yes = 0
        for item in distances:
            if item[1] == 'yes':
                yes += 1
            elif item[1] == 'no':
                no += 1
        # print("No number: "+ str(no))
        # print("Yes number: "+ str(yes))
        if no > yes:
            final_array.append("no")
        else:
            final_array.append("yes")
    if (do_print):
        print_out_final()


def naive_bayes(train_array, test_array, number_of_attributes,
                do_print=True):
    length_no = len(train_array["no"])
    length_yes = len(train_array["yes"])
    # print("No count: "+ str(length_no))
    # print("Yes count: "+ str(length_yes))
    for line_of_test in test_array:
        yes_final = None
        no_final = None
        yes_probabilities = []
        no_probabilities = []
        columns = []
        for index, line_of_train in enumerate(train_array["yes"]):
            if index == 0:
                for i in range(number_of_attributes):
                    columns.append([float(line_of_train[i])])
            else:
                for i in range(number_of_attributes):
                    # print(yes_columns[i])
                    columns[i].append(float(line_of_train[i]))
        # print(yes_columns)
        for idx, column in enumerate(columns):
            yes_probabilities.append(generate_pdf(
                (mean(column), std(column, ddof=1)),
                float(line_of_test[idx])))

        # print(yes_probabilities)
        for idx, yes_item in enumerate(yes_probabilities):
            if yes_item is not None:
                if idx == 0:
                    yes_final = yes_item
                else:
                    yes_final = yes_final * yes_item
        if yes_final is not None:
            yes_final = yes_final * (length_yes/(length_yes + length_no))

        # Clear my columns
        del columns[:]

        for index, line_of_train in enumerate(train_array["no"]):
            if index == 0:
                for i in range(number_of_attributes):
                    columns.append([float(line_of_train[i])])
            else:
                for i in range(number_of_attributes):
                    # print(yes_columns[i])
                    columns[i].append(float(line_of_train[i]))
        # print(columns)
        for idx, column in enumerate(columns):
            no_probabilities.append(generate_pdf((mean(column),
                                                  std(column, ddof=1)),
                                                 float(line_of_test[idx])))

        # print(no_probabilities)
        for idx, no_item in enumerate(no_probabilities):
            if no_item is not None:
                if idx == 0:
                    no_final = no_item
                else:
                    no_final = no_final * no_item
        if no_final is not None:
            no_final = no_final * (length_no/(length_yes + length_no))
        # print(no_final)

        if (no_final is not None and yes_final is None):
            final_array.append("no")
        elif ((no_final is None and yes_final is not None) or
              no_final == yes_final or yes_final > no_final):
            final_array.append("yes")
        elif (no_final > yes_final):
            final_array.append("no")

    if (do_print):
        print_out_final()


def generate_pdf(block, cur_num):
    if block[1] == 0:
        return None
    # print(block)
    # print(cur_num)
    first = 1/(block[1]*sqrt(2 * pi))
    second = pow(e, -1*pow(cur_num - block[0], 2)/(2*pow(block[1], 2)))
    # print(first*second)
    return first*second


def print_out_final():
    for item in final_array:
        print(item)


def initialise_array(raw_data, train, fold_number=None):
    with open(raw_data) as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        if fold_number is None:
            if train:
                yes = []
                no = []
                for row in csv_reader:
                    if (row[-1] == "yes"):
                        yes.append(row[:-1])
                    else:
                        no.append(row[:-1])
                return {"yes": yes, "no": no}
            else:
                i_collection = []
                for row in csv_reader:
                    i_collection.append(tuple(row))
                return tuple(i_collection)
        else:
            if train is False:
                cross_collection = []
                found = False
                # print(list(csv_reader))
                for row in csv_reader:
                    if ("fold" + str(fold_number) in row):
                        # print(fold_number)
                        found = True
                    elif (found):
                        if (row != []):
                            cross_collection.append(tuple(row))
                        if (row == []):
                            # print(cross_collection)
                            return tuple(cross_collection)
            # Now we look at the training data
            else:
                if (fold_number == 1):
                    # print(len(test_array))
                    training_data = list(csv_reader)[77:]
                    # print(training_data)
                    # print(produce_training_dictionary(training_data))
                    return produce_training_dictionary(training_data)

            #         ignore the first 77 lines
                else:
                    if (fold_number != 9 and fold_number != 10):
                        training_data = list(csv_reader)[0:77*(
                            fold_number - 1)] + list(
                                csv_reader)[77*fold_number:]
                        return produce_training_dictionary(training_data)

                    elif (fold_number == 9):
                        # print(list(csv_reader)[692])
                        training_data = list(csv_reader)[0:616] + list(
                            csv_reader)[692:]
                        return produce_training_dictionary(training_data)
                    elif (fold_number == 10):
                        training_data = list(csv_reader)[0:692]
                        return produce_training_dictionary(training_data)
                        # print()

                # print(row)
            # print(csv_reader)


def produce_training_dictionary(data):
    yes = []
    no = []
    for row in data:
        if (row[-1] == "yes"):
            yes.append(row[:-1])
        else:
            no.append(row[:-1])
    return {"yes": yes, "no": no}


if (len(argv) == 4):
    train_array = initialise_array(argv[1], True)
    test_array = initialise_array(argv[2], False)
    attribute_num = len(test_array[0])
    if ("nn" in argv[3].lower()):
        nearest_neighbour(train_array, test_array,
                          int(argv[3].lower().rstrip("nn")), attribute_num)
        # pass
    elif ("nb" in argv[3].lower()):
        naive_bayes(train_array, test_array, attribute_num)

elif (len(argv) == 5):
    if ("cross" in argv[4].lower()):
        accuracies = []
        for fold_number in range(1, 11):
            # fold_number=9
            # print("fold number--------- " + str(fold_number))
            test_array = initialise_array(argv[2], False, fold_number)
            train_array = initialise_array(argv[1], True, fold_number)
            attribute_num = len(test_array[0]) - 1

            if ("nn" in argv[3].lower()):
                nearest_neighbour(train_array, test_array,
                                  int(argv[3].lower().rstrip("nn")),
                                  attribute_num, False)
                # pass
            elif ("nb" in argv[3].lower()):
                naive_bayes(train_array, test_array, attribute_num, False)
                # pass
            correct = 0
            wrong = 0
            for idx, item in enumerate(test_array):
                if (item[-1] == final_array[idx]):
                    correct += 1
                else:
                    wrong += 1
            print("--------------------")
            print("For fold: " + str(fold_number))
            print("Correct number: " + str(correct))
            print("Wrong number: " + str(wrong))
            percentage = (correct/(correct+wrong))*100
            print("Percentage: " + str(percentage) + " %")
            accuracies.append(percentage)

        print("Average accuracy: " + str(mean(accuracies)))

else:
    print("Missing arguments. Expected 4 arguments")
