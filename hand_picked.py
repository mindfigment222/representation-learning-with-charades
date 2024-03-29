import torch
import torchvision
from image_folder_with_paths import ImageFolderWithPaths
import torchvision.transforms as T
import csv
import pandas as pd
from utils import visualize_labels
import click
import numpy as np
import os
from tqdm import tqdm
from PIL import Image


@click.command()
@click.option('--root', '-r', default='/media/STORAGE/DATASETS/open-images/', help='Dir where your data sits')
@click.option('--output', '-o', default='./csv_files/handpicked.csv', help='File with hand-picked labeled examples')
def main(root, output):

    data_dir = os.path.join(root, 'train')
    image_ids = [
        [
            'Bicycle/4eb478ec0835cfdd.jpg',
            'Bicycle/020feca9b536f1fe.jpg',
            'Balloon/8ff25f5ccc3b7717.jpg',
            'Cake/429a17e931a48e84.jpg',
            'Ball/978502eef1aa0d13.jpg',

            'Bicycle helmet/a7fa2eca5a25af76.jpg',
            'Computer monitor/1f5cf6e96f0e0690.jpg',
            'Bicycle helmet/0721a8637777a826.jpg',
            'Airplane/0a4abf0a8071b917.jpg',
            'Airplane/6fa1d2c9152bf37f.jpg'
        ],
        [
            'Airplane/0a4abf0a8071b917.jpg',
            'Bowl/0d1c49afcf00e948.jpg',
            'Airplane/6fa1d2c9152bf37f.jpg',
            'Alarm clock/46a0cd25a1f06d65.jpg',
            'Apple/69f3f3889793e68e.jpg',

            'Bowl/9f26942709846de3.jpg',
            'Bicycle helmet/a7fa2eca5a25af76.jpg',
            'Bowl/da95f58bf0813d29.jpg',
            'Bicycle helmet/0721a8637777a826.jpg',
            'Bicycle/4eb478ec0835cfdd.jpg',
        ],
        [
            'Human body/d50b0457d9624258.jpg',
            'Musical instrument/afe96a54fe0610cd.jpg',
            'Dog/c7a81616ee618ccd.jpg',
            'Rifle/24a5c73ad828580e.jpg',
            'Man/fa96d52b52a1ff28.jpg',

            'Man/200907829e4fbe95.jpg',
            'Musical keyboard/5e6b55b7203464b5.jpg',
            'Television/84a1048891bb636c.jpg',
            'Land vehicle/731f10ee0e1d6b70.jpg',
            'Vehicle/7c6e8d04b6e52053.jpg'
        ],
        [
            'Food/0bfcd180b1d67f94.jpg',
            'Man/fa96d52b52a1ff28.jpg',
            'Human body/d50b0457d9624258.jpg',
            'Television/84a1048891bb636c.jpg',
            'Vehicle/7c6e8d04b6e52053.jpg',

            'Dog/c7a81616ee618ccd.jpg',
            'Rifle/24a5c73ad828580e.jpg',
            'Man/200907829e4fbe95.jpg',
            'Giraffe/2647aeeff6ef00be.jpg',
            'Land vehicle/731f10ee0e1d6b70.jpg'
        ],
        [
            'Muffin/966ca10a7907662a.jpg',
            'Musical keyboard/0bff5d8cb2c2a2c9.jpg',
            'Musical instrument/39f032086de8375a.jpg',
            'Musical instrument/ffb2640fb0b5a865.jpg',
            'Musical instrument/ceda9adb4e88fc8e.jpg',

            'Musical instrument/5a31c61d001558c3.jpg',
            'Musical keyboard/0e160088b30f6234.jpg',
            'Musical instrument/7f467f785446806d.jpg',
            'Musical instrument/c929dbfa9cb5aa18.jpg',
            'Musical instrument/2eaca36ed49515ca.jpg'
        ],
        [
            'Human body/9eaffa603797e2dd.jpg',
            'Tree/7fa8b4a5f88946e4.jpg',
            'Bottle/2c9817c8076a3fd4.jpg',
            'Beer/e1b4b8f660967a1a.jpg',
            'Dog/04a27da7e880ddcd.jpg',
            
            'Dog/7cc816e323d254a0.jpg',
            'Giraffe/2647aeeff6ef00be.jpg',
            'Bottle/966d44c47effc043.jpg',
            'Bottle/7e2afdc21926bd14.jpg',
            'Dog/000c4d66ce89aa69.jpg'
        ],
        [
            'Unknown/1ee37d95b6c9a487.jpg',
            'Car/0b75807d9dc2f283.jpg',
            'Dog/7cc816e323d254a0.jpg',
            'Ice cream/75161733278e50d9.jpg',
            'Woman/3c678dab48dd6191.jpg',

            'Car/0c2db401e7e5bf89.jpg',
            'Car/0c9f9b713f229fba.jpg',
            'Human body/9eaffa603797e2dd.jpg',
            'Tree/7fa8b4a5f88946e4.jpg',
            'Dog/04a27da7e880ddcd.jpg'
            
        ],
        [
            'Unknown/5c4658dfb87ef8bf.jpg',
            'Car/0c9f9b713f229fba.jpg',
            'Human body/a013282071756b84.jpg',
            'Human body/3529ed57057b4d08.jpg',
            'Human body/e2eb9b5eca496b1e.jpg',
            
            
            'Human body/983255791f113009.jpg',
            'Human body/7772aaad3a1b72cc.jpg',
            'Human body/ada6444710b9b1c4.jpg',
            'Human body/3680bce5527b2efe.jpg',
            'Human body/4097eda463e6631c.jpg'
        ],
        [
            'Human body/9efc246660ca5253.jpg',
            'Television/84a1048891bb636c.jpg',
            'Land vehicle/731f10ee0e1d6b70.jpg',
            'Human body/3097b67f07b8f8e8.jpg',
            'Apple/69f3f3889793e68e.jpg',

            'Organ (Musical Instrument)/72ac183680821ed4.jpg',
            'Human body/1806f5b35279d7a5.jpg',
            'Human body/973c75e13ab55347.jpg',
            'Human body/969af219a0438f06.jpg',
            'Human body/434166afed88f797.jpg'
        ],
        [
            'Computer monitor/1f8d2f13a6cd1206.jpg',
            'Human body/9efc246660ca5253.jpg',
            'Television/84a1048891bb636c.jpg',
            'Land vehicle/731f10ee0e1d6b70.jpg',
            'Human body/3097b67f07b8f8e8.jpg',

            'Apple/69f3f3889793e68e.jpg',
            'Organ (Musical Instrument)/72ac183680821ed4.jpg',
            'Human body/1806f5b35279d7a5.jpg',
            'Human body/973c75e13ab55347.jpg',
            'Human body/969af219a0438f06.jpg'
        ],
        [
            'Building/0c5458ea3583233b.jpg',
            'Human body/a3ede9354b3f5cd5.jpg',
            'Human body/76571813b79399e5.jpg',
            'Human body/3097b67f07b8f8e8.jpg',
            'Ice cream/75161733278e50d9.jpg',
            
            'Human body/68b5e7af876a3062.jpg',
            'Human body/434166afed88f797.jpg',
            'Human body/226f45719bfa23b3.jpg',
            'Human body/1806f5b35279d7a5.jpg',
            'Unknown/1ee37d95b6c9a487.jpg' 
        ]
    ]

    topics = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    choices = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    transform = T.Compose([
                           T.Resize(size=224),
                           T.CenterCrop(size=224)
    ])

    # print([print(im_id) for im_batch in image_ids for im_id in im_batch])

    get_images = lambda im_batch: [transform(Image.open(os.path.join(data_dir, im_id))) for im_id in im_batch]

    images = list(map(get_images, image_ids))

    print(len(images), len(images[0]), type(images[0][0]))

    # Column names for validation.csv file
    context = [''.join(['Context', str(i)]) for i in range(5)]
    source = [''.join(['Source', str(i)]) for i in range(5)]
    columns = [*context, *source, 'Topic', 'Weights']

    handpicked_dir = os.path.join(root, 'hand-picked')
    try:
        os.makedirs(handpicked_dir)
        # print('Created dir: {}'.format(dir_path))
    except FileExistsError:
        print('{} already exists!'.format(handpicked_dir))

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for i in tqdm(range(len(topics))):
            example = images[i]
            part_paths = image_ids[i]
            topic = topics[i]
            choice = choices[i]

            row = [*part_paths, choice, topic]
            
            row_dict = dict(zip(columns, row))
            writer.writerow(row_dict)
            
            save_f = os.path.join(root, 'hand-picked', 'example' + str(i + 1))

            # Create image of our particular examples to help us visually inspect it
            # and decide upon correct label we want to assign to it
            visualize_labels(example, i + 1, [topic], [choice], show=False, save_f=save_f)


if __name__ == '__main__':
    main()
