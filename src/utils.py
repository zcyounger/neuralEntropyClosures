'''
Accumulation of utility functions
Date: 15.03.2021
Author: Steffen Schotthöfer
'''

import numpy as np
import time
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import random
import os
from pathlib import Path
import git


def finiteDiff(x, y):
    '''
    :param x: Function Argument
    :param y: Function value = f(x)
    :return: df/dx at all points x
    '''

    grad = np.zeros(x.shape)

    grad[0] = (y[1] - y[0]) / (x[1] - x[0])

    for i in range(0, x.shape[0] - 1):
        grad[i + 1] = (y[i] - y[i - 1]) / (x[i] - x[i - 1])

    return grad


def integrate(x, y):
    '''
    :param x: function argument
    :param y: = f(x)
    :return: integrate y over span of x
    '''

    integral = np.zeros(x.shape)

    for i in range(0, x.shape[0] - 1):
        integral[i + 1] = integral[i] + (x[i + 1] - x[i]) * y[i + 1]

    return integral


def load_data(filename: str, input_dim: int, selected_cols: list = [True, True, True]) -> list:
    '''
    Load training Data from csv file <filename>
    u, alpha have length <inputDim>
    returns: training_data = [u,alpha,h]
    '''

    training_data = []

    print("Loading Data from location: " + filename)
    # determine which cols correspond to u, alpha and h
    u_cols = list(range(1, input_dim + 1))
    alpha_cols = list(range(input_dim + 1, 2 * input_dim + 1))
    h_col = [2 * input_dim + 1]

    # selectedCols = self.selectTrainingData() #outputs a boolean triple.
    start = time.time()
    if selected_cols[0]:
        df = pd.read_csv(filename, usecols=[i for i in u_cols])
        uNParray = df.to_numpy()
        training_data.append(uNParray)
    if selected_cols[1]:
        df = pd.read_csv(filename, usecols=[i for i in alpha_cols])
        alphaNParray = df.to_numpy()
        training_data.append(alphaNParray)
    if selected_cols[2]:
        df = pd.read_csv(filename, usecols=[i for i in h_col])
        hNParray = df.to_numpy()
        training_data.append(hNParray)

    end = time.time()
    print("Data loaded. Elapsed time: " + str(end - start))

    return training_data


def evaluateModel(model, input):
    '''Evaluates the model at input'''
    # x = input
    # print(x.shape)
    # print(x)
    return model.predict(input)


def evaluateModelDerivative(model, input):
    '''Evaluates model derivatives at input'''

    x_model = tf.Variable(input)

    with tf.GradientTape() as tape:
        # training=True is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(x_model, training=False)  # same as model.predict(x)

    gradients = tape.gradient(predictions, x_model)
    return gradients


def loadTFModel(filename):
    '''Loads a .h5 file to memory'''
    nn = tf.keras.models.load_model(filename)
    return nn


def plot1D(xs, ys, labels=[], name='defaultName', log=True, folder_name="figures", linetypes=[], show_fig=False,
           ylim=None, xlabel=None, ylabel=None):
    plt.clf()
    if not linetypes:
        linetypes = ['-', '--', '-.', ':', ':', '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*',
                     'h',
                     'H',
                     '+', 'x', 'D', 'd', '|']
        linetypes = linetypes[0:len(labels)]

    if len(xs) == 1:
        x = xs[0]
        for y, lineType in zip(ys, linetypes):
            plt.plot(x, y, lineType, linewidth=1, markersize=1000)
        plt.legend(labels)
    elif len(xs) is not len(ys):
        print("Error: List of x entries must be of same length as y entries")
        exit(1)
    else:
        for x, y, lineType in zip(xs, ys, linetypes):
            plt.plot(x, y, lineType, linewidth=1)
        plt.legend(labels)  # , prop={'size': 6})
    if log:
        plt.yscale('log')

    if show_fig:
        plt.show()
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
    if xlabel is not None:
        plt.xlabel(xlabel)  # , fontsize=8)
        # plt.xticks(fontsize=6)
        # plt.yticks(fontsize=6)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=6)
    plt.savefig(folder_name + "/" + name + ".png", dpi=500)
    print("Figure successfully saved to file: " + str(folder_name + "/" + name + ".png"))
    return 0


