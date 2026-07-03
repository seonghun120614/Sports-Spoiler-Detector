import numpy as np
import torch

def _clear(obj):
    """numpy/torch 타입을 파이썬 기본 타입으로 재귀 변환"""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return round(float(obj), 2)
    if isinstance(obj, float):
        return round(obj, 2)
    if isinstance(obj, torch.Tensor):
        obj = obj.detach().cpu()
        if obj.ndim == 0:
            return _clear(obj.item())
        return _clear(obj.tolist())
    if isinstance(obj, np.ndarray):
        if obj.ndim == 0:
            return _clear(obj.item())
        return _clear(obj.tolist())
    if isinstance(obj, dict):
        return {k: _clear(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clear(v) for v in obj]
    return obj