import pandas as pd
import sys


def main(argv):
    if len(argv) < 2:
        print('Not enough arguments provided.')
        return

    in_dfs = []
    for input_file in sys.argv[1:-1]:
        in_dfs.append(pd.read_csv(input_file))

    out_df = pd.concat(in_dfs)
    output_file = sys.argv[-1]
    out_df.to_csv(output_file, index=False)
    print('Wrote merged CSV data to "%s".' % output_file)


if __name__ == "__main__":
    main(sys.argv)
