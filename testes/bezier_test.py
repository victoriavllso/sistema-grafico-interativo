import numpy as np
import matplotlib.pyplot as plt

# Pontos de controle da curva Bézier cúbica
P0 = np.array([100, 250])  # Ponto inicial
P1 = np.array([150, 100])  # Ponto de controle 1
P2 = np.array([250, 400])  # Ponto de controle 2
P3 = np.array([300, 250])  # Ponto final

# Função para calcular a curva Bézier cúbica
def cubic_bezier(t, p0, p1, p2, p3):
    return (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3

# Gerar pontos da curva
t_values = np.linspace(0, 1, 100)  # 100 pontos entre 0 e 1
curve_points = np.array([cubic_bezier(t, P0, P1, P2, P3) for t in t_values])

# Plotar a curva e os pontos de controle
plt.figure(figsize=(10, 6))
plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', label="Curva Bézier")
plt.plot([P0[0], P1[0]], [P0[1], P1[1]], 'r--', label="Linhas de controle")
plt.plot([P2[0], P3[0]], [P2[1], P3[1]], 'r--')
plt.scatter([P0[0], P3[0]], [P0[1], P3[1]], c='red', s=100, label="Pontos Inicial/Final (P0, P3)")
plt.scatter([P1[0], P2[0]], [P1[1], P2[1]], c='blue', s=100, label="Pontos de Controle (P1, P2)")
plt.title("Curva Bézier Cúbica")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.legend()
plt.axis('equal')  # Mantém a proporção correta
plt.show()