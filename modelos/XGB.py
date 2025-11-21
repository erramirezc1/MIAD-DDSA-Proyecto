import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
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

with mlflow.start_run(experiment_id=experiment.experiment_id, run_name="XGboost"):
    modelo_xgb = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
    modelo_xgb.fit(X_train, y_train)

    # Predicción
    y_pred_xgb = modelo_xgb.predict(X_test)

    # Evaluación del Modelo
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    rmse_xgb = mean_squared_error(y_test, y_pred_xgb)
    r2_xgb = r2_score(y_test, y_pred_xgb)
    # Registre el modelo
    mlflow.sklearn.log_model(modelo_xgb, "modelo_xgb")
    mlflow.log_metric("mae", mae_xgb)
    mlflow.log_metric("rmse", rmse_xgb)
    mlflow.log_metric("r2", r2_xgb)
