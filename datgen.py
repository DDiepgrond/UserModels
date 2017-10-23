import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FOLDER = 'output'

N_SELECTION_LOOPS = 15
N_ROUNDS = 5
N_SAMPLES = 10

HEIGHT_OFFSET = .1
PHASE_OFFSET = 30

FREQ_NOISE = .1
HEIGHT_NOISE = .4
SIGNAL_NOISE = .3

def gen_wave(amp, height_offset, freq, phase, samples):
    t = np.arange(samples)

    freq *= np.random.uniform(1-FREQ_NOISE, 1)
    height_noise = np.random.uniform(-HEIGHT_NOISE, HEIGHT_NOISE, samples) + height_offset
    noise = np.random.uniform(-2 * SIGNAL_NOISE, 2 * SIGNAL_NOISE, samples)

    wave = amp * np.sin(2 * np.pi *  freq * t / samples + phase)
    wave = (wave + noise + height_noise)
    return wave.tolist()

def add_plot(wave, color='blue', xlabel = '', ylabel = ''):
    for s in wave:
        data = []
        for r in s:
            data += r
        plt.plot(data, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot_all():
    plt.show()

def gen_selection_loop(n_rounds, samples_per_round, height_shift, phase_shift):
    data = []
    flip = 1
    for i in range(n_rounds):
        round = gen_wave(1, height_shift, .5, np.deg2rad(flip*90) + np.deg2rad(phase_shift), samples_per_round)
        data.append(round)
        flip *= -1
    return data

def gen_data(n_selection_loops, n_rounds, samples_per_round, height_shift, phase_shift):
    data = []
    for i in range(n_selection_loops):
        s_loop = gen_selection_loop(n_rounds, samples_per_round, height_shift, phase_shift)
        data.append(s_loop)

    mx = max([max([max(r) for r in s]) for s in data])
    mn = min([min([min(r) for r in s]) for s in data])
    return data, mx, mn
    
def norm_data(data, mx, mn):
    data = [[[(x-mn)/(mx-mn) for x in r] for r in s] for s in data]
    return data

def save_wave(wave, name):
    data = [[[str(d) for d in i] for i in s] for s in wave]
    with open(OUTPUT_FOLDER + '/' + name + '.dat', "w") as f:
        np.save(f, data)

if __name__ == "__main__":
    d0, mx0, mn0 = gen_data(N_SELECTION_LOOPS, N_ROUNDS, N_SAMPLES, -HEIGHT_OFFSET, 0)
    d1, mx1, mn1 = gen_data(N_SELECTION_LOOPS, N_ROUNDS, N_SAMPLES, HEIGHT_OFFSET, PHASE_OFFSET)

    mx = max([mx0, mx1])
    mn = min([mn0, mn1])

    d0 = norm_data(d0, mx, mn)
    d1 = norm_data(d1, mx, mn)

    add_plot(d0)
    add_plot(d1, 'green')
    plot_all()
    save_wave(d0, '0/0')
    save_wave(d1, '1/1')