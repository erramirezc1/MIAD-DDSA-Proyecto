import pandas as pd
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
    alpha = 0.01
    

    modelo_base = LinearRegression()
    sfs = SequentialFeatureSelector(modelo_base, direction="forward", n_features_to_select="auto", cv=5)
    sfs.fit(X_train, y_train)

    # Variables seleccionadas
    selected_features = X_train.columns[sfs.get_support()]
    print("Variables seleccionadas:", list(selected_features))

    # Entrenar el modelo con las variables seleccionadas
    X_train_selected = X_train[selected_features]
    X_test_selected = X_test[selected_features]

    modelo_final = LinearRegression()
    modelo_final.fit(X_train_selected, y_train)

    # Hacer predicciones
    y_pred = modelo_final.predict(X_test_selected)

    # Evaluar el modelo
    mae_rg_forward = mean_absolute_error(y_test, y_pred)
    rmse_rg_forward = mean_squared_error(y_test, y_pred)
    r2_rg_forward = r2_score(y_test, y_pred)

    print(f"MAE: {mae_rg_forward}, RMSE: {rmse_rg_forward}, R2: {r2_rg_forward}")

    mlflow.log_param("alpha", alpha)

    # Evaluación del modelo
    mae_lasso = mean_absolute_error(y_test, y_pred)
    rmse_lasso = mean_squared_error(y_test, y_pred)
    r2_lasso = r2_score(y_test, y_pred)

    # Registre el modelo
    mlflow.sklearn.log_model(modelo_final, "forward_linear_regression_model")
    mlflow.log_metric("mae", mae_lasso)
    mlflow.log_metric("rmse", rmse_lasso)
    mlflow.log_metric("r2", r2_lasso)