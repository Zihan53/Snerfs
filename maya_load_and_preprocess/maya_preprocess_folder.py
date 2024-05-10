import numpy as np
import torch
import os
import json
import shutil


from PIL import Image


class MayaPreprocessorFolder:
    def __init__(self):
        self.focal = 30
        
    def split_train_test(train_test_ratio):
        
        for image in range(618):
            curr_file_path = 'data/sofa/' + str(image) + '.png'
            new_file_path = 'data/sofa/'

            if random.uniform(0, 1) >= train_test_ratio:
                new_file_path += 'test'
            else:
                new_file_path += 'train'
            shutil.move(curr_file_path, new_file_path)


    def load_train_data(self, path):
        
        train_images, train_poses = self.preprocess(path, 'train')
        self.H, self.W = train_images.shape[1:3] 
        return train_images, train_poses

    def load_test_data(self, path):
        test_images, test_poses = self.preprocess(path, 'test')
        return test_images, test_poses

    def preprocess(self, path, mode):
        path = os.path.join(path, mode)
        images = []

        for file in os.listdir(path):
            if file.endswith('.png'):
                img_path = os.path.join(path, file)
                with Image.open(img_path) as img:
                    img_array = np.array(img.convert('RGB')).astype(np.float32)
                    img_array /= 255.0
                    images.append(img_array)
        images_tensor = torch.tensor(np.stack(images), dtype=torch.float32)

        pose_path = os.path.join(path, f'transforms_{mode}.json')
        with open(pose_path, 'r') as file:
            data = json.load(file)
        poses = np.array([frame['transform_matrix'] for frame in data['frames']])
        poses_tensor = torch.tensor(poses, dtype=torch.float32)

        return images_tensor, poses_tensor

    
        

        
mpf = MayaPreprocessorFolder()
mpf.split_train_test()