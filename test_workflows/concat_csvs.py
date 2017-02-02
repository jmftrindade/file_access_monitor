import pandas as pd
import sys


def main(argv):
    if len(argv) < 2:
        print('Not enough input files provided.')
        return

    in_dfs = []
    for input_file in sys.argv[1:]:
        in_dfs.append(pd.read_csv(input_file))

    out_df = pd.concat(in_dfs)
    out_df.to_csv('out1.csv', index=False)
    print('Wrote merged CSV data to "out1.csv".')


if __name__ == "__main__":
    main(sys.argv)
