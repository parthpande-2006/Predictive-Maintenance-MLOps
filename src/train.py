import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
from xgboost import XGBClassifier

from dataprocessing import load_data

def train_and_evaluate_models(data_path:str, output_dir:str = 'models'):
    X_train, X_test, y_train, y_test = load_data(data_path)
    models = {'RandomForest': RandomForestClassifier(n_estimators = 100, class_weight = 'balanced', random_state =42),
              'XGB': XGBClassifier(n_estimators = 150, learning_rate = 0.05, scale_pos_weight = 28, eval_metric = 'logloss', random_state= 42)}
    best_f1 = 0
    best_model = None
    model_name = ""

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        f1 = f1_score(y_test, predictions)
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)

        print(f'model:{name}')
        print(f'Precision: {precision:.4f}')
        print(f'Recall: {recall: .4f}')
        print(f'F1 Score : {f1: .4f}')

        if f1> best_f1:
            best_f1 = f1
            best_model = model
            model_name = name
    os.makedirs(output_dir, exist_ok=True)
    model_save_path = os.path.join(output_dir, 'predictive_model.pkl')
    joblib.dump(best_model, model_save_path)
    print(f' best_model:{model_name}')
    print(f'saved model serialization archi to: {model_save_path}\n')


if __name__ == '__main__':
    train_and_evaluate_models('data/ai4i2020.csv')


    

