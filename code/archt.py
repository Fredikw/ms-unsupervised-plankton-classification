import torch.nn as nn
import torch.nn.init as init
import torchvision.models as models

"""
Feed Forward Neural Network

"""
class NeuralNet(nn.Module):
    def __init__(self, num_classes):
        super(NeuralNet, self).__init__()

        # Fully connected layer with 428 * 428 input neurons and 1200 output neurons
        self.fc1 = nn.Linear(in_features=428*428, out_features=1200)
        self.fc2 = nn.Linear(in_features=1200, out_features=1200)
        # Add output layer of size 10 
        self.fc3 = nn.Linear(in_features=1200, out_features=num_classes)
        
        # Initialize the weights of the layer
        # TODO Consider other initializations, e.g torch.nn.init.kaiming_uniform_, torch.nn.init.xavier_uniform_, torch.nn.init.normal_, torch.nn.init.constant_
        # Improved performance using init.kaiming_normal_(self.fc1.weight, nonlinearity='relu') on MNIST
        init.xavier_uniform_(self.fc1.weight)
        init.xavier_uniform_(self.fc2.weight)
        init.xavier_uniform_(self.fc3.weight)
        
        # Add batch normalization layer with 1200 neurons
        # TODO Consider different values for eps
        self.bn1 = nn.BatchNorm1d(num_features=1200, eps=2e-5)
        self.bn2 = nn.BatchNorm1d(num_features=1200, eps=2e-5)
        
        # Add first ReLU activation function
        self.relu = nn.ReLU()

    # Define the forward pass through the network
    def forward(self, x):

        x = self.relu(self.bn1(self.fc1(x)))
        x = self.relu(self.bn2(self.fc2(x)))
        
        x = self.fc3(x)

        return x

"""
Convolutional Neural Network

"""
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        # self.conv2 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, padding=1)

        # Define max pooling layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
    
        # Add batch normalization layers
        self.conv_bn1 = nn.BatchNorm2d(num_features=16, eps=2e-5)
        # self.conv_bn2 = nn.BatchNorm2d(16, eps=2e-5)
        self.conv_bn3 = nn.BatchNorm2d(num_features=16, eps=2e-5)
        
        # Dropout layer
        self.dropout = nn.Dropout(p=0.5)

        # Fully connected layers
        self.fc1 = nn.Linear(in_features=107*107*16, out_features=1024)
        # self.fc2 = nn.Linear(in_features=1024, out_features=1024)
        self.fc3 = nn.Linear(in_features=1024, out_features=num_classes)

        # Initialize the weights of the layer
        # TODO Consider other initializations, e.g torch.nn.init.kaiming_uniform_, torch.nn.init.xavier_uniform_, torch.nn.init.normal_, torch.nn.init.constant_
        init.kaiming_normal_(self.fc1.weight, nonlinearity='relu')
        # init.xavier_uniform_(self.fc2.weight)
        init.xavier_uniform_(self.fc3.weight)

        # Add batch normalization layer with 1200 neurons
        # TODO Consider different values for eps
        self.fc_bn1 = nn.BatchNorm1d(num_features=1024, eps=2e-5)
        # self.fc_bn2 = nn.BatchNorm1d(512, eps=2e-5)
        
        # Add first ReLU activation function
        self.relu = nn.ReLU()

    def forward(self, x):

        x = self.pool(self.conv_bn1(self.conv1(x)))
        # x = self.pool(self.conv_bn2(self.conv2(x)))
        x = self.conv_bn3(self.conv3(x))

        # Flatten the output for the fully connected layers
        x = x.view(-1, 107*107*16)  # -1 is a placeholder for the batch size
        
        x = self.relu(self.fc_bn1(self.fc1(x)))
        # x = self.relu(self.fc_bn2(self.fc2(x)))
        x = self.fc3(self.dropout(x))
        
        return x

