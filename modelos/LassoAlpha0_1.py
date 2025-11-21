import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
import mlflow
import mlflow.sklearn

dataframe = pd.read_csv("Importaciones2024limpia_modelos.csv")


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
    alpha = 0.1
    
    # Modelo Lasso
    modelo_lasso = Lasso(alpha=alpha)  # Ajusta alpha según sea necesario
    modelo_lasso.fit(X_train, y_train)

    y_pred_lasso = modelo_lasso.predict(X_test)

    mlflow.log_param("alpha", alpha)

    # Evaluación del modelo
    mae_lasso = mean_absolute_error(y_test, y_pred_lasso)
    rmse_lasso = mean_squared_error(y_test, y_pred_lasso)
    r2_lasso = r2_score(y_test, y_pred_lasso)

    # Registre el modelo
    mlflow.sklearn.log_model(modelo_lasso, "lasso_modelo")
    mlflow.log_metric("mae", mae_lasso)
    mlflow.log_metric("rmse", rmse_lasso)
    mlflow.log_metric("r2", r2_lasso)
    print(f"Lasso MAE: {mae_lasso}, RMSE: {rmse_lasso}, R2: {r2_lasso}")
