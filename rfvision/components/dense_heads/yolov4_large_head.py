import torch.nn as nn
from .yolo_head import YOLOV3Head
from robotflow.rflearner.builder import HEADS
from robotflow.rflib.cnn import kaiming_init, constant_init
from torch.nn.modules.batchnorm import _BatchNorm


@HEADS.register_module()
class YOLOV4LargeHead(YOLOV3Head):
    def _init_layers(self, ):
        self.m = nn.ModuleList(nn.Conv2d(out_channels, self.num_anchors * self.num_attrib, 1) for out_channels in self.out_channels)  # output conv
        
    def forward(self, feats):
        head_outs = []
        for i in range(len(feats)):
            head_out = self.m[i](feats[i])
            head_outs.append(head_out)
        return tuple(head_outs),
        
        
    def init_weights(self, pretrained=None):
        if isinstance(pretrained, str):
            pass
        elif pretrained is None:
            for m in self.modules():
                if isinstance(m, nn.Conv2d):
                    kaiming_init(m)
                elif isinstance(m, (_BatchNorm, nn.GroupNorm)):
                    constant_init(m, 1)
        else:
            raise TypeError('pretrained must be a str or None')