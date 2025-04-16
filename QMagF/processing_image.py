import numpy as np

np.bool = np.bool_

from preprocessing.align import main_align
from preprocessing.embed import main_embed
from multiprocessing import freeze_support


if __name__ == '__main__':

    main_align('alignedImages/', 'static/')
    freeze_support()
    main_embed('mainEmbeddings/', 'alignedImages/')
