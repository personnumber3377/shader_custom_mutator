
import copy

def deepclone(x):
    # dataclasses + simple classes: copy.deepcopy is fine
    return copy.deepcopy(x)
