import numpy as np
import pandas as pd

# Parámetros de la simulación
hours = 8  # Simular 8 horas
arrival_rate = 5  # En promedio, llegan 5 clientes por hora
service_rate = 6  # El cajero atiende 6 clientes por hora en promedio
total_minutes = hours * 60  # Convertir las horas a minutos

# Inicializar variables
current_time = 0
queue = []  # Cola de espera
service_time = 0  # Tiempo en que el cajero estará libre
waiting_times = []  # Lista para guardar los tiempos de espera

# Función para generar tiempos entre llegadas de clientes (distribución exponencial)
def generate_interarrival_time(rate):
    return np.random.exponential(1 / rate) * 60  # Convertir a minutos

# Función para generar tiempo de servicio (distribución exponencial)
def generate_service_time(rate):
    return np.random.exponential(1 / rate) * 60  # Convertir a minutos

# Simulación de la llegada y atención de clientes
while current_time < total_minutes:
    # Tiempo hasta la próxima llegada de cliente
    next_arrival = generate_interarrival_time(arrival_rate)
    current_time += next_arrival
    
    if current_time >= total_minutes:
        break
    
    # Si el cajero está ocupado, agregar a la cola
    if current_time < service_time:
        queue.append(current_time)
    else:
        # Si el cajero está libre, atender al cliente inmediatamente
        service_time = current_time + generate_service_time(service_rate)
        waiting_times.append(0)  # Este cliente no tuvo que esperar
    
    # Procesar a los clientes en la cola cuando el cajero esté libre
    while queue and service_time <= total_minutes:
        # Sacar al cliente de la cola
        arrival_time = queue.pop(0)
        wait_time = service_time - arrival_time
        waiting_times.append(wait_time)
        
        # Generar tiempo de servicio para este cliente
        service_time += generate_service_time(service_rate)

# Resultados de la simulación
waiting_times = np.array(waiting_times)
avg_wait_time = waiting_times.mean()

print(f"Total de clientes atendidos: {len(waiting_times)}")
print(f"Tiempo promedio de espera: {avg_wait_time:.2f} minutos")
print(f"Clientes que no esperaron: {len(waiting_times[waiting_times == 0])}")

# Crear un DataFrame para guardar la información
result_df = pd.DataFrame({
    "Cliente": np.arange(1, len(waiting_times) + 1),
    "Tiempo de espera (min)": waiting_times
})

# Mostrar los primeros 10 clientes
print(result_df.head(10))
