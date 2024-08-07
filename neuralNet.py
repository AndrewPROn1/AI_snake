from Matrix import *


class NeuralNet:
    iNodes: int
    hNodes: int
    oNodes: int

    whi: Matrix
    whh: Matrix
    woh: Matrix

    def __init__(self, inputs, hidden, output):
        self.iNodes = inputs
        self.hNodes = hidden
        self.oNodes = output

        self.whi = Matrix(self.hNodes, self.iNodes + 1)
        self.whh = Matrix(self.hNodes, self.hNodes + 1)
        self.woh = Matrix(self.oNodes, self.hNodes + 1)

        self.whi.randomize()
        self.whh.randomize()
        self.woh.randomize()

    def mutate(self, mutate_rate):
        self.whi.mutate(mutate_rate)
        self.whh.mutate(mutate_rate)
        self.woh.mutate(mutate_rate)

    def output(self, inputs_arr):
        inputs = column(inputs_arr)
        inputs_bias = inputs.add_bias()

        hidden_inputs = self.whi.dot(inputs_bias)
        hidden_outputs = hidden_inputs.activate()
        hidden_outputs_bias = hidden_outputs.add_bias()

        hidden_inputs2 = self.whi.dot(hidden_outputs_bias)
        hidden_outputs2 = hidden_inputs2.activate()
        hidden_outputs_bias2 = hidden_outputs2.add_bias()

        output_inputs = self.woh.dot(hidden_outputs_bias2)
        outputs = output_inputs.activate()

        return outputs.to_array()

    def crossover(self, partner):
        child = NeuralNet(self.iNodes, self.hNodes, self.oNodes)

        child.whi = self.whi.crossover(partner.whi)
        child.whh = self.whi.crossover(partner.whh)
        child.woh = self.whi.crossover(partner.woh)

        return child

    def clone(self):
        clone = NeuralNet(self.iNodes, self.hNodes, self.oNodes)

        clone.whi = self.whi
        clone.whh = self.whh
        clone.woh = self.woh

        return clone

    def net_to_file(self):
        d = dict()

        whi_arr = self.whi.to_array()
        whh_arr = self.whh.to_array()
        woh_arr = self.woh.to_array()

        d["whi"] = whi_arr.copy()
        d["whh"] = whh_arr.copy()
        d["woh"] = woh_arr.copy()

        return d

    def file_to_net(self, d):
        whi_arr = d["whi"]
        whh_arr = d["whh"]
        woh_arr = d["woh"]

        self.whi.from_array(whi_arr)
        self.whh.from_array(whh_arr)
        self.woh.from_array(woh_arr)
