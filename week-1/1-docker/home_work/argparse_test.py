# Testing *args using argparse

import argparse

def get_args():
    #parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--name" , help="Just 1 argument")
    parser.add_argument("--something" , nargs="*", help="Any number of arguments")
    parser.add_argument("--education" , help="Just 1 argument")

    args = parser.parse_args()
    return args

def main():
    args = get_args()
    name = args.name
    education = args.education
    something = args.something
    print(name)
    print(type(something))
    print(something == None)
    print(education)


if __name__ == "__main__":
    main()