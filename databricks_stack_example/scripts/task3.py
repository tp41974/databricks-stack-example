from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(prog="task1")
    parser.add_argument("--param-1", metavar="ANY", help="the first parameter")
    parser.add_argument("--param-2", metavar="INT", type=int, help="the second parameter")
    args = parser.parse_args()
    print(f'Task 3 executed with parameters: {vars(args)}')