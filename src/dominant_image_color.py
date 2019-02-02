from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

NUM_CLUSTERS = 5


def dominant_color(image_path):
    """
    Adapted from:
    https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
    """
    image = Image.open(image_path)
    image = image.resize((150, 150))
    ar = np.asarray(image)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    return tuple(peak)
