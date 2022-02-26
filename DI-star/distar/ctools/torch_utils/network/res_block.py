"""
Copyright 2020 Sensetime X-lab. All Rights Reserved

Main Function:
    1. build ResBlock: you can use this classes to build residual blocks
"""
import torch.nn as nn

from .nn_module import conv2d_block, fc_block
from .normalization import build_normalization


class ResBlock(nn.Module):
    r'''
    Overview:
        Residual Block with 2D convolution layers, including 2 types:
            basic block:
                input channel: C
                x -> 3*3*C -> norm -> act -> 3*3*C -> norm -> act -> out
                \__________________________________________/+
            bottleneck block:
                x -> 1*1*(1/4*C) -> norm -> act -> 3*3*(1/4*C) -> norm -> act -> 1*1*C -> norm -> act -> out
                \_____________________________________________________________________________/+

    Interface:
        __init__, forward
    '''

    def __init__(self, in_channels, activation=nn.ReLU(), norm_type='BN', res_type='basic'):
        r"""
        Overview:
            Init the Residual Block

        Arguments:
            - in_channels (:obj:`int`): Number of channels in the input tensor
            - activation (:obj:`nn.Module`): the optional activation function
            - norm_type (:obj:`str`): type of the normalization, defalut set to batch normalization,
                                      support ['BN', 'IN', 'SyncBN', None]
            - res_type (:obj:`str`): type of residual block, support ['basic', 'bottleneck'], see overview for details
        """
        super(ResBlock, self).__init__()
        self.act = activation
        assert res_type in ['basic',
                            'bottleneck'], 'residual type only support basic and bottleneck, not:{}'.format(res_type)
        self.res_type = res_type

        self.conv1 = conv2d_block(in_channels, in_channels, 3, 1, 1, activation=self.act, norm_type=norm_type)
        self.conv2 = conv2d_block(in_channels, in_channels, 3, 1, 1, activation=None, norm_type=norm_type)

    def forward(self, x):
        r"""
        Overview:
            return the redisual block output

        Arguments:
            - x (:obj:`tensor`): the input tensor

        Returns:
            - x(:obj:`tensor`): the resblock output tensor
        """
        residual = x
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.act(x + residual)
        return x


class ResFCBlock(nn.Module):
    r'''
    Overview:
        Residual Block with 2 fully connected block
        x -> fc1 -> norm -> act -> fc2 -> norm -> act -> out
        \_____________________________________/+

    Interface:
        __init__, forward
    '''

    def __init__(self, in_channels, activation=nn.ReLU(), norm_type='BN'):
        r"""
        Overview:
            Init the Residual Block

        Arguments:
            - activation (:obj:`nn.Module`): the optional activation function
            - norm_type (:obj:`str`): type of the normalization, defalut set to batch normalization
        """
        super(ResFCBlock, self).__init__()
        self.act = activation
        self.fc1 = fc_block(in_channels, in_channels, activation=self.act, norm_type=norm_type)
        self.fc2 = fc_block(in_channels, in_channels, activation=None, norm_type=norm_type)

    def forward(self, x):
        r"""
        Overview:
            return  output of  the residual block with 2 fully connected block

        Arguments:
            - x (:obj:`tensor`): the input tensor

        Returns:
            - x(:obj:`tensor`): the resblock output tensor
        """
        residual = x
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.act(x + residual)
        return x

class ResFCBlock2(nn.Module):
    def __init__(self, in_channels, activation=nn.ReLU(), norm_type='LN'):
        r"""
        Overview:
            Init the Residual Block

        Arguments:
            - activation (:obj:`nn.Module`): the optional activation function
            - norm_type (:obj:`str`): type of the normalization, defalut set to batch normalization
        """
        super(ResFCBlock2, self).__init__()
        self.act = activation
        self.fc1 = fc_block(in_channels, in_channels, activation=self.act, norm_type=None)
        self.fc2 = fc_block(in_channels, in_channels, activation=None, norm_type=None)
        self.norm = build_normalization(norm_type)(in_channels)

    def forward(self, x):
        r"""
        Overview:
            return  output of  the residual block with 2 fully connected block

        Arguments:
            - x (:obj:`tensor`): the input tensor

        Returns:
            - x(:obj:`tensor`): the resblock output tensor
        """
        residual = x
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.norm(x + residual)
        return x