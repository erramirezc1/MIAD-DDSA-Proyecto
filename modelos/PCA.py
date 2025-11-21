import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
import mlflow
import mlflow.sklearn

dataframe = pd.read_csv("../data/Importaciones2024limpia_modelos.csv")




mlflow.set_tracking_uri("http://localhost:8050")
experiment = mlflow.set_experiment("proyecto_soluciones_analiticas")

X = dataframe.drop(columns=['vacid'])
y = dataframe['vacid']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Estandarización
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # Escalar solo con los datos de entrenamiento
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # Solo transformamos X_test

    # Aplicar PCA con los datos de entrenamiento
    pca = PCA(n_components=0.95)  # Mantener 95% de la varianza
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)  # Aplicamos PCA también a los datos de prueba
    
    # Entrenar el modelo de Regresión Lineal con los datos transformados
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train_pca, y_train)

    # Predicción
    y_pred_lr = modelo_lr.predict(X_test_pca)

    # Evaluación del modelo
    mae_pca = mean_absolute_error(y_test, y_pred_lr)
    rmse_pca = mean_squared_error(y_test, y_pred_lr)
    r2_pca = r2_score(y_test, y_pred_lr)

    print(f"MAE: {mae_pca}, RMSE: {rmse_pca}, R2: {r2_pca}")


    # Registre el modelo
    mlflow.sklearn.log_model(modelo_lr, "pca_linear_regression_model")
    mlflow.log_metric("mae", mae_pca)
    mlflow.log_metric("rmse", rmse_pca)
    mlflow.log_metric("r2", r2_pca)