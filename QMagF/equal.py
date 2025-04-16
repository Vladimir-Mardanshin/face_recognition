import numpy as np

np.bool = np.bool_

from preprocessing.embed import main_embed, search_from_image
import torch


def main_equal():
    search_from_image('inputImage/', 'alignedImage/')


if __name__ == '__main__':
    torch.multiprocessing.freeze_support()
    main_equal()
