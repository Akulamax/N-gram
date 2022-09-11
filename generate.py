from main_train import NgramModelTextGeneration
import pickle
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prefix")
    parser.add_argument("--length", required=True)
    args = parser.parse_args()
    pkl_filename = args.model
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    prefix = args.prefix if args.prefix else ""
    result = pickle_model.generate(int(args.length), prefix)
    for i, word in enumerate(result):
      print(word, end=" ")
      if (i != 0 and i % 15 == 0): print('\n')

        
if __name__ == "__main__":
    main()
