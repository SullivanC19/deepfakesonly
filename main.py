import numpy as np
import matplotlib.pyplot as plt

# import torch
from data.preprocessing import CustomDataset
from torch.utils.data import DataLoader
from torchvision import transforms
from models.cnn import cnn_model
from train.trainer import train, base_svm

def main():
  # Define the path to your data csv 
  data_folder = './140k-real-and-fake-faces'
  data_set = 'dev_train.csv'

  # Define the transformations to apply to the images
  transform = transforms.Compose([
      transforms.Resize((256, 256)),  # Resize the image to 256x256
      transforms.ToTensor(),  # Convert PIL image to tensor
      transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalize image pixels
  ])

  # Create an instance of your custom dataset
  custom_dataset = CustomDataset(data_folder, data_set, transform=transform)

  # Create a DataLoader to load the data in batches
  batch_size = 1005
  data_loader = DataLoader(custom_dataset, batch_size=batch_size, shuffle=True)

  # Iterate over the data loader to access batches of preprocessed images
  for batch_idx, batch in enumerate(data_loader):
    # Process each batch as needed
    # batch is a tensor of shape (batch_size, channels, height, width)
    # For example, you can perform some operations on the batch like printing its shape
    print(f"Batch {batch_idx + 1} shape:", batch[0].shape, len(batch[1]))
    bdev_x = batch[0].detach().numpy()
    bdev_x = bdev_x.reshape((bdev_x.shape[0], bdev_x.shape[1]*bdev_x.shape[2]*bdev_x.shape[3]))
    bdev_y = batch[1].detach().numpy()

    # # Convert the batch tensor to a NumPy array
    # batch_np = batch[0].numpy()

    # # Iterate over images in the batch
    # for i in range(len(batch_np)):
    #   image_np = np.transpose(batch_np[i], (1, 2, 0))  # Change from (C, H, W) to (H, W, C)
    #   # Display the image using matplotlib
    #   plt.imshow(image_np)
    #   plt.title(f"Batch {batch_idx + 1}, Image {i + 1}")
    #   plt.axis('off')  # Turn off axis labels
    #   plt.show()
    #   print('label: ', batch[1][i])
    
    # Optionally, break the loop after processing a few batches
    # if batch_idx == 4:
      # using batch 5 as dev set (0 indexing)
      # dev_x = batch[0].to(torch.float32).requires_grad_(True)
      # dev_y = batch[1].to(torch.float32).requires_grad_(True)
      # break

  # dev_data = TensorDataset(dev_x, dev_y)

  print('Starting baseline')
  b_acc = base_svm(bdev_x, bdev_y)
  print('Starting training')
  channel_dims = [3, 128, 128, 64, 32, 1]
  losses, accuracies = train(cnn_model(channel_dims, 2), custom_dataset)
  
  plt.title("Training loss")
  plt.plot(losses)
  plt.xlabel("Iteration")
  plt.grid(linestyle='--', linewidth=0.5)
  plt.show()

  plt.title("Training accuracy")
  plt.plot(np.arange(1, len(accuracies)+1), b_acc*np.ones(len(accuracies)), '--', label='baseline')
  plt.plot(np.arange(1, len(accuracies)+1), accuracies, label='CNN')
  plt.xlabel("Epoch")
  plt.grid(True)
  plt.legend(loc='best')
  plt.show()


if __name__ == '__main__':
  main()