import torch
import torch.nn as nn
from torch.nn import Parameter
import torch.nn.functional as F

class Attention(nn.Module):

    def __init__(self, args):
        # :param int input_dim: Input's diamention
        # :param int hidden_dim: Number of hidden units in the attention

        super(Attention, self).__init__()
        self.args           = args
        self.input_linear   = nn.Linear(args.n_hidden, args.n_hidden)
        self.context_linear = nn.Conv1d(args.n_hidden, args.n_hidden, 1, 1)
        self.V = Parameter(torch.FloatTensor(args.n_hidden), requires_grad=True)
        self._inf = Parameter(torch.FloatTensor([float('-inf')]), requires_grad=False)
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax()

        # Initialize vector V
        nn.init.uniform_(self.V, -1, 1)

    def forward(self, input,
                context,
                mask):
        # :param Tensor input: Hidden state h
        # :param Tensor context: Attention context
        # :param ByteTensor mask: Selection mask
        # :return: tuple of - (Attentioned hidden state, Alphas)

        # (batch, hidden_dim, seq_len)
        inp = self.input_linear(input).unsqueeze(2).expand(-1, -1, context.size(1))

        # (batch, hidden_dim, seq_len)
        context = context.permute(0, 2, 1)
        ctx = self.context_linear(context)

        # (batch, 1, hidden_dim)
        V = self.V.unsqueeze(0).expand(context.size(0), -1).unsqueeze(1)

        # (batch, seq_len)
        att = torch.bmm(V, self.tanh(inp + ctx)).squeeze(1)
        if len(att[mask]) > 0:
            att[mask] = self.inf[mask]
        alpha = self.softmax(att)

        hidden_state = torch.bmm(ctx, alpha.unsqueeze(2)).squeeze(2)

        return hidden_state, alpha

    def init_inf(self, mask_size):
        self.inf = self._inf.unsqueeze(1).expand(*mask_size)
