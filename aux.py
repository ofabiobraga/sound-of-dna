import numpy as np
import matplotlib.pyplot as plt

def graph_senoidal_la_oitavas():
    # Frequência da nota Lá em Hz
    frequencia = 440

    # Amplitude da onda senoidal
    amplitude = 1

    # Período de tempo de -2pi a 2pi
    tempo = np.linspace(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2), 1000)

    # Equação da onda senoidal
    senoide_220 = amplitude * np.sin(2 * np.pi * 0.5 * frequencia * tempo)
    senoide_440 = amplitude * np.sin(2 * np.pi * frequencia * tempo)
    senoide_880 = amplitude * np.sin(2 * np.pi * 2 * frequencia * tempo)

    # Configurações do gráfico
    plt.figure(figsize=(8, 4))
    plt.plot(tempo, senoide_440, label='440 [Hz]', linestyle='solid', color='black', linewidth=2)
    plt.plot(tempo, senoide_220, label='220 [Hz]', linestyle='dashed', color='black', linewidth=2)
    plt.plot(tempo, senoide_880, label='880 [Hz]', linestyle='dotted', color='black', linewidth=2)
    plt.title('Sonoidal - Oitavas de Lá')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.xlim(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2))
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.legend()
    plt.show()

def graph_amplitude():
    # Frequência da nota Lá em Hz
    frequencia = 440

    # Período de tempo de -2pi a 2pi
    tempo = np.linspace(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2), 1000)

    # Equação da onda senoidal
    senoide_1 = 1 * np.sin(2 * np.pi * frequencia * tempo)
    senoide_2 = 0.2 * np.sin(2 * np.pi * frequencia * tempo)

    # Configurações do gráfico
    plt.figure(figsize=(8, 4))
    plt.plot(tempo, senoide_1, label='Mais alto', linestyle='solid', color='black', linewidth=2)
    plt.plot(tempo, senoide_2, label='Mais baixo', linestyle='dashed', color='black', linewidth=2)
    plt.title('Volume')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.xlim(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2))
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.legend()
    plt.show()
    
def graph_frequencies_high_low():
    # Frequência da nota Lá em Hz
    frequencia = 55

    # Período de tempo de -2pi a 2pi
    tempo = np.linspace(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2), 1000)

    # Equação da onda senoidal
    senoide_1 = np.sin(2 * np.pi * frequencia * tempo)
    senoide_2 = np.sin(2 * np.pi * 4 * frequencia * tempo)

    # Configurações do gráfico
    plt.figure(figsize=(8, 4))
    plt.plot(tempo, senoide_1, label='Mais grave', linestyle='solid', color='black', linewidth=2)
    plt.plot(tempo, senoide_2, label='Mais agudo', linestyle='dashed', color='black', linewidth=1)
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.xlim(-2 * np.pi/(frequencia*2), 2 * np.pi/(frequencia*2))
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.legend()
    plt.show()
    
graph_frequencies_high_low()
