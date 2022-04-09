from itertools import permutations
import torch
from torch import nn
from scipy.optimize import linear_sum_assignment
import PITLossWrapper

class PITLossWrapper_index0(PITLossWrapper):
    @staticmethod
    def get_pw_losses(loss_func, est_targets, targets, **kwargs):
        r"""Get pair-wise losses between the training targets and its estimate
        for a given loss function.

        Args:
            loss_func: function with signature (est_targets, targets, **kwargs)
                The loss function to get pair-wise losses from.
            est_targets: torch.Tensor. Expected shape $(batch, nsrc, ...)$.
                The batch of target estimates.
            targets: torch.Tensor. Expected shape $(batch, nsrc, ...)$.
                The batch of training targets.
            **kwargs: additional keyword argument that will be passed to the
                loss function.

        Returns:
            torch.Tensor or size $(batch, nsrc, nsrc)$, losses computed for
            all permutations of the targets and est_targets.

        This function can be called on a loss function which returns a tensor
        of size :math:`(batch)`. There are more efficient ways to compute pair-wise
        losses using broadcasting.
        """
		
        est_targets = est_targets[0]
        targets = targets[0]
		
        batch_size, n_src, *_ = targets.shape
        pair_wise_losses = targets.new_empty(batch_size, n_src, n_src)
        for est_idx, est_src in enumerate(est_targets.transpose(0, 1)):
            for target_idx, target_src in enumerate(targets.transpose(0, 1)):
                pair_wise_losses[:, est_idx, target_idx] = loss_func(est_src, target_src, **kwargs)
        return pair_wise_losses
