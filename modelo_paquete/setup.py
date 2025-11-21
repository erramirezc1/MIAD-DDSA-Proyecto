"""
Setup para construir el paquete instalable del modelo de regresión lineal.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Leer el README si existe
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="modelo-importaciones",
    version="1.0.0",
    description="Modelo de regresión lineal para predecir valor CIF de importaciones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Equipo MIAD-DDSA",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "modelo_importaciones": [
            "model/*.pkl",
        ],
    },
    install_requires=[
        "scikit-learn>=1.0.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "joblib>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

