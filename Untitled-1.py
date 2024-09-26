Import tensorflow as tf # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

# Datos: Valores en Celsius y sus correspondientes en Fahrenheit
celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

# Definición de la arquitectura del modelo
# Capa oculta 1 con 3 neuronas
oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
# Capa oculta 2 con 3 neuronas
oculta2 = tf.keras.layers.Dense(units=3)
# Capa de salida con 1 neurona (predicción de Fahrenheit)
salida = tf.keras.layers.Dense(units=1)

# Creación del modelo secuencial
modelo = tf.keras.Sequential([oculta1, oculta2, salida])

# Compilación del modelo
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),  # Optimizador Adam con tasa de aprendizaje de 0.1
    loss='mean_squared_error'  # Función de pérdida de error cuadrático medio
)

# Entrenamiento del modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(celsius, fahrenheit, epochs=1000, verbose=False)  # Entrena durante 1000 épocas

# Visualización de la pérdida durante el entrenamiento
plt.xlabel("# Época")  # Etiqueta del eje X
plt.ylabel("Magnitud de pérdida")  # Etiqueta del eje Y
plt.plot(historial.history["loss"])  # Grafica la pérdida
plt.show()  # Muestra el gráfico

# Realizando una predicción
print("Hagamos una predicción!")
resultado = modelo.predict([100.0])  # Predicción para 100 grados Celsius
print("El resultado es " + str(resultado[0][0]) + " fahrenheit!")  # Muestra el resultado

# Imprimir las variables internas del modelo (pesos de las capas)
print("Variables internas del modelo")
print(oculta1.get_weights())  # Pesos de la primera capa oculta
print(oculta2.get_weights())  # Pesos de la segunda capa oculta
print(salida.get_weights())    # Pesos de la capa de salida

print("Modelo entrenado!")  # Mensaje final