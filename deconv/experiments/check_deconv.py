import numpy as np
import torch

import matplotlib.pyplot as plt
import seaborn as sns

from deconv.gmm.plotting import plot_covariance
from deconv.gmm.deconv_gmm import DeconvGMM


def check_deconv_gmm(D, K, N, plot=False):

    means = (np.random.rand(K, D) * 20) - 10
    q = (2 * np.random.randn(K, D, D))
    covars = np.matmul(q.swapaxes(1, 2), q)

    qn = (0.5 * np.random.randn(N, K, D, D))
    noise_covars = np.matmul(qn.swapaxes(2, 3), qn)

    X = np.empty((N, K, D))

    for i in range(K):
        X[:, i, :] = np.random.multivariate_normal(
            mean=means[i, :],
            cov=covars[i, :, :],
            size=N
        )
        for j in range(N):
            X[j, i, :] += np.random.multivariate_normal(
                mean=np.zeros(D),
                cov=noise_covars[j, i, :, :]
            )

    data = (
        torch.from_numpy(X.reshape(-1, D).astype(np.float32)),
        torch.from_numpy(noise_covars.reshape(-1, D, D).astype(np.float32))
    )

    gmm = DeconvGMM(K, D, max_iters=1000)
    gmm.fit(data)

    if plot:
        fig, ax = plt.subplots()

        for i in range(K):
            sc = ax.scatter(X[:, i, 0], X[:, i, 1], alpha=0.2, marker='x')
            plot_covariance(
                means[i, :],
                covars[i, :, :],
                ax,
                color=sc.get_facecolor()[0]
            )

        sc = ax.scatter(gmm.means[:, 0], gmm.means[:, 1], marker='+')

        for i in range(K):
            plot_covariance(
                gmm.means[i, :],
                gmm.covars[i, :, :],
                ax,
                color=sc.get_facecolor()[0]
            )

        plt.show()


if __name__ == '__main__':
    sns.set()
    D = 2
    K = 5
    N = 2000
    check_deconv_gmm(D, K, N, plot=True)
