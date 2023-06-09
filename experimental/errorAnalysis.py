'''
Script to conduct error Analysis of the Training
Author: Steffen Schotthöfer
Date: 15.03.2021
'''

from src.networks.configmodel import init_neural_closure
import src.utils as utils
import src.math as math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

plt.style.use("kitish")
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})


def main():
    filenameModelAlpha = "models/001_alpha"  # "models/01_errorAnalysis_M1_1D/best_model.h5"
    filenameModelU = "models/001_u"
    filenameData = "Monomial_M1_1D_normal.csv"
    inputDim = 2

    # Load Model
    modelAlpha = init_neural_closure(network_mk=11, poly_degree=1, spatial_dim=1,
                                     folder_name="001_alpha", loss_combination=2,
                                     nw_width=15, nw_depth=7, normalized=True)
    modelAlpha.load_model("../models/001_alpha")
    modelU = init_neural_closure(network_mk=11, poly_degree=1, spatial_dim=1,
                                 folder_name="001_alpha", loss_combination=2,
                                 nw_width=15, nw_depth=7, normalized=True)
    modelU.load_model("../models/001_u")

    # Load Data
    [u, alpha, h] = utils.load_data(filenameData, inputDim)
    [u_modelAlpha, alpha_modelAlpha, h_modelAlpha] = modelAlpha.call_scaled_64(u)
    [u_modelU, alpha_modelU, h_modelU] = modelU.call_scaled_64(u)
    # plot results
    utils.plot_1d([u[:, 1], u[:, 1], u[:, 1]], [h_modelAlpha[:, 0], h_modelU[:, 0], h],
                  [r'$h_{\theta}$ - uniform $\alpha$', r'$h_{\theta}$  - uniform $u$', r'$h$ test'],
                  '000_h', folder_name="ValidationTest", log=False, show_fig=False, xlabel=r"$u_1$")
    # plot results
    utils.plot_1d([u[:, 1], u[:, 1], u[:, 1]], [alpha_modelAlpha[:, 1], alpha_modelU[:, 1], alpha[:, 1]],
                  [r'$\alpha_{1\theta}$ - uniform $\alpha$', r'$\alpha_{1\theta}$  - uniform $u$',
                   r'$\alpha_1$ test'],
                  '000_alpha', folder_name="ValidationTest", log=False, show_fig=False, xlabel=r"$u_1$")
    # plot results
    utils.plot_1d([u[:, 1], u[:, 1], u[:, 1]], [u_modelAlpha[:, 1], u_modelU[:, 1], u[:, 1]],
                  [r'$u_{1\theta}$ - uniform $\alpha$', r'$u_{1\theta}$  - uniform $u$', r'$u_1$ test'],
                  '000_u', folder_name="ValidationTest", log=False, show_fig=False,
                  xlabel=r"$u_1$")

    # plot errors

    ys = [relDifferenceScalar(alpha[:, 1], alpha_modelAlpha[:, 1], maxMode=True),
          relDifferenceScalar(alpha[:, 1], alpha_modelU[:, 1], maxMode=True)]
    utils.plot_1d([u[:, 1], u[:, 1]], ys, [r'uniform $\alpha$', 'uniform $u$'],
                  '000_alphaErr', folder_name="ValidationTest", log=True, show_fig=False,
                  ylabel=r"$|\alpha_1-\alpha_{1,\theta}|/|\alpha_1|$",
                  xlabel=r"$u_1$")

    ys = [relDifferenceScalar(u[:, 1], u_modelAlpha[:, 1], maxMode=True),
          relDifferenceScalar(u[:, 1], u_modelU[:, 1], maxMode=True)]
    utils.plot_1d([u[:, 1], u[:, 1]], ys, [r'uniform $\alpha$', 'uniform $u$'],
                  '000_uErr', folder_name="ValidationTest", log=True, show_fig=False,
                  ylabel=r"$|\alpha_1-\alpha_{1,\theta}|/|\alpha_1|$",
                  xlabel=r"$u_1$")
    ys = [relDifferenceScalar(h, h_modelAlpha, maxMode=True),
          relDifferenceScalar(h, h_modelU, maxMode=True)]
    utils.plot_1d([u[:, 1], u[:, 1]], ys, [r'uniform $\alpha$', 'uniform $u$'],
                  '000_hErr', folder_name="ValidationTest", log=True, show_fig=False,
                  ylabel=r"$|(h-h_{\theta)}|/|h|$",
                  xlabel=r"$u_1$")

    """
    x = u[:, 1]
    ys = [alpha[:, 1], alpha_pred[:, 1]]
    labels = ["alpha 1", "alpha 1 pred"]
    utils.plot1D(x, ys, labels, 'alpha_0', log=False)
    ys = [alpha[:, 0], alpha_pred[:, 0]]
    labels = ["alpha 0", "alpha 0 pred"]
    utils.plot1D(x, ys, labels, 'alpha_0', log=False)
    ys = [relDifferenceScalar(alpha[:, 0], alpha_pred[:, 0], maxMode=False),
          relDifferenceScalar(alpha[:, 1], alpha_pred[:, 1], maxMode=True),
          relDifferenceScalar(h, h_pred, maxMode=False)]
    labels = ["diff alpha0", "diff alpha1", "diff h"]
    utils.plot1D(x, ys, labels, 'differences', log=True)

    ### Compare u and reconstructed u
    [mu, w] = math.qGaussLegendre1D(100)  # Create quadrature
    mBasis = math.computeMonomialBasis1D(mu, 1)  # Create basis

    # Sanity check: reconstruct u with original alpha
    erg = math.reconstructU(alpha, mBasis, w)
    err = relDifference(u, erg)
    erg_neural = math.reconstructU(alpha_pred, mBasis, w)
    err_neural = relDifference(u, erg_neural)
    # plot1D(x, [err, err_neural], ['err', 'err neural'], 'Error in U')

    # plot error in u and error in alpha
    err_alpha = relDifference(alpha_pred, alpha)
    # plot1D(x, [err_alpha, err_neural], ['errAlpha', 'errU'], 'Error in network prediction')

    ### Error Analysis of the reconstruction
    # errorAnalysisU(u, alpha, mBasis, w)
    # errorAnalysisf(alpha, mBasis, w)
    # errorAnalysisUM0()

    c = 0
    # for alpha_orig in alpha:
    # errorAnalysisUM1_normal(alpha, c)
    #    c += 1
    """
    return 0


