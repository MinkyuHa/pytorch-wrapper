import torch
import numpy as np
import unittest

from unittest.mock import MagicMock

from pytorch_wrapper.loss_wrappers import GenericPointWiseLossWrapper, SequenceLabelingGenericPointWiseLossWrapper


class GenericPointWiseLossWrapperTestCase(unittest.TestCase):

    def test_execution(self):
        mocked_loss_module = MagicMock(side_effect=lambda x, y: (x - y).sum())

        model_output_key = None
        batch_target_key = 'target'
        loss_wrapper = GenericPointWiseLossWrapper(mocked_loss_module, model_output_key, batch_target_key)

        output = torch.tensor([1., 2., 3., 4.])
        batch = {'target': torch.tensor([1., 2., 3., 4.])}
        training_context = {}

        res = loss_wrapper.calculate_loss(output, batch, training_context)

        self.assertAlmostEqual(res.item(), 0.)


class SequenceLabelingGenericPointWiseLossWrapperTestCase(unittest.TestCase):

    def test_binary(self):
        mocked_loss_module = MagicMock(side_effect=lambda x, y: (x - y).sum())

        bi_sequence_len_idx = 1
        batch_input_key = 'input'
        model_output_key = None
        batch_target_key = 'target'
        perform_last_activation = False
        end_padded = True
        loss_wrapper = SequenceLabelingGenericPointWiseLossWrapper(loss=mocked_loss_module,
                                                                   batch_input_sequence_length_idx=bi_sequence_len_idx,
                                                                   batch_input_key=batch_input_key,
                                                                   model_output_key=model_output_key,
                                                                   batch_target_key=batch_target_key,
                                                                   perform_last_activation=perform_last_activation,
                                                                   end_padded=end_padded)

        output = torch.tensor([[1., 0., -2.], [1., -2., -2.], [1., 0., 0.]])
        batch = {'target': torch.tensor([[1., 0., -1.], [1., -1., -1.], [1., 0., 0.]]),
                 'input': [None, torch.tensor([2, 1, 3], dtype=torch.int)]}
        training_context = {}

        res = loss_wrapper.calculate_loss(output, batch, training_context)

        self.assertAlmostEqual(res.item(), 0.)

    def test_multilabel(self):
        mocked_loss_module = MagicMock(side_effect=lambda x, y: (x - y).sum())

        bi_sequence_len_idx = 1
        batch_input_key = 'input'
        model_output_key = None
        batch_target_key = 'target'
        perform_last_activation = False
        end_padded = True
        loss_wrapper = SequenceLabelingGenericPointWiseLossWrapper(loss=mocked_loss_module,
                                                                   batch_input_sequence_length_idx=bi_sequence_len_idx,
                                                                   batch_input_key=batch_input_key,
                                                                   model_output_key=model_output_key,
                                                                   batch_target_key=batch_target_key,
                                                                   perform_last_activation=perform_last_activation,
                                                                   end_padded=end_padded)

        output = torch.tensor([[[1., 1.], [0., 1.], [-2., -2.]], [[1., 1.], [-2., -2.], [-2., -2.]],
                               [[1., 0.], [0., 1.], [1., 1.]]])

        batch = {'target': torch.tensor([[[1., 1.], [0., 1.], [-1., -1.]], [[1., 1.], [-1., -1.], [-1., -1.]],
                                         [[1., 0.], [0., 1.], [1., 1.]]]),
                 'input': [None, torch.tensor([2, 1, 3], dtype=torch.int)]}
        training_context = {}

        res = loss_wrapper.calculate_loss(output, batch, training_context)

        self.assertAlmostEqual(res.item(), 0.)

    def test_multiclass(self):
        eye = torch.eye(2)
        mocked_loss_module = MagicMock(side_effect=lambda x, y: (x - eye[y]).sum())

        bi_sequence_len_idx = 1
        batch_input_key = 'input'
        model_output_key = None
        batch_target_key = 'target'
        perform_last_activation = False
        end_padded = True
        loss_wrapper = SequenceLabelingGenericPointWiseLossWrapper(loss=mocked_loss_module,
                                                                   batch_input_sequence_length_idx=bi_sequence_len_idx,
                                                                   batch_input_key=batch_input_key,
                                                                   model_output_key=model_output_key,
                                                                   batch_target_key=batch_target_key,
                                                                   perform_last_activation=perform_last_activation,
                                                                   end_padded=end_padded)

        output = torch.tensor([[[1., 0.], [0., 1.], [-2., -2.]], [[1., 0.], [-2., -2.], [-2., -2.]],
                               [[1., 0.], [0., 1.], [0., 1.]]])

        batch = {'target': torch.tensor([[0, 1, -1], [0, -1, -1], [0, 1, 1]], dtype=torch.long),
                 'input': [None, torch.tensor([2, 1, 3], dtype=torch.int)]}
        training_context = {}

        res = loss_wrapper.calculate_loss(output, batch, training_context)

        self.assertAlmostEqual(res.item(), 0.)
