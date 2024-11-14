import marimo

__generated_with = "0.9.18"
app = marimo.App(width="full", app_title="AHPmethod")


@app.cell
def __():
    import numpy as np
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt


    class Criterio:
        def __init__(self, criterio1, criterio2):
            self.criterio1 = criterio1
            self.criterio2 = criterio2

        def show(self):
            score = mo.ui.range_slider(
                start=-10, stop=10, step=1, value=[-1, 1], full_width=True
            )
            textl = mo.md(self.criterio1)
            textr = mo.md(self.criterio2)
            return [textl, score, textr]


    class Titles:
        def __init__(self, title):
            self.title = title

        def show(self):
            return mo.vstack(
                [mo.md(f"<br/>"), mo.md(f"#{self.title}"), mo.md(f"<br/>")]
            )


    def CompareLayoutValues(criterios):
        pares = []
        for i in range(1, criterios + 1):
            for j in range(1, criterios + 1):
                if i < j:
                    pares.append(
                        [
                            "Factor de riesgo " + str(i),
                            "Factor de riesgo " + str(j),
                        ]
                    )
        compares = []
        hstacks = []
        for i in range(int((criterios * (criterios - 1)) / 2)):
            compares.append(Criterio(pares[i][0], pares[i][1]).show())
            hstacks.append(
                mo.hstack(
                    compares[i],
                    justify="start",
                    align="center",
                    widths=[1, 6, 1],
                    gap=4,
                )
            )
        vstack = mo.vstack(hstacks)
        return compares, vstack


    def ShowMatrix(compares, criterios):
        values = []
        for i in range(len(compares)):
            values.append(
                abs(compares[i][1].value[0]) / abs(compares[i][1].value[1])
            )

        matrix0 = pd.DataFrame([[1] * criterios] * criterios, dtype=float)
        names = []
        k = -1
        for i in range(criterios):
            names.append("Factor de riesgo " + str(i + 1))
            for j in range(criterios):
                if j > i:
                    k += 1
                    matrix0.iat[i, j] = values[k]
                elif j < i:
                    matrix0.iat[i, j] = 1 / matrix0.iat[j, i]
        names = pd.DataFrame(names)
        matrix0 = pd.concat([names, matrix0], axis=1, ignore_index=True)
        matrix0.columns = [
            "Factores de riesgo\n             VS\nFactores de riesgo"
        ] + names.loc[:, 0].to_list()

        matrix1 = matrix0.iloc[:, 1:]
        matrix1 = matrix1.div(matrix1.sum(axis=0), axis=1)
        matrix1 = pd.concat([names, matrix1], axis=1, ignore_index=True)
        matrix1.columns = [
            "Factores de riesgo\n             VS\nFactores de riesgo"
        ] + names.loc[:, 0].to_list()

        matrix2 = matrix1.iloc[:, 1:]
        matrix2 = matrix2.mean(axis=1)
        matrix3 = matrix0.iloc[:, 1:].T.reset_index(drop=True).T
        matrix3 = matrix3.dot(matrix2)
        matrix4 = matrix3.div(matrix2)
        matrix5 = pd.concat(
            [names, matrix2, matrix3, matrix4], axis=1, ignore_index=True
        )
        matrix5.columns = [
            "Parámetros de cálculo\n              VS\n  Factores de riesgo",
            "Vector promedio",
            "Vector producto",
            "Vector cociente",
        ]

        ymax = matrix4.mean()
        # ci = (ymax - criterios.value) / (criterios.value - 1)
        # cr = ci / np.polyval([-8.44988345e-04, 2.56164206e-02, -2.95897436e-01, 1.61445934e+00, -2.23388889e+00], criterios.value)
        text1 = mo.md(f"El cociente promedio resultante es {str(round(ymax, 3))}")
        matrixs = [
            Titles("Matriz de consistencias").show(),
            matrix0,
            Titles("Matriz normalizada").show(),
            matrix1,
            Titles("Matriz de vectores").show(),
            matrix5,
            text1,
        ]
        return matrixs
    return (
        CompareLayoutValues,
        Criterio,
        ShowMatrix,
        Titles,
        mo,
        np,
        pd,
        plt,
    )


@app.cell(hide_code=True)
def __(mo):
    criterios = mo.ui.number(
        start=2,
        stop=10,
        step=1,
        full_width=True,
        label="Establesca el número de factores de riesgo a comparar: ",
    )
    criterios
    return (criterios,)


@app.cell(hide_code=True)
def __(CompareLayoutValues, criterios):
    compares, vstack = CompareLayoutValues(criterios.value)
    vstack
    return compares, vstack


@app.cell(hide_code=True)
def __(ShowMatrix, compares, criterios, mo):
    calcs = mo.ui.button(
        label="Calcular matrices !",
        kind="success",
        full_width=True,
        on_click=lambda _: ShowMatrix(compares, criterios.value),
    )
    calcs
    return (calcs,)


@app.cell(hide_code=True)
def __(calcs, mo):
    mo.vstack(calcs.value)
    return


if __name__ == "__main__":
    app.run()
