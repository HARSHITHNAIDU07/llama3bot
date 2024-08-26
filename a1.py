import torch
print(torch.__version__)
print(torch.cuda.is_available())  # This should return False since you're using CPU