def scatterPlot2D(x_in: np.ndarray, y_in: np.ndarray, name: str = 'defaultName', log: bool = True,
                  folder_name: str = "figures", show_fig: bool = False, z_lim: float = 0.0) -> bool:
    '''
    brief: Compute a scatter plot
    input: x_in = [x1,x2] function arguments
           y_in = function values
    return: True if exit successfully
    '''
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)  # , projection='3d')
    ax.grid(True, linestyle='-', color='0.75')
    x = x_in[:, 0]
    y = x_in[:, 1]
    z = y_in
    if log:
        out = ax.scatter(x, y, s=20, c=z, cmap=cm.hot, norm=colors.LogNorm(), vmax=z_lim)
    else:
        out = ax.scatter(x, y, s=20, c=z, cmap=cm.hot)
    ax.set_title(name, fontsize=14)
    ax.set_xlabel("u1", fontsize=12)
    ax.set_ylabel("u2", fontsize=12)
    # ax.set_xlabel('N1')
    # ax.set_ylabel('N2')
    # ax.set_zlabel('h')
    # pos_neg_clipped = ax.imshow(z)
    cbar = fig.colorbar(out, ax=ax, extend='both')

    if show_fig:
        plt.show()
    plt.savefig(folder_name + "/" + name + ".png", dpi=150)

    return True


def shuffleTrainData(x, y, mode="random"):
    c = list(zip(x, y))

    random.shuffle(c)

    x, y = zip(*c)

    return [np.asarray(x), np.asarray(y)]


def writeConfigFile(options, neural_closure_model):
    # create String to create a python runscript
    runScript = "python callNeuralClosure.py \\\n"
    runScript = runScript + "--sampling=" + str(int(options.sampling)) + " \\\n"
    runScript = runScript + "--batch=" + str(options.batch) + " \\\n"
    runScript = runScript + "--curriculum=" + str(options.curriculum) + " \\\n"
    runScript = runScript + "--degree=" + str(options.degree) + " \\\n"
    runScript = runScript + "--epoch=" + str(options.epoch) + " \\\n"
    runScript = runScript + "--folder=" + str(options.folder) + " \\\n"
    runScript = runScript + "--loadModel=" + str(1) + " \\\n"  # force to load
    runScript = runScript + "--model=" + str(options.model) + " \\\n"
    runScript = runScript + "--normalized=" + str(int(options.normalized)) + " \\\n"
    runScript = runScript + "--scaledOutput=" + str(int(options.scaledOutput)) + " \\\n"
    runScript = runScript + "--decorrInput=" + str(int(options.decorrInput)) + " \\\n"
    runScript = runScript + "--objective=" + str(options.objective) + " \\\n"
    runScript = runScript + "--processingmode=" + str(options.processingmode) + " \\\n"
    runScript = runScript + "--spatialDimension=" + str(options.spatialDimension) + " \\\n"
    runScript = runScript + "--training=" + str(options.training) + " \\\n"
    runScript = runScript + "--verbosity=" + str(options.verbosity) + " \\\n"
    runScript = runScript + "--networkwidth=" + str(options.networkwidth) + " \\\n"
    runScript = runScript + "--networkdepth=" + str(options.networkdepth)

    # Getting filename
    rsFile = neural_closure_model.folder_name + '/runScript_001_'
    count = 0

    # create directory if it does not exist
    make_directory(neural_closure_model.folder_name)

    while os.path.isfile(rsFile + '.sh'):
        count += 1
        rsFile = neural_closure_model.folder_name + '/runScript_' + str(count).zfill(3) + '_'

    rsFile = rsFile + '.sh'

    print("Writing config to " + rsFile)
    f = open(rsFile, "w")
    f.write(runScript)
    f.close()

    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    print("Current git checkout: " + str(sha))
    # Print chosen options to csv
    d = {'git_version': [sha],
         'sampling': [options.sampling],
         'batch': [options.batch],
         'curriculum': [options.curriculum],
         'degree': [options.degree],
         'epoch': [options.epoch],
         'folder': [options.folder],
         'loadModel': [options.loadmodel],
         'model': [options.model],
         'normalized moments': [options.normalized],
         'decorrelate inputs': [options.decorrInput],
         'scaled outputs': [options.scaledOutput],
         'objective': [options.objective],
         'processingmode': [options.processingmode],
         'spatial Dimension': [options.spatialDimension],
         'verbosity': [options.verbosity],
         'training': [options.training],
         'network width': [options.networkwidth],
         'network depth': [options.networkdepth]}

    count = 0
    cfg_file = neural_closure_model.folder_name + '/config_001_'

    while os.path.isfile(cfg_file + '.csv'):
        count += 1
        cfg_file = neural_closure_model.folder_name + '/config_' + str(count).zfill(3) + '_'
    cfg_file = cfg_file + '.csv'
    pd.DataFrame.from_dict(data=d, orient='index').to_csv(cfg_file, header=False, sep=';')
    return True


