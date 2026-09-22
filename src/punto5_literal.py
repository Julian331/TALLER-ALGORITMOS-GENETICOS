"""
Punto 5 del enunciado, en su forma literal.

experimentos.py (100 semillas, tasa de exito, McNemar, Holm...) responde una
pregunta mas fuerte -- "cual es el efecto real de cada parametro" -- pero no
entrega el formato que pide el enunciado: una tabla con UNA corrida por cada
experimento A, B, C, reportando mejor beneficio, costo, proyectos, generacion
en la que aparecio esa mejor solucion, tiempo de ejecucion y aptitud promedio
de la ultima generacion. Este script entrega exactamente eso, ademas de las
"al menos cinco ejecuciones con la configuracion inicial" y la grafica
comparativa de las tres curvas (mejor aptitud + aptitud promedio) que pide
el enunciado.

Se usa una unica semilla fija (SEMILLA_ENUNCIADO = 42, la que sugiere el
enunciado) para esta tabla literal. El resto del proyecto (experimentos.py)
usa una semilla por corrida por las razones ya documentadas en el informe;
aqui se vuelve a la semilla 42 porque lo que se pide en este punto es
justamente "una corrida", no un estudio estadistico.
"""

import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from genetico import CONFIG_ENUNCIADO, ejecutar_algoritmo_genetico
from instancia import proyectos_seleccionados

SEMILLA_ENUNCIADO = 42
DIR_RESULTADOS = os.path.join(os.path.dirname(__file__), "..", "RESULTADOS")

EXPERIMENTOS = {
    "A": {"n_poblacion": 10, "n_generaciones": 50, "p_mutacion": 0.01},
    "B": {"n_poblacion": 20, "n_generaciones": 100, "p_mutacion": 0.05},
    "C": {"n_poblacion": 50, "n_generaciones": 200, "p_mutacion": 0.10},
}
BASE = {"p_cruce": 0.80, "tam_torneo": 3, "n_elite": 1, "lambda_penalizacion": 5.0}


def _mejor_solucion(resultado):
    """Prefiere la mejor solucion FACTIBLE encontrada en la corrida;
    si ninguna lo fue, cae de vuelta a la mejor por aptitud (informando
    que es invalida, para que quede visible y no se reporte como buena)."""
    if resultado["mejor_factible"] is not None:
        r = resultado["mejor_factible"]
        return r["beneficio"], r["costo"], r["proyectos"], True
    r = resultado["mejor_por_aptitud"]
    return r["beneficio"], r["costo"], r["proyectos"], False


# ---------------------------------------------------------------------------
# 1) Al menos cinco ejecuciones con la configuracion inicial (N=20, G=100...)
# ---------------------------------------------------------------------------
def cinco_ejecuciones_config_inicial(n_corridas=5):
    print("=" * 78)
    print(f"CINCO EJECUCIONES CON LA CONFIGURACION INICIAL {CONFIG_ENUNCIADO}")
    print("=" * 78)
    for s in range(n_corridas):
        r = ejecutar_algoritmo_genetico(**CONFIG_ENUNCIADO, semilla=s)
        beneficio, costo, proyectos, valido = _mejor_solucion(r)
        print(f"Corrida {s + 1} (semilla={s}): Beneficio={beneficio}  Costo={costo}  "
              f"Valido={valido}  Proyectos={proyectos}")
    print()


# ---------------------------------------------------------------------------
# 2) Tabla literal de los experimentos A, B y C (una corrida cada uno)
# ---------------------------------------------------------------------------
def tabla_experimentos_abc(semilla=SEMILLA_ENUNCIADO):
    print("=" * 78)
    print(f"EXPERIMENTOS A, B, C -- una corrida por experimento (semilla={semilla})")
    print("=" * 78)

    resultados = {}
    for nombre, cfg in EXPERIMENTOS.items():
        inicio = time.perf_counter()
        r = ejecutar_algoritmo_genetico(
            **cfg, **BASE, semilla=semilla, registrar_historial=True
        )
        duracion = time.perf_counter() - inicio
        beneficio, costo, proyectos, valido = _mejor_solucion(r)

        resultados[nombre] = {
            "config": cfg,
            "beneficio": beneficio,
            "costo": costo,
            "proyectos": proyectos,
            "valido": valido,
            "generacion_mejor": r["generacion_mejor_factible"],
            "tiempo_s": duracion,
            "aptitud_promedio_final": r["historial"][-1]["aptitud_promedio"],
            "historial": r["historial"],
        }

        print(f"\n--- Experimento {nombre}  {cfg} ---")
        print(f"  Mejor beneficio           : {beneficio}")
        print(f"  Costo                     : {costo} / 50  (valido: {valido})")
        print(f"  Proyectos seleccionados   : {proyectos}")
        print(f"  Generacion del mejor      : {resultados[nombre]['generacion_mejor']}")
        print(f"  Tiempo de ejecucion       : {duracion:.4f} s")
        print(f"  Aptitud promedio (ult.gen): {resultados[nombre]['aptitud_promedio_final']:.2f}")

    print()
    return resultados


# ---------------------------------------------------------------------------
# 3) Grafica comparativa: mejor aptitud y aptitud promedio por generacion,
#    para A, B y C en una sola figura (lo que pide literalmente el enunciado)
# ---------------------------------------------------------------------------
def grafica_comparativa_abc(resultados):
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    colores = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}

    plt.figure(figsize=(9, 5.5))
    for nombre, datos in resultados.items():
        hist = datos["historial"]
        gens = [h["generacion"] for h in hist]
        mejores = [h["mejor_aptitud"] for h in hist]
        promedios = [h["aptitud_promedio"] for h in hist]
        color = colores[nombre]
        plt.plot(gens, mejores, color=color, linewidth=2,
                  label=f"Mejor aptitud - Exp {nombre}")
        plt.plot(gens, promedios, color=color, linewidth=1.4, linestyle="--",
                  label=f"Aptitud promedio - Exp {nombre}")

    plt.xlabel("Generacion")
    plt.ylabel("Aptitud")
    plt.title("Evolucion de la aptitud por experimento (A, B, C)")
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    ruta = os.path.join(DIR_RESULTADOS, "fig_ABC_comparacion.png")
    plt.savefig(ruta, dpi=150)
    plt.savefig(ruta.replace(".png", ".pdf"))
    plt.close()
    print(f"Grafica guardada en {ruta} (y su version .pdf)")


if __name__ == "__main__":
    cinco_ejecuciones_config_inicial()
    resultados = tabla_experimentos_abc()
    grafica_comparativa_abc(resultados)
