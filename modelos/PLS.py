import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.cross_decomposition import PLSRegression
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
    # Aplicar PLS con 10 componentes
    pls = PLSRegression(n_components=10)
    pls.fit(X_train, y_train)
   
    # Predicción
    y_pred_pls = pls.predict(X_test)

    # Evaluar el desempeño del modelo con PLS
    mae_pls = mean_absolute_error(y_test, y_pred_pls)
    rmse_pls = mean_squared_error(y_test, y_pred_pls)
    r2_pls = r2_score(y_test, y_pred_pls)
    # Registre el modelo
    mlflow.sklearn.log_model(pls, "modelo_pls")
    mlflow.log_metric("mae", mae_pls)
    mlflow.log_metric("rmse", rmse_pls)
    mlflow.log_metric("r2", r2_pls)
    