def errorAnalysisf(alpha, mBasis, w):
    # do error analysis at one for f (L1 error)
    alpha_spec = alpha[25000]
    # disturb alpha in direction e = [0,1] with different stepsize

    alphas = np.repeat(alpha_spec[np.newaxis, :], 50, axis=0)
    alphas_dist = np.copy(alphas)
    delta = np.power(0.5, 20)

    for i in range(0, 50):
        alphas_dist[i, 1] = alphas_dist[i, 1] * (1 + delta)
        delta = delta * 2

    f_err = math.reconstructL1F(alphas_dist - alphas, mBasis, w)
    # f = math.reconstructL1F(alphas, mBasis, w)
    err_alpha = relDifference(alphas_dist, alphas)
    plot1D(range(0, 50), [err_alpha, f_err], ['errAlpha', 'err f'], 'err in f')
    return 0


def errorAnalysisU(u, alpha, mBasis, w):
    # do error analysis at one point
    u_spec = u[25000]
    alpha_spec = alpha[25000]
    # disturb alpha in direction e = [0,1] with different stepsize

    us = np.repeat(u_spec[np.newaxis, :], 50, axis=0)
    alphas = np.repeat(alpha_spec[np.newaxis, :], 50, axis=0)
    alphas_dist = np.copy(alphas)
    delta = np.power(0.5, 20)

    for i in range(0, 50):
        alphas_dist[i, 1] = alphas_dist[i, 1] * (1 + delta)
        delta = delta * 2

    u_rec_spec = math.reconstructU(alphas_dist, mBasis, w)

    err_alpha = relDifference(alphas_dist, alphas)
    err_u = relDifference(u_rec_spec, us)
    utils.plot_1d(range(0, 50), [err_alpha, err_u], ['errAlpha', 'errU'], 'Disturbed_alpha')
    return 0


def errorAnalysisUM0():
    """
    plots u0 over alpha0 in [0,1]
    """
    [mu, w] = math.qGaussLegendre1D(100)  # Create quadrature
    mBasis = math.computeMonomialBasis1D(mu, 0)  # Create basis

    alphas = np.arange(0, 1, 0.001).reshape((1000, 1))
    us = 2 * np.exp(alphas)
    us_rec = math.reconstructU(alphas, mBasis, w)
    utils.plot_1d(alphas, [us, us_rec], ['u', 'u rec'], 'u and u rec', log=False)

    return 0


