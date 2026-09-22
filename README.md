# Taller: diseño e implementación de un algoritmo genético

Selección óptima de proyectos bajo restricción presupuestal (mochila 0-1,
n = 10 proyectos, presupuesto W = 50).

## Ejecución

Todos los scripts se ejecutan desde `src/`.

```bash
cd src

python3 exacto.py              # verdad de terreno: enumeración, PD, voraz, lambda*
python3 baseline.py            # línea base aleatoria + autoprueba analítica
python3 verificar_genetico.py  # 9 pruebas de verificación del AG
python3 traza_manual.py        # traza completa de una iteración (punto 3)
python3 punto5_literal.py      # respuesta literal al punto 5 del enunciado:
                                #   5 ejecuciones con la config. inicial + tabla
                                #   A/B/C (una corrida c/u) + grafica comparativa
python3 experimentos.py        # estudio estadistico extendido -> RESULTADOS/resultados.json
python3 graficas.py            # figuras del estudio extendido -> RESULTADOS/fig*.pdf y fig*.png
```

`experimentos.py` tarda unos 45 segundos (2200 ejecuciones) y genera el
estudio estadístico extendido (factorial, barrido de lambda, comparación
contra búsqueda aleatoria). `graficas.py` requiere que `experimentos.py` se
haya ejecutado antes. `punto5_literal.py` es independiente de ambos y basta
por sí solo para cubrir lo que pide el enunciado en el punto 5.


## Estructura

```
src/
  instancia.py           datos del problema; C(X), B(X), factibilidad
  exacto.py              enumeración, programación dinámica, voraz, lambda*
  metricas.py            intervalo de Wilson, resumen con censura
  baseline.py            búsqueda aleatoria con presupuesto igualado
  genetico.py            las nueve funciones exigidas + medición de diversidad
  verificar_genetico.py  pruebas de verificación
  traza_manual.py        traza paso a paso de una iteración (punto 3)
  punto5_literal.py      respuesta literal al punto 5 (5 corridas + tabla A/B/C + grafica)
  experimentos.py        estudio extendido: factorial, barrido de lambda, McNemar, Holm
  graficas.py            figuras del estudio extendido
RESULTADOS/
  resultados.json          salida completa del estudio extendido (experimentos.py)
  hallazgos_lambda.txt     atractores dominantes por régimen de lambda
  fig1..fig5 .pdf/.png     figuras del estudio extendido (graficas.py)
  fig_ABC_comparacion.*    grafica comparativa A/B/C del punto 5 literal (punto5_literal.py)
informe taller_geneticos.pdf   informe completo (en la raíz del proyecto)
```


## Resultados principales

- **Óptimo global:** B* = 100, costo 50 exacto, `1010010001` = {P1, P3, P6, P10}.
  Único. Verificado por enumeración y por programación.
- **La heurística voraz por razón b/c alcanza ese óptimo** en diez operaciones.
- **Umbral exacto de penalización:** λ* = 1.9. Por debajo, el óptimo del paisaje
  penalizado es infactible. El λ = 5 sugerido rinde 0.31 de tasa de éxito frente
  a 0.65 con λ = 2.1.
- **El algoritmo genético no supera a la búsqueda aleatoria** con el mismo
  presupuesto de evaluaciones en ninguna de las doce configuraciones evaluadas
  (McNemar pareado con corrección de Holm, 100 semillas): empata en tres y es
  significativamente peor en ocho.

## Nota sobre reproducibilidad

Cada ejecución usa una instancia `random.Random(semilla)` propia en lugar del
estado global de `random`. Los resultados son por tanto reproducibles
exactamente, y el orden en que se ejecuten los scripts no altera ninguna salida.
