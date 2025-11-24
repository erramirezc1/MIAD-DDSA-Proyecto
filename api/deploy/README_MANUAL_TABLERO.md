# Manual de usuario para uso del tablero

## 1. Objetivo del tablero

El tablero de análisis predictivo de importaciones colombianas en 2024 permite estimar el valor CIF en USD/kg de una operación de importación a partir de cuatro variables clave: mes, país de origen, aduana y tipo de importación. El tablero actúa como interfaz gráfica de la API de predicción y muestra un único resultado numérico fácil de interpretar.

## 2. Acceso al tablero

El tablero se abre desde un navegador web usando la dirección configurada a partir de las instrucciones del Manual de Despliegue API y tablero interactivo en EC2 Ubuntu, simlar a este ejemplo:

```text
http://IP_DEL_SERVIDOR:8050
```

## 3. Componentes principales de la interfaz

La pantalla principal se organiza de la siguiente manera:

1. **Barra superior**: franja de color verde azulado con el título del tablero:
   
   > Análisis predictivo de importaciones colombianas en 2024

2. **Texto introductorio**: debajo del título aparece un mensaje que indica que el usuario debe ingresar las variables relacionadas con la importación para obtener una estimación del valor CIF en USD/kg.

3. **Zona de filtros**: fila central con cuatro listas desplegables:
   - **Mes**
   - **País de origen**
   - **Aduana**
   - **Tipo importación**

4. **Botón de acción**:
   - Botón centrado con el texto **“Predecir valor CIF”**.

5. **Cuadro de resultado**:
   - Recuadro grande bajo el botón donde se muestra el valor CIF estimado en formato similar a este ejemplo:
   
   ```text
   184,380 USD/kg
   ```

## 4. Uso paso a paso

### 4.1 Seleccionar el mes

1. En la columna izquierda ubique la lista desplegable **Mes**.
2. Haga clic sobre el control para desplegar las opciones.
3. Seleccione el número de mes que corresponda al período de la importación, del 1 al 12.

### 4.2 Seleccionar el país de origen

1. En la segunda columna encuentre la lista desplegable **País de origen**.
2. Haga clic para desplegar el listado de países disponibles.
3. Desplácese por la lista y seleccione el país desde el cual se exporta la mercancía hacia Colombia.

### 4.3 Seleccionar la aduana

1. En la tercera columna localice la lista **Aduana**.
2. Haga clic para ver las opciones disponibles, por ejemplo:
   - **Marítima y Fluvial**
   - **Aéreas y Terrestres**
3. Seleccione el tipo de aduana por la que se proyecta ingresar la mercancía.

### 4.4 Seleccionar el tipo de importación

1. En la columna derecha se encuentra la lista **Tipo importación**.
2. Haga clic y elija la modalidad correspondiente, por ejemplo:
   - **Ordinaria**
   - **Franquicia**
   - **Temporal**
   - **Reimportación**
3. Escoja el tipo de importación de acuerdo con el régimen aduanero aplicable a la operación.

### 4.5 Generar la predicción

1. Una vez seleccionados los cuatro filtros (Mes, País de origen, Aduana y Tipo importación), diríjase al centro de la pantalla.
2. Haga clic en el botón **“Predecir valor CIF”**.
3. El tablero enviará automáticamente la información seleccionada a la API de predicción y calculará el valor CIF estimado.

### 4.6 Interpretar el resultado

1. Después de unos segundos aparecerá el valor predicho en el recuadro debajo del botón.
2. El resultado se muestra como un valor numérico en **USD/kg**, que representa el costo estimado por kilogramo de la mercancía.
3. Utilice este valor como referencia para:
   - Planear el presupuesto de la importación.
   - Comparar el precio declarado frente a la estimación del modelo.
   - Identificar posibles casos de subvaloración o sobrevaloración.

### 4.7 Actualizar la predicción

Para evaluar diferentes escenarios:

1. Modifique cualquiera de los filtros (Mes, País de origen, Aduana o Tipo importación).
2. Vuelva a hacer clic en **“Predecir valor CIF”**.
3. El recuadro de resultado se actualizará con la nueva estimación.

No es necesario recargar la página para cambiar la predicción, basta con ajustar los filtros y volver a presionar el botón.

## 5. Buenas prácticas de uso

- Revise que la combinación de mes, país, aduana y tipo de importación sea coherente con el caso real.
- Interprete la predicción como una estimación basada en datos históricos y no como un valor absoluto garantizado.
- Utilice el tablero como apoyo para la toma de decisiones, la planeación de costos y la priorización de operaciones que requieran análisis adicional.

## 6. Solución de problemas básicos

- **El tablero no carga o la página queda en blanco**:
  - Verifique que la dirección ingresada sea correcta, incluida la parte `:8050`.
  - Compruebe la conexión a internet.
  - Si el problema continúa, contacte al equipo técnico del proyecto.

- **El botón “Predecir valor CIF” no responde**:
  - Confirme que se haya seleccionado una opción válida en cada uno de los cuatro filtros.
  - Actualice la página del navegador y vuelva a intentarlo.

Con estos pasos el usuario puede explorar el tablero, comprender sus elementos clave e integrar el valor CIF estimado en su análisis de operaciones de importación.
