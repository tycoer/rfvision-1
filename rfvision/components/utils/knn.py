import torch


def KNN(train_x, test_x,  k):

    m = test_x.size(0)
    n = train_x.size(0)

    # cal Eud distance mat
    print("cal dist matrix")
    xx = (test_x**2).sum(dim=1,keepdim=True).expand(m, n)
    yy = (train_x**2).sum(dim=1, keepdim=True).expand(n, m).transpose(0,1)

    dist_mat = xx + yy - 2*test_x.matmul(train_x.transpose(0,1))
    mink_idxs = dist_mat.argsort(dim=-1)
    return mink_idxs[:, :k], dist_mat

def euclidean_dist(x, y):
    """
    Args:
      x: pytorch Variable, with shape [m, d]
      y: pytorch Variable, with shape [n, d]
    Returns:
      dist: pytorch Variable, with shape [m, n]
    """
    assert len(x.shape) == len(y.shape) == 2
    m, n = x.size(0), y.size(0)
    xx = (x**2).sum(1, keepdim=True).expand(m, n)
    yy = (y**2).sum(1, keepdim=True).expand(n, m).T
    dist_mat = xx + yy - 2 * x.matmul(y.T)
    return dist_mat.T

def knn_search(x, y, k=1):
    assert k > 0, 'k cannot less than 0'
    dist_mat = euclidean_dist(x, y)
    index = dist_mat.argsort(dim=-1)[:, :k]
    return index

if __name__ == '__main__':
    k = 5
    x = torch.rand((5, 3))
    y = torch.rand((2, 3))

    # knn_search is cuda-supported
    index = knn_search(x, y, k)

    # KNNSearch is not cuda-supported
    from open3d.ml.torch.layers import KNNSearch
    nsearch = KNNSearch()
    index_o3d = nsearch(x, y, k).neighbors_index.reshape(y.shape[0], k)
