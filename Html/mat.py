import matplotlib.pyplot as plt

x = [214, 103, 141, 173, 209, 127, 117, 89, 62, 37]
y = [103, 58, 83, 114, 103, 97, 65, 61, 47, 36]

y_pred = [53.8984 + 0.1796 * xi for xi in x]

plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='blue', label='Фактические данные')
plt.plot(x, y_pred, color='red', label='Линия регрессии')
plt.title('Поле корреляции и линия регрессии')
plt.xlabel('Площадь квартиры, м²')
plt.ylabel('Цена квартиры, тыс. долл.')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("correlation_plot.png", dpi=300)  
plt.show()
