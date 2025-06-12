import matplotlib.pyplot as plt
import itertools as it
import pandas as pd
import numpy as np
import os

def smooth_line(x, y, args):
    T = len(x)
    T = (T // args.n_smooth) * args.n_smooth
    x = x[:T].reshape(-1, args.n_smooth)
    x = x[:, 0]
    y = y[:T].reshape(-1, args.n_smooth)
    y = np.mean(y, axis=1)
    return x, y

def load(args):
    label = f'{args.mode}/{args.dataset}_{args.n_node}_{args.solver}'
    path = os.path.join(args.csv_dir, f'{label}.csv')
    df = pd.read_csv(path)
    x = df['step'].to_numpy()
    y = df[args.metric].to_numpy()
    x, y = smooth_line(x, y, args)
    return x, y

def plot_line(args):
    plt.cla()
    plt.clf()
    # scenarios
    datasets = ['tsp']
    n_nodes = [5, 10]
    modes = ['train']
    for dataset, n_node, mode in it.product(datasets, n_nodes, modes):
        # assign args
        args.dataset = dataset
        args.n_node = n_node
        args.mode = mode
        label = f'{args.dataset}_{args.n_node}'
        # load csv
        try:
            x, y = load(args)
            # plot
            plt.plot(x, y, '-o', label=label)
        except:
            raise
    # decorate
    plt.legend()
    plt.xlabel('step')
    plt.ylabel(f'{args.metric}')
    plt.tight_layout()
    # save figure
    path = os.path.join(args.figure_dir, f'{args.scenario}_{args.metric}.jpg')
    plt.savefig(path)
