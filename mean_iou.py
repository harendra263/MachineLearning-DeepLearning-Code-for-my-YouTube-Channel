from tkinter import Y
import torch
import torch.nn.functional as F
import numpy as np

#######################################################
# First Alternative Mean IoU Calculations with PyTorch
########################################################
def mean_iou(predicted_label, label, eps=1e-10, num_classes=10):
    with torch.no_grad():
        predicted_label = F.softmax(predicted_label, dim=1)
        predicted_label = torch.argmax(predicted_label, dim=1)

        predicted_label = predicted_label.contiguous().view(-1)
        label = label.contiguous().view(-1)

        iou_single_class = []
        for class_number in range(num_classes):
            true_predicted_class = predicted_label == class_number
            true_label = label == class_number

            if true_label.long().sum().item() == 0:
                iou_single_class.append(np.nan)
            else:
                intersection = (
                    torch.logical_and(true_predicted_class, true_label)
                    .sum()
                    .float()
                    .item()
                )
                union = (
                    torch.logical_or(true_predicted_class, true_label)
                    .sum()
                    .float()
                    .item()
                )

                iou = (intersection + eps) / (union + eps)
                iou_single_class.append(iou)
        return np.nanmean(iou_single_class)


############################################
# Second Alternative Mean IoU Calculations
############################################
def meanIoU(target, predicted):
    if target.shape != predicted.shape:
        print(
            "target has dimension",
            target.shape,
            ", predicted values have shape ",
            predicted.shape,
        )
        return

    if target.dim() != 4:
        print("target has dim ", target.dim(), ", it must be 4")
        return

    iousum = 0
    for i in range(target.shape[0]):
        target_arr = target[i, :, :, :].clone().detach().cpu().numpy().argmax(0)
        predicted_arr = predicted[i, :, :, :].clone().detach().cpu().numpy().argmax(0)

        intersection = np.logical_and(target_arr, predicted_arr).sum()
        union = np.logical_or(target_arr, predicted_arr).sum()

        iou_score = 0 if union == 0 else intersection / union
        iousum += iou_score

    return iousum / target.shape[0]


#######################################################
# Third Alternative Mean IoU Calculations with sklearn
#######################################################
from sklearn.metrics import confusion_matrix


def mean_iou(y_pred, y_true):
    y_pred = y_pred.flatten()
    y_true = y_true.flatten()

    confusion_tensor = confusion_matrix(y_true, y_pred, labels=[0, 1])

    intersection = np.diag(confusion_tensor)
    ground_truth_set = confusion_tensor.sum(axis=1)
    predicted_set = confusion_tensor.sum(axis=0)

    union = ground_truth_set + predicted_set - intersection
    IoU = intersection / union.astype(np.float32)
    return np.mean(IoU)
