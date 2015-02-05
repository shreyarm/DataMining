
if __name__ == '__main__':
    #parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("train_file", help="Name of file with training data", type=str)
    parser.add_argument("--y_col", help="name of column containing target", type=str)
    parser.add_argument("--ibm", help="Flag to indicate that input is IBM data, else plain CSV", action="store_true")
    args = parser.parse_args()

    #for you to add is logic for handling the --y_col flag if given (for tennis, for example)
    if args.ibm:
        data = joblib.load(args.train_file)
    else:
        if not args.y_col:
          data = mlUtil.extract_data(args.train_file)
        else:
          data = mlUtil.extract_data(fileName=args.train_file,targetInfo=args.y_col)
    data = mlUtil.enhance_data(data)
    #will need some args in constructor

    tree = DecisionTree(attrib_d = data['feature_dict'], attribs = data['feature_names'],default_v="default")
    tree.fit(data['data'], data['target'])
    #pritnTree(tree.clf)
    #test on training data
    tree.predict(data['data'])