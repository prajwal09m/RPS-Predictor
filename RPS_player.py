
import random
import itertools

class RPSPredictor:
    def __init__(self, order=1, decay=0.9):
        self.order = order
        self.decay = decay
        self.beat = {'R': 'P', 'P': 'S', 'S': 'R'}
        self.reset()

    def reset(self):
        self.matrix = self._create_matrix(self.order)
        self.prev_input = ""
        self.pair1 = ""
        self.pair2 = ""
        self.last_output = ""

    def _create_matrix(self, order):
        keys = self._generate_keys(order)
        matrix = {
            key: {move: {'prob': 1/3, 'n_obs': 0} for move in 'RPS'}
            for key in keys
        }
        return matrix

    def _generate_keys(self, order):
        keys = ['R', 'P', 'S']
        for _ in range(order * 2 - 1):
            prev_len = len(keys)
            for combo in itertools.product(keys, repeat=2):
                keys.append(''.join(combo))
            keys = keys[prev_len:]
        return keys

    def _update_matrix(self, pair, move):
        for option in self.matrix[pair]:
            self.matrix[pair][option]['n_obs'] *= self.decay
        self.matrix[pair][move]['n_obs'] += 1

        total = sum(self.matrix[pair][opt]['n_obs'] for opt in 'RPS')
        for option in self.matrix[pair]:
            self.matrix[pair][option]['prob'] = self.matrix[pair][option]['n_obs'] / total

    def _predict(self, pair):
        probs = self.matrix.get(pair, {opt: {'prob': 1/3} for opt in 'RPS'})
        options = list(probs.keys())
        probabilities = [probs[opt]['prob'] for opt in options]
        if max(probabilities) == min(probabilities):
            return random.choice(['R', 'P', 'S'])
        best_guess = options[probabilities.index(max(probabilities))]
        return best_guess

    def play(self, prev_play):
        if not prev_play:
            self.reset()
            return random.choice(['R', 'P', 'S'])

        self.prev_input = prev_play
        self.pair2 = self.pair1
        self.pair1 = self.last_output + self.prev_input

        if self.pair2 in self.matrix:
            self._update_matrix(self.pair2, self.prev_input)

        if self.pair1 in self.matrix:
            prediction = self._predict(self.pair1)
            self.last_output = self.beat[prediction]
        else:
            self.last_output = random.choice(['R', 'P', 'S'])

        return self.last_output

predictor = RPSPredictor()

def player(prev_play):
    return predictor.play(prev_play)

def reset():
    predictor.reset()