"""
DL model based on:
https://web.archive.org/web/20210716204136id_/https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/handle/11250/2730780/33-3_saad.pdf?sequence=2

# TODO Implement None fileds
"""
class AILARONNet(nn.Module):
    def __init__(self, num_classes):
        super(AILARONNet, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)

        # Define max pooling layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
    
        # Add batch normalization layers
        self.conv_bn1 = nn.BatchNorm2d(64, eps=2e-5)
        self.conv_bn2 = nn.BatchNorm2d(128, eps=2e-5)
        self.conv_bn3 = nn.BatchNorm2d(256, eps=2e-5)
        self.conv_bn4 = nn.BatchNorm2d(256, eps=2e-5)
        self.conv_bn5 = nn.BatchNorm2d(256, eps=2e-5)

        # Fully connected layers
        # TODO set in_features
        self.fc1 = nn.Linear(in_features=None, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=256)
        self.fc3 = nn.Linear(in_features=256, out_features=256)
        self.fc4 = nn.Linear(in_features=256, out_features=num_classes)

        # Initialize the weights of the layer
        # TODO Consider other initializations, e.g- torch.nn.init.xavier_uniform_, torch.nn.init.normal_, torch.nn.init.constant_
        init.xavier_uniform_(self.fc1.weight)
        init.xavier_uniform_(self.fc2.weight)
        init.xavier_uniform_(self.fc3.weight)
        init.xavier_uniform_(self.fc4.weight)

        # Add batch normalization layer with 1200 neurons
        # TODO Consider different values for eps
        # TODO set num_features
        self.fc_bn1 = nn.BatchNorm1d(num_features=None, eps=2e-5)
        self.fc_bn2 = nn.BatchNorm1d(num_features=256, eps=2e-5)
        self.fc_bn3 = nn.BatchNorm1d(num_features=256, eps=2e-5)
        
        # Add first ReLU activation function
        self.relu = nn.ReLU()

    def forward(self, x):
        107*107*128
        x = self.pool(self.conv_bn1(self.conv1(x)))
        x = self.pool(self.conv_bn2(self.conv2(x)))
        x = self.pool(self.conv_bn3(self.conv3(x)))
        x = self.pool(self.conv_bn4(self.conv4(x)))
        x = self.pool(self.conv_bn5(self.conv5(x)))

        # Flatten the output for the fully connected layers
        # TODO Set num_features
        x = x.view(-1, None)  # -1 is a placeholder for the batch size
        
        x = self.relu(self.fc_bn1(self.fc1(x)))
        x = self.relu(self.fc_bn2(self.fc2(x)))
        x = self.relu(self.fc_bn3(self.fc3(x)))
        x = self.fc4(x)

        return x

"""

"""
def get_model(model_name: str, num_classes=None):

    if model_name == "neuralnet":
        model = NeuralNet(num_classes=num_classes)
    
    elif model_name == "cnn":
        model = CNN(num_classes=num_classes)

    elif model_name == "AILARONNet":
        model = AILARONNet(num_classes=num_classes)
    
    elif model_name == "resnet18":
        # Residual Network
        model = models.resnet18()
        # Change the first layer to accept grayscale images
        model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False) # Setting the bias term to false in the first convolutional layer can improve performance, particularly for large-scale image classification tasks.
        # Modify the final fully connected layer to have num_classes output classes
        model.fc = nn.Linear(in_features=512, out_features=num_classes)
        
#    elif model_name == "alexnet":
#        model = models.alexnet()
#        # Modify the first layer to accept grayscale images
#        model.features[0]   = nn.Conv2d(1, 64, kernel_size=11, stride=4, padding=2)
#        # Modify the last layer to output the correct number of classes
#        model.classifier[6] = nn.Linear(4096, num_classes)

    elif model_name == "vgg11":
       # Visual Geometry Group
        model = models.vgg11()
        # Modify the input layer to accept grayscale images
        model.features[0] = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        # Modify the last layer to output the correct number of classes
        model.classifier[6] = nn.Linear(4096, num_classes)

    elif model_name == "densenet":
        model = models.densenet121()
        # Modify the input layer to accept grayscale images
        model.features[0] = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        # Modify the last layer to output the correct number of classes
        model.classifier = nn.Linear(in_features=1024, out_features=num_classes)
    
    elif model_name == "inception_v3":
        model = models.inception_v3()
        # Modify the input layer to accept grayscale images
        model.Conv2d_1a_3x3.conv = nn.Conv2d(1, 32, kernel_size=3, stride=2, bias=False)
        # Remove the auxiliary outputs
        model.aux_logits = False
        # Modify the last layer to output the correct number of classes
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
#        # Initialize weights
#        for _, module in model.named_modules():
#            if isinstance(module, nn.Linear):
#                init.xavier_uniform_(module.weight)

#        # If you also want to initialize the bias to zero
#        if module.bias is not None:
#            init.constant_(module.bias, 0)

    else:
        raise NotImplemented

    print(f"Model specifications: {model}")
    return model