# @title
# --- Reto resuelto ---

# Generamos también un dato de "es fin de semana" (booleano) por cada lectura,
# simulando por ejemplo el día de la semana en que se tomó la lectura.
def generar_datos_con_dia(n):
    temperaturas, humedades = generar_datos(n)
    # 0=lunes ... 6=domingo -> fin de semana si es 5 o 6
    dias = np.random.randint(0, 7, n)
    es_fin_de_semana = (dias == 5) | (dias == 6)
    return temperaturas, humedades, es_fin_de_semana


# 1. Versión con loop: P AND Q AND (NOT R)
def alarma_con_loop_v2(temperaturas, humedades, es_fin_de_semana):
    resultados = []
    operaciones = 0
    for temp, hum, fin_semana in zip(temperaturas, humedades, es_fin_de_semana):
        operaciones += 1  # sigue siendo 1 evaluación lógica por dato
        P = temp > 30
        Q = hum < 40
        R = fin_semana
        resultados.append(P and Q and (not R))
    return resultados, operaciones


# 2. Versión vectorizada: misma lógica, con arrays completos
def alarma_vectorizada_v2(temperaturas, humedades, es_fin_de_semana):
    P = temperaturas > 30
    Q = humedades < 40
    R = es_fin_de_semana
    return P & Q & (~R)   # AND y NOT elemento a elemento


# --- Verificación de que ambas versiones coinciden ---
n = 10_000
temps, hums, finde = generar_datos_con_dia(n)

resultados_loop, ops = alarma_con_loop_v2(temps, hums, finde)
resultados_vec = alarma_vectorizada_v2(temps, hums, finde)

coinciden = np.array_equal(np.array(resultados_loop), resultados_vec)
print(f"¿Coinciden loop y vectorizado?: {coinciden}")


# --- Medición con n = 1,000,000 ---
n = 1_000_000
temps_n, hums_n, finde_n = generar_datos_con_dia(n)

inicio = time.time()
resultados_loop, operaciones = alarma_con_loop_v2(temps_n, hums_n, finde_n)
t_loop = time.time() - inicio

inicio = time.time()
resultados_vec = alarma_vectorizada_v2(temps_n, hums_n, finde_n)
t_vec = time.time() - inicio

aceleracion = t_loop / t_vec if t_vec > 0 else float("inf")
print(f"n={n:,}")
print(f"Operaciones lógicas: {operaciones:,}")
print(f"Tiempo loop:  {t_loop:.5f}s")
print(f"Tiempo numpy: {t_vec:.5f}s")
print(f"NumPy es {aceleracion:.1f}x más rápido")