def errorAnalysisUM1_normal(alphas_orig, count):
    """
    Creates random deviations of a given starting alpha, and plots error of u over the deviation
    """
    # Basis creation
    [mu, w] = math.qGaussLegendre1D(1000)  # Create quadrature
    mBasis = math.computeMonomialBasis1D(mu, 1)  # Create basis

    '''
    # sample the alphas
    alpha_orig = np.asarray([-100, -100])

    devitatio_dir = np.random.rand(1, 2)
    devitatio_norm = np.linalg.norm(devitatio_dir)
    devitatio_dir = devitatio_dir / devitatio_norm
    deltas = np.arange(0, 1, 0.001) * np.linalg.norm(alpha_orig)
    deltas = deltas.reshape(deltas.shape[0], 1)
    alphas = np.repeat(alpha_orig[np.newaxis, :], deltas.shape[0], axis=0)

    alphas = alphas + deltas * devitatio_dir

    # us = 2 * np.exp(alphas)
    us_rec = math.reconstructU(alphas, mBasis, w)
    us_orig = np.repeat(us_rec[0][np.newaxis, :], us_rec.shape[0], axis=0)
    relDiff = relDifference(us_orig, us_rec, maxMode=False)
    plot1D(deltas, [relDiff], ['relErr'], 'relErrU_dir_' + str(devitatio_dir), log=False)
    '''

    ### Same plot as heatmap point cloud for multiple directions
    maxDir = 100
    nDelta = 20
    dTheta = 2 * np.pi / maxDir
    # alpha_orig = np.asarray([-5.210706, 0.280600])
    maxRange = 0.1
    deltas = np.arange(0, maxRange, maxRange / nDelta)
    deltas = deltas.reshape(deltas.shape[0], 1)

    completeAlphas = np.empty((1, 2))
    completeRelDiff = np.empty((1,))

    for j in range(0, alphas_orig.shape[0]):
        alpha_orig = alphas_orig[j, :]
        for i in range(0, maxDir):
            theta = i * dTheta
            devitatio_dir = [np.cos(theta), np.sin(theta)]
            alphas = np.repeat(alpha_orig[np.newaxis, :], deltas.shape[0], axis=0)
            alphas = alphas + deltas * devitatio_dir

            us_rec = math.reconstructL1F(alphas, mBasis, w).reshape(alphas.shape[0], 1)
            us_orig = np.repeat(us_rec[0][np.newaxis, :], us_rec.shape[0], axis=0)
            relDiff = relDifference(us_orig, us_rec, maxMode=False)

            completeAlphas = np.concatenate((completeAlphas, alphas), axis=0)
            completeRelDiff = np.concatenate((completeRelDiff, relDiff), axis=0)

    completeAlphas = completeAlphas[1:]
    completeRelDiff = completeRelDiff[1:]

    # plot everything
    fig = plt.figure()
    ax = fig.add_subplot(111)  # , projection='3d')
    ax.grid(True, linestyle='-', color='0.75')
    x = completeAlphas[:, 0]
    y = completeAlphas[:, 1]
    z = completeRelDiff
    out = ax.scatter(x, y, s=20, c=z, cmap=cm.jet, norm=cm.colors.LogNorm());

    ax.set_title("err f over alpha1 and alpha2", fontsize=14)
    ax.set_xlabel("alpha0", fontsize=12)
    ax.set_ylabel("alpha1", fontsize=12)
    ax.set_ylim([-2, 2])
    ax.set_xlim([-1.5, -0.5])
    # ax.set_xlabel('N1')
    # ax.set_ylabel('N2')
    # ax.set_zlabel('h')
    # pos_neg_clipped = ax.imshow(z)
    cbar = fig.colorbar(out, ax=ax, extend='both')
    # plt.show()
    plt.savefig("figures/ScatterPlots/ScatterM1Error_" + str(count) + ".png")
    plt.close(fig)
    return 0


def relDifferenceScalar(x1, x2, maxMode=True):
    '''
    input: x1,x2: dim ns
    returns: rel difference vector (dim ns)
    '''
    result = 0
    if maxMode:
        result = np.absolute((x1 - x2)) / np.maximum(np.maximum(np.absolute(x1), np.absolute(x2)), 1e-3)
    else:
        result = np.absolute(x1 - x2) / np.absolute(x1)
    return result


def relDifference(x1, x2, maxMode=True):
    '''
    input: x1,x2: dim nsxN
    returns: rel difference vector (dim ns)
    '''
    absDiff = np.linalg.norm((x1 - x2), axis=1, ord=1)
    if maxMode == True:
        normalization = np.maximum(np.linalg.norm(x1, axis=1, ord=1), np.linalg.norm(x2, axis=1, ord=1))
    else:
        normalization = np.linalg.norm(x1, axis=0, ord=1)
    return absDiff / normalization


if __name__ == '__main__':
    main()
