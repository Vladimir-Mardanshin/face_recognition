import os
import tqdm
import numpy as np
import cv2
import torch
import requests
import torchvision.transforms
from torch.utils import data
from collections import namedtuple

from preprocessing.align import main_align
from utils.files import list_all_files
from preprocessing.magface.network_inf import builder_inf

np.bool = np.bool_


class ImgDataset(data.Dataset):
    def __init__(self, filenames, transform):
        super(ImgDataset, self).__init__()
        self.filenames = filenames
        self.transform = transform

    def __getitem__(self, item):
        path = self.filenames[item]
        img = cv2.imread(path)
        return self.transform(img), path

    def __len__(self):
        return len(self.filenames)


def send_to_server(name: str, embedding: np.ndarray):
    url = "http://127.0.0.1:5000/add"
    payload = {
        "name": name,
        "embedding": embedding.tolist()
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[✓] Sent embedding for {name}")
        else:
            print(f"[!] Failed to send {name}: {response.text}")
    except Exception as e:
        print(f"[!] Exception for {name}: {e}")


def main_embed(source_dir, result_dir, model_path='_models/magface_models/magface_epoch_00025.pth'):
    main_align(result_dir, source_dir)
    Args = namedtuple('Args', ['arch', 'resume', 'embedding_size', 'cpu_mode'])
    args = Args('iresnet100', model_path, 512, True)
    model = builder_inf(args)
    model = torch.nn.DataParallel(model)
    model.eval()

    trans = torchvision.transforms.ToTensor()
    filenames = list_all_files(result_dir)
    dataset = ImgDataset(filenames, trans)
    loader = data.DataLoader(dataset, batch_size=64, num_workers=4, pin_memory=True, shuffle=False)

    with torch.no_grad():
        for input_, paths in tqdm.tqdm(loader):
            input_ = input_.to('cpu')
            embeddings = model(input_).to('cpu').numpy()

            for emb, path in zip(embeddings, paths):
                name = os.path.splitext(os.path.basename(path))[0].split('_')[0]
                send_to_server(name, emb)

    filenames = list_all_files(source_dir)
    for file in filenames:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Could not delete {file}: {e}")

    filenames = list_all_files(result_dir)
    for file in filenames:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Could not delete {file}: {e}")


def search_from_image(source_dir, result_dir, model_path='_models/magface_models/magface_epoch_00025.pth',
                      return_result=False):
    main_align(result_dir, source_dir)

    Args = namedtuple('Args', ['arch', 'resume', 'embedding_size', 'cpu_mode'])
    args = Args('iresnet100', model_path, 512, True)
    model = builder_inf(args)
    model = torch.nn.DataParallel(model)
    model.eval()

    trans = torchvision.transforms.ToTensor()
    filenames = list_all_files(result_dir)

    dataset = ImgDataset(filenames, trans)
    loader = data.DataLoader(dataset, batch_size=1, num_workers=1, pin_memory=True, shuffle=False)

    results = []

    try:
        with torch.no_grad():
            for input_, paths in loader:
                input_ = input_.to('cpu')
                embedding = model(input_).to('cpu').numpy()[0]

                url = "http://127.0.0.1:5000/search"
                payload = {"embedding": embedding.tolist()}
                response = requests.post(url, json=payload)

                result = {"path": paths[0], "match_name": None, "score": 0.0}
                if response.status_code == 200:
                    response_json = response.json()
                    result.update(response_json)

                    if result.get("match_name") and result["score"] > 0.5:
                        print(f"На фото ({paths[0]}): {result['match_name']} (score: {result['score']:.2f})")
                    else:
                        print(f"Человек на фото ({paths[0]}) не распознан")

                results.append(result)
    finally:
        for folder in [source_dir, result_dir]:
            for file in list_all_files(folder):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Не удалось удалить {file} из {folder}: {e}")

    return results if return_result else None
