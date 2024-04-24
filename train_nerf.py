import torch
import argparse
import json
import numpy as np
import imageio
import os

from preprocess import Preprocessor
from utils import visualize, utils
from renderer.nerf_renderer import NRFRenderer
from tqdm import tqdm


if __name__ == '__main__':
    # TODO add argparse
    device = utils.get_device()
    print("Using device: ", device)
    
    parser = argparse.ArgumentParser(description="nerf")
    parser.add_argument(
        "--config", type=str, default="configs/default.json", help="Config file"
    )
    parser.add_argument(
        "--test", default=False, action="store_true"
    )
    args = parser.parse_args()

    if args.config is not None:
        config = json.load(open(args.config, "r"))
        for key in config:
            args.__dict__[key] = config[key]
 
    os.makedirs(os.path.join(args.out_dir, 'ckpt'), exist_ok=True)
    os.makedirs(os.path.join(args.out_dir, 'test_results'), exist_ok=True)

    # ---------------------------------------------------------------------

    # Load Data
    preprocessor = Preprocessor()
    preprocessor.load_new_data(args.data_path)
    split_params = (True, 100)
    train_images, train_poses, test_images, test_poses = preprocessor.split_data(split_params, randomize=False)
    # visualize.plot_images(test_images[1].numpy())

    # Set metric
    if args.metric == "psnr":
        metric = utils.psnr
    elif args.metric == "ssim":
        metric = utils.ssim
    else:
        raise ValueError(f"Unsupported metric '{args.metric}'. Expected 'psnr' or 'ssim'.")

    # pred = test_images[1]
    # target = train_images[1]
    # print(utils.apply_metric(pred, target, metric))

    NerfRenderer = NRFRenderer().to(device)
    optimizer = torch.optim.Adam(NerfRenderer.parameters(), lr=1e-3)
    start_epoch = 0

    # Load saved model
    if hasattr(args, 'model_path'):
        checkpoint = torch.load(args.model_path, map_location=device)
        NerfRenderer.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1


    if not args.test:
        NerfRenderer.train()
        for epoch in tqdm(range(start_epoch, args.num_epochs)):
            for img, pose in zip(train_images, train_poses):
                optimizer.zero_grad()
                rays = NerfRenderer.get_rays(preprocessor.H, preprocessor.W, preprocessor.focal, pose.to(device))

                rgb, depth = NerfRenderer(rays)

                loss = utils.mse_loss(rgb, img.to(device))

                loss.backward()

                # for param in NerfRenderer.parameters():
                #     print(param.grad)

                optimizer.step()

            print(f'Epoch {epoch}: Loss: {loss.item()}')

        # Save model for training mode
        utils.save_model(args.num_epochs - 1, NerfRenderer, optimizer, os.path.join(args.out_dir, 'ckpt', "model.ckpt"))

    # test
    NerfRenderer.eval()
    for idx, (img, pose) in enumerate(zip(test_images, test_poses)):
        rays = NerfRenderer.get_rays(preprocessor.H, preprocessor.W, preprocessor.focal, pose.to(device))
        rgb, depth = NerfRenderer(rays)

        visualize.save_result_comparison(rgb.detach().cpu().numpy(), img.numpy(), os.path.join(args.out_dir, 'test_results', f"{idx}.jpg"))







