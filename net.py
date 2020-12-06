import torch
from torch import nn


class MancNet(nn.Module):
    """" Mancala """

    def __init__(self):
        super(MancNet, self).__init__()
        self.d11 = nn.Linear(14, 36)
        self.d12 = nn.Linear(36, 36)
        self.d13 = nn.Linear(36, 36)
        self.output = nn.Linear(36, 14)

    def forward(self, x):
        x = self.d11(x)
        x = torch.relu(x)
        x = self.d12(x)
        x = torch.relu(x)
        x = self.d13(x)
        x = torch.relu(x)
        x = self.output(x)
        x = torch.sigmoid(x)
        return x


class TTTNet(nn.Module):
    """ Tic Tac Toe """

    def __init__(self):
        super(TTTNet, self).__init__()
        self.d11 = nn.Linear(9, 36)
        self.d12 = nn.Linear(36, 36)
        self.output = nn.Linear(36, 9)

    def forward(self, x):
        x = self.d11(x)
        x = torch.relu(x)
        x = self.d12(x)
        x = torch.relu(x)
        x = self.output(x)
        x = torch.sigmoid(x)
        return x
