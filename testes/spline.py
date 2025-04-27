import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Pontos fornecidos na ordem dada
points = np.array([
    [0, 20],
    [20, 20],
    [0, 15],
    [15, 15],
    [0, 7],
    [7, 7]
])

# Criar um parâmetro t que representa a "distância" ao longo da curva
t = np.arange(len(points))  # t = [0, 1, 2, 3, 4, 5]

# Criar splines paramétricas para x(t) e y(t)
cs_x = CubicSpline(t, points[:, 0], bc_type='natural')  # Spline para x
cs_y = CubicSpline(t, points[:, 1], bc_type='natural')  # Spline para y

# Gerar pontos intermediários para uma curva suave
t_new = np.linspace(0, len(points)-1, 500)
x_new = cs_x(t_new)
y_new = cs_y(t_new)

# Plotar
plt.figure(figsize=(10, 6))
plt.plot(x_new, y_new, 'b-', label='Spline Paramétrica')
plt.plot(points[:, 0], points[:, 1], 'ro', label='Pontos Originais')

# Mostrar a ordem dos pontos
for i, (x, y) in enumerate(points):
    plt.text(x, y, f'{i}', ha='right', va='bottom')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Spline Paramétrica passando por todos os pontos')
plt.legend()
plt.grid(True)
plt.axis('equal')  # Mantém a proporção correta
plt.show()