import torch.nn as nn
import torch
import torch.nn.functional as F
import random


class Decoder(nn.Module):
    def __init__(self, hidden_size, output_size,max_length,dropout_p=0.1,teacher_forcing_ratio=0.4):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length
        self.teacher_forcing_ratio =teacher_forcing_ratio
        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)
        self.criterion = nn.NLLLoss()


    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    def decode(self,decoder_input,encoder_output,hidden,length):

        decoder_hidden = hidden

        wrong_indexs = 0
        result = []
        for di in range(length):
            decoder_output, decoder_hidden, decoder_attention = self(
                decoder_input, decoder_hidden, encoder_output)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input
            result.append(topi.cpu().detach().numpy()[0][0])
        return result