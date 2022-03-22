import numpy as np
import random
import matplotlib.pyplot as plt

# def gen_random_offset(offset=0.005):
#     '''
#     Generate random offset in lat/long degrees
#     '''
#     return (np.random.random_sample() - np.random.random_sample()) * offset  # (-0.005,0.005)


def genRoi(lon, lat, length=0.01, w_offset=0.5):
    '''

    Generate an ROI rectangle with upperleft coord and bottomright coord from a centroid
    length unit in deg

    '''
    offset = random.uniform(-length / 2, length / 2) * w_offset

    # (long1,lat1): up left corner (-0.01,0)
    lat1 = lat + offset - length / 2
    lon1 = lon + offset - length / 2  # *2.67   #longitude correction

    # (long2,lat2): bottom right corner (0,0.01)
    lat2 = lat + offset + length / 2
    lon2 = lon + offset + length / 2  # *2.67   #longitude correction

    return lon1, lat1, lon2, lat2


def normalise(arr):
    '''

    Normalise an np.array to 0-1

    '''
    numerator = arr - arr.min()
    denominator = arr.max() - arr.min()
    return (numerator / denominator)


def padArr(img, side_len=280):
    '''

    pad nparrays to a fixed shape (square)

    '''
    if img.ndim == 3:  # if the image is rgb
        # print ('padding an rgb image')
        shape = np.zeros((side_len, side_len, 3))
        for channel in range(img.shape[-1]):
            shape[:img.shape[0], :img.shape[1], channel] = img[..., channel]

    else:  # 1 channel - label
        # print ('padding a label image')
        shape = np.zeros((side_len, side_len))
        shape[:img.shape[0], :img.shape[1]] = img

    return shape


def onehotLabels(ls):
    '''

    convert numerical labels to one-hot encoded labels

    '''
    out = np.zeros((ls.shape[0], ls.shape[1], ls.shape[2], 2))  # split background and forground
    for i in range(ls.shape[0]):
        out[i, ..., 0] = ~ls[i, ..., -1]  # not label
        out[i, ..., 1] = ls[i, ..., -1]  # label
    return out.astype('bool')


def plotim(**images):
    """PLot images in one row."""

    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
    plt.show()


def CropAndPad(arr, target_size):
    '''

    resize a 3d array to a fixed size with crop and pad

    '''
    def f(a): return (abs(a)+a)/2  # negative values become zero

    hpad = f(target_size[0]-arr.shape[0])
    wpad = f(target_size[1]-arr.shape[1])

    pad = np.pad(arr, ((0, int(hpad)), (0, int(wpad)), (0, 0)))
    out = pad[:target_size[0], :target_size[1], :]
    return out
