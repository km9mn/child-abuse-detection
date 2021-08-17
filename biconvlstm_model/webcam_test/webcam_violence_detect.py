import os
import cv2
import numpy as np 
import datetime
import argparse
import paramiko
import os
import re
import random
import shutil
import time
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.optim
import torch.utils.data
import matplotlib.pyplot as plt
from torchvision import transforms

from data.data_reader import DatasetReader
from data.data_splitter import DatasetSplit
from data.data_transformer import DatasetTransform
from data.transforms import SelectFrames, FrameDifference, Downsample, TileVideo, RandomCrop, Resize, RandomHorizontalFlip, Normalize, ToTensor

model_names = ['E', 'E_bi', 'E_bi_avg_pool', 'E_bi_max_pool']
data_names = ['FD','RWF','AH','UCF','ALL', 'YT']


parser = argparse.ArgumentParser(description='PyTorch Violence Predictor Training')
parser.add_argument('--arch', '-a', metavar='ARCH', default='E_bi_max_pool',
                    choices=model_names,
                    help='model architecture: ' +
                    ' | '.join(model_names) +
                    ' (default: E)')
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('-b', '--batch-size', default=8, type=int,
                    metavar='N', help='mini-batch size (default: 1)')
parser.add_argument('--evalmodel', default='', type=str, metavar='PATH',
                    help='path to model (default: none)')
parser.add_argument('--c', '--cpu', dest='cpu', action='store_true',
                    help='evaluate model on cpu')
parser.add_argument('--k', '--kfold', dest='kfold', default=0, type=int,
                    help='evaulate model with kfold index as test')
parser.add_argument('--s', '--split', dest='split', default=5, type=int,
                    help='fractional split of training/validation data. I.e. 5 -> 1/5 data is validation')
parser.add_argument('--f', '--frames', dest='frames', default=20, type=int,
                    help='number of frame diffs per video')
parser.add_argument('--i', '--id', dest='ID', default='', type=str,
                    help='id of the learning')
parser.add_argument('--lr', '--learning-rate', default=1e-6, type=float,
                    metavar='LR', help='initial learning rate')
parser.add_argument('--weight-decay', '--wd', default=1e-1, type=float,
                    metavar='W', help='weight decay (default: 1e-4)')

best_prec = 0

seed = 250


def main():
    global args, best_prec
    args = parser.parse_args()

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)

    # create model
    print("=> creating model '{}'".format(args.arch))
    VP = network_factory(args.arch)

    model = VP()
    
    if not args.cpu:
        model = model.cuda()

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(model.parameters(), args.lr,
                                 weight_decay=args.weight_decay)

    # optionally resume from a checkpoint
    if os.path.isfile(args.evalmodel):
        print("=> loading checkpoint '{}'".format(args.evalmodel))
        checkpoint = torch.load(args.evalmodel, map_location=torch.device('cpu'))
        args.start_epoch = checkpoint['epoch']
        print('start_epoch : ', args.start_epoch)
        best_prec = checkpoint['best_prec']
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        print("=> loaded checkpoint '{}' (epoch {})"
                .format(args.evalmodel, checkpoint['epoch']))
    else:
        print("=> no checkpoint found at '{}'".format(args.evalmodel))
    
    cap = cv2.VideoCapture(0)
    idx = 1
    total = 0
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    #out = cv2.VideoWriter('test'+str(idx)+'.mp4', fourcc,fps, (int(width), int(height)))
    frames = list()
    model_ret = 1

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = np.array(frame)
        if model_ret == 0:
            frame[::height-1,:,0] = frame[:,::width-1,0] = 0
            frame[::height-1,:,1] = frame[:,::width-1,1] = 0
            frame[::height-1,:,2] = frame[:,::width-1,2] = 255
        else:
            frame[::height-1,:,0] = frame[:,::width-1,0] = 255
            frame[::height-1,:,1] = frame[:,::width-1,1] = 0
            frame[::height-1,:,2] = frame[:,::width-1,2] = 0
        cv2.imshow('frame',frame)

        if not ret:
            break
        #out.write(frame)
        total += 1
        frames.append(frame)
        if (total%60==0):
            print(idx,total)
            idx +=1

            ###############################################
            val_dataset = DatasetReader(np.array(frames)[:,80:-80,:,:])
            val_transformations = transforms.Compose([Resize(size=224), SelectFrames(num_frames=args.frames), FrameDifference(dim=0), Normalize(), ToTensor()])
            val_dataset = DatasetTransform(val_dataset, val_transformations)
 
            data = torch.utils.data.DataLoader(val_dataset, batch_size=1, shuffle=False, num_workers=1, pin_memory=False)
            #input = torch.tensor(frames)

            print('validating input ', idx)
            model.eval()
            end = time.time()
            input = None
            for tmp in data:
                input = tmp
                break
            print('shaep : ', input.shape)
            input_var = torch.autograd.Variable(input, volatile=True)

            # compute output
            output_dict = model(input_var)
            print(output_dict)
            print(time.time() - end)

            #out = cv2.VideoWriter('test'+str(idx)+'.mp4', fourcc,fps, (int(width), int(height)))

            #model_ret = 1
            ##############################################33
            frames = list()
            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return

def validate(val_loader, model):

    # switch to evaluate mode
    model.eval()

    end = time.time()
    #for i, (input, target) in enumerate(val_loader):
    print(type(val_loader))
    input = None
    for data in val_loader:
        input = data
        break
    #input = input.view([60, 480, 640, 3])
    #print(input.shape)
    #print('changing input to tensor')
    #print('input shape : ',np.array(input).shape)
    #input = torch.from_numpy(np.array(input))
    input_var = torch.autograd.Variable(input, volatile=True)

    # compute output
    output_dict = model(input_var)
    
    print('time took : ',time.time()-end)

    return output_dict['classification']


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target):
    """Computes the precision of model"""
    batch_size = target.size(0)

    _, pred = torch.max(output.data, 1)

    correct = pred.eq(target).cpu().sum()

    res = correct * 100.0 / batch_size
    return res

# DatasetSplit (data, index, length)
def fold(folds, data):                      #folds : 몇개로 나눌건가 , data : DatasetReader
    #tot_length = len(data)                  #tot_length: 영상 총 개수
    #split_length = tot_length #// folds      # // : 나누기 결과에서 소수점 버려줌, split_length : 몇개가 한묶음?
    for i in range(folds):                  # folds =3, split_length = 5, tot_length = 15일때 i= 0,1,2
        train_dataset = None#DatasetSplit(data, (i + 1) * split_length, tot_length - split_length)   # 5, 10개/ 10, 10개 / 15 , 10개
        val_dataset = DatasetSplit(data)#, split_length, split_length)                        # 0,5개 / 5 , 5개/ 10 , 5개
        yield (train_dataset, val_dataset)
# 총 영상 개수 15개 일때 3 folds를 하면 5개는 val/ 10개는 train
# idx = 3
# train_dataset -> self.index = 5, length = 10 -> index = (5+6) % 10 = 1
# val_dataset -> self.index = 0, length = 5


def network_factory(arch):

    if arch == 'E':
        from networks.E import VP

    elif arch == 'E_bi':
        from networks.E_bi import VP

    elif arch == 'E_bi_avg_pool':
        from networks.E_bi_avg_pool import VP

    elif arch == 'E_bi_max_pool':
        from networks.E_bi_max_pool import VP

    else:
        assert 0, "Bad network arch name: " + arch

    return VP

if __name__ == '__main__':
    main()