def make_directory(path_to_directory):
    if not os.path.exists(path_to_directory):
        p = Path(path_to_directory)
        p.mkdir(parents=True)
    return 0


def kl_divergence_loss(m_b, q_w):
    """
    KL divergence between f_u and f_true  using alpha and alpha_true.
    inputs: mB, moment Basis evaluted at quadPts, dim = (N x nq)
            quadWeights, dim = nq
    returns: KL_divergence function using mBasis and quadWeights
    """

    def reconstruct_alpha(alpha):
        """
        brief:  Reconstructs alpha_0 and then concats alpha_0 to alpha_1,... , from alpha1,...
                Only works for maxwell Boltzmann entropy so far.
                => copied from sobolev model code
        nS = batchSize
        N = basisSize
        nq = number of quadPts

        input: alpha, dims = (nS x N-1)
               m    , dims = (N x nq)
               w    , dims = nq
        returns alpha_complete = [alpha_0,alpha], dim = (nS x N), where alpha_0 = - ln(<exp(alpha*m)>)
        """
        # Check the predicted alphas for +/- infinity or nan - raise error if found
        checked_alpha = tf.debugging.check_numerics(alpha, message='input tensor checking error', name='checked')
        # Clip the predicted alphas below the tf.exp overflow threshold
        clipped_alpha = tf.clip_by_value(checked_alpha, clip_value_min=-50, clip_value_max=50,
                                         name='checkedandclipped')

        tmp = tf.math.exp(tf.tensordot(clipped_alpha, m_b[1:, :], axes=([1], [0])))  # tmp = alpha * m
        alpha_0 = -tf.math.log(tf.tensordot(tmp, q_w, axes=([1], [1])))  # ln(<tmp>)
        return tf.concat([alpha_0, alpha], axis=1)  # concat [alpha_0,alpha]

    def kl_divergence(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        """
        brief: computes the Kullback-Leibler Divergence of the kinetic density w.r.t alpha given the kinetic density w.r.t
                alpha_true
        input: alpha_true , dim= (ns,N)
               alpha , dim = (ns, N+1)
        output: pointwise KL Divergence, dim  = ns x 1
        """

        # extend alpha_true to full dimension
        alpha_true_recon = reconstruct_alpha(y_true)
        alpha_pred_recon = reconstruct_alpha(y_pred)
        # compute KL_divergence
        diff = alpha_true_recon - alpha_pred_recon
        t1 = tf.math.exp(tf.tensordot(alpha_true_recon, m_b, axes=([1], [0])))
        t2 = tf.tensordot(diff, m_b, axes=([1], [0]))
        integrand = tf.math.multiply(t1, t2)
        return tf.tensordot(integrand, q_w, axes=([1], [1]))

    return kl_divergence
