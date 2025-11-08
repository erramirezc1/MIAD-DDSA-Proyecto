# Proyecto final — Despliegue Soluciones Analíticas  
**Universidad de los Andes**

![License](https://img.shields.io/github/license/OWNER/REPO) ![Status](https://img.shields.io/badge/status-Final-blue) ![Python](https://img.shields.io/badge/python-3.10+-blue)

<p align="center">
  <!-- Sustituye por un GIF o imagen demo en assets/demo.gif -->
  <img src="https://raw.githubusercontent.com/OWNER/REPO/main/assets/demo.gif" alt="Demo del proyecto" width="800"/>
</p>

---

## Índice
- [Resumen](#resumen)
- [Equipo](#equipo)
- [Contexto y definición del problema](#contexto-y-definición-del-problema)
- [Pregunta de negocio y alcance](#pregunta-de-negocio-y-alcance)
- [Descripción de los datos](#descripción-de-los-datos)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Instalación y uso rápido](#instalación-y-uso-rápido)
- [Reproducción y artefactos](#reproducción-y-artefactos)
- [Contacto y licencia](#contacto-y-licencia)

---

## Resumen
**Proyecto final de la materia _Despliegue Soluciones Analíticas_ — Universidad de los Andes.**  
Objetivo: desarrollar un modelo supervisado para predecir el **valor CIF (USD/kg)** de importaciones en Colombia usando sólo la información disponible en la declaración de importación **antes** del arribo.

---

## Equipo

### Edwin Ricardo Ramirez Clavijo — *Principal Investigator*
- Dirección técnica del modelado predictivo  
- Diseño metodológico y validación de resultados  
- Análisis de estacionalidad  
- Visualizaciones clave para el informe  
- Redacción de secciones técnicas

### Lady Tatiana Garcia Moreno — *Principal Investigator*
- Carga y limpieza de datos  
- Unión de archivos de datos mensuales  
- Análisis y tratamiento de valores faltantes  
- Documentación de variables y metadatos  
- Soporte a ingeniería de características

### Joaquin Abondano Araoz — *Project Administrator*
- Coordinación de equipos y seguimiento del plan de trabajo  
- Documentación y publicación de materiales del proyecto  
- Control de calidad y pruebas de consistencia  
- Empaquetado final del prototipo  
- Gobernanza de datos

### Omar Leonardo Albarracín — *Data Manager*
- Curaduría, organización y preservación de datos  
- Análisis exploratorio y feature engineering  
- Modelado base con Random Forest  
- Integridad, trazabilidad y seguridad de datos  
- Publicación de datasets derivados y scripts en repositorios

---

## Contexto y definición del problema
La reducción de las importaciones en Colombia durante 2024, atribuida a la desaceleración económica y el aumento de la inflación, plantea interrogantes sobre los factores estructurales que impulsan esta tendencia y sus implicaciones sobre la economía nacional (Bancolombia, 2024). Esta contracción podría restringir el acceso a insumos y tecnología, afectar la integración del país en las cadenas de valor globales y generar repercusiones en la balanza comercial y el tipo de cambio. Asimismo, la industria local enfrenta el desafío de adaptarse a un entorno de menor disponibilidad de insumos externos, lo que pone a prueba su capacidad de innovación y eficiencia.

En este contexto, Colombia ha experimentado una contracción de las importaciones que reduce la recaudación del comercio exterior y presiona la balanza comercial y el tipo de cambio. Para las autoridades aduaneras y empresas importadoras, la falta de estimaciones precisas del valor CIF (Costo, Seguro y Flete) de los productos antes de su arribo al territorio nacional dificulta la planificación de costos y logística, encarece el financiamiento y eleva el riesgo de valuación en aduanas, lo que puede retrasar la nacionalización y el acceso oportuno a insumos y tecnologías.

Actualmente, el valor CIF se estima mediante métodos manuales, tablas de referencia y juicio experto, lo que introduce subjetividad, retrasos operativos y posibles errores de valoración. Esto puede generar tanto subvaluación (y pérdida de recaudación tributaria) como sobrevaluación (que encarece los productos y afecta la competitividad de las empresas).

Ante esta situación, nuestro proyecto propone desarrollar un modelo de aprendizaje supervisado capaz de predecir el valor CIF de una importación, utilizando únicamente la información disponible en la declaración de importación antes de que el producto llegue al país, permitiendo así:
- Optimizar los procesos de revisión aduanera.  
- Mejorar la planificación financiera de las empresas.  
- Fortalecer la transparencia y eficiencia en el comercio exterior.

El modelo busca identificar las variables más relevantes que explican el valor CIF y produce predicciones tempranas a partir de la declaración de importación, reduciendo la subjetividad de los métodos actuales.

---

## Pregunta de negocio y alcance del proyecto

**Pregunta de negocio:**  
¿Es posible predecir con precisión el valor CIF (en USD/kg) de una importación en Colombia utilizando atributos aduaneros, logísticos y económicos disponibles antes del arribo del producto?

**Alcance:**  
- Alcance técnico: entrenamiento y evaluación de modelos supervisados (baseline con Random Forest y modelos complementarios), análisis de variables relevantes, evaluación por segmentos HS/partidas arancelarias y validación temporal.  
- Entregables: código reproducible, notebooks de EDA, modelos serializados, reportes con visualizaciones y documento metodológico.

---

## Descripción de los datos a emplear
Los datos utilizados provienen de los reportes mensuales de importaciones publicados por la **DIAN**, puestos a disposición por el **DANE** en el conjunto *Importaciones de Colombia 2024, catálogo 473* (microdatos.dane.gov.co).  
- Formato original: CSV, codificación **Latin-1**, separador `;`.  
- Volumen aproximado: **3.2 GB** sin procesar (archivos mensuales concatenados).  
- Variables clave previstas: partida arancelaria (HS), país origen, country of dispatch, peso neto, valor CIF declarado, incoterm, transporte, fecha de declaración, agentes declarantes, códigos aduaneros, etc.

---

