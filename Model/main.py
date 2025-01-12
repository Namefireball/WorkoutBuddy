import argparse
import torch
from torchvision import transforms
from Model_Config import Config, parse_config_file, config_file
from model import BaseCNN
from ConfigCNN import DynamicCNN
from Train import Train
from CustomLoader import DataSet
from torch.utils.data import DataLoader
from memory_profiler import profile

@profile
def main(args):
    config = Config()
    configuration = parse_config_file(config_file)
    # Define transforms
    transform = transforms.Compose([transforms.ToTensor(),])
    # Create dataset and dataloader
    dataset = DataSet(config.data_folder, config.label_csv, transform=transform)
    dataloader = DataLoader(dataset, batch_size=config.batch_size, shuffle=True, collate_fn=DataSet.collate_fn)
    model = DynamicCNN(configuration, 8)
    # Create optimizer and criterion
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = torch.nn.BCEWithLogitsLoss()
    print(model)
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        print("using cuda")
    else:
        print("using cpu")

    # Create trainer
    trainer = Train(model, dataloader, criterion, optimizer, device)

    if args.train:
        trainer.train_model(config.num_epochs)
    elif args.validate:
        pass
    elif args.fast:
        pass
    elif args.accurate:
        pass
    else:
        print("no arguments given")
        trainer.train_model(config.num_epochs)


if __name__ == '__main__':
    config = Config()
    config_file_path = 'CNN_config.cfg'
    parser = argparse.ArgumentParser(description='Training or Validation')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--validate', action='store_true', help='Validate the model')
    parser.add_argument('--fast', action='store_true', help='Fast training mode')
    parser.add_argument('--accurate', action='store_true', help='Accurate training mode')
    args = parser.parse_args()
    main(args)
