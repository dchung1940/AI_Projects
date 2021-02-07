# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F

np.random.seed(0)
torch.manual_seed(0)

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        """
        super(NeuralNet, self).__init__()
        self.lrate = lrate
        self.in_size = in_size
        self.out_size = out_size
        self.loss_fn = loss_fn
        # self.fc1 = torch.nn.Linear(self.in_size,64)
        # self.relu1 = torch.nn.LeakyReLU()
        # self.fc2 = torch.nn.Linear(64,32)
        # self.relu2 = torch.nn.LeakyReLU()
        # self.fc3 = torch.nn.Linear(32,self.out_size)
        self.conv1 = torch.nn.Conv2d(3,6,5)
        self.pool = torch.nn.MaxPool2d(2,2)
        self.conv2 = torch.nn.Conv2d(6,16,5)
        self.fc1 = torch.nn.Linear(16*5*5,128)
        self.fc2 = torch.nn.Linear(128,64)
        self.fc3 = torch.nn.Linear(64,10)
        # self.relu2 = torch.nn.LeakyReLU()
        # self.fc4 = torch.nn.Linear(pit)

        # self.sigmoid = torch.nn.Sigmoid()
        self.graph = torch.nn.Sequential(self.fc1,self.conv1,self.fc2,self.conv2,self.fc3)
        self.optimizer = optim.Adam(self.graph.parameters(),lr = self.lrate,weight_decay = .0001)
        # self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size = 30, gamma = 0.1)
        self.set_parameters(list(self.graph.parameters()))

    def set_parameters(self, params):
        """ Set the parameters of your network
        @param params: a list of tensors containing all parameters of the network
        """
        self.parameters_ = []
        for i in range(len(params)):
            for j in range(len(params[i])):
                self.parameters_.append(params[i][j])

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters_


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        x = x.view(-1,3,32,32)
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1,16*5*5)
        x=F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        # criterion = self.loss_fn
        self.optimizer.zero_grad()
        outputs = self.forward(x)
        loss = self.loss_fn(outputs,y)
        loss.backward()
        self.optimizer.step()
        return loss.item()



def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of epochs of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    net = NeuralNet(.001, torch.nn.CrossEntropyLoss(),3072,2 )
    yhats = np.zeros(len(dev_set))
    losses = []
    trainset = torch.utils.data.TensorDataset(train_set,train_labels)
    trainloader = torch.utils.data.DataLoader(trainset,batch_size)
    for epoch in range(10):
        running_loss = 0.0
        for i,data in enumerate(trainloader,0):
            inputs, labels = data
            running_loss += net.step(inputs, labels)
        losses.append(running_loss)
        # net.scheduler.step()
    correct =0
    total =0
    count = 0
    for data in dev_set:
        # print(data)
        images = data
        outputs = net(images)
        # _, predicted = torch.max(outputs.data,0)
        print(outputs)
        outputs = outputs.detach()
        predicted = np.argmax(outputs.detach())
        total += labels.size(0)
        correct += (predicted).sum().item()
        # print(predicted)
        yhats[count] = predicted
        # print(correct)
        count +=1

    return losses,yhats,net
