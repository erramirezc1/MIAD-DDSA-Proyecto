import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
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
    alpha = 0.001
    solver = 'auto'
    max_iter = 5000
    
    # Modelo Ridge
    modelo_ridge = Ridge(alpha=alpha, solver=solver, max_iter=max_iter)  # Ajusta alpha para más regularización
    modelo_ridge.fit(X_train, y_train)

    # Predicción
    y_pred_ridge = modelo_ridge.predict(X_test)
    
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("solver", solver)
    mlflow.log_param("max_iter", max_iter)

    # Evaluación del modelo
    mae_ridge = mean_absolute_error(y_test, y_pred_ridge)
    rmse_ridge = mean_squared_error(y_test, y_pred_ridge)
    r2_ridge = r2_score(y_test, y_pred_ridge)
    
    # Registre el modelo
    mlflow.sklearn.log_model(modelo_ridge, "ridge_modelo")
    mlflow.log_metric("mae", mae_ridge)
    mlflow.log_metric("rmse", rmse_ridge)
    mlflow.log_metric("r2", r2_ridge)
