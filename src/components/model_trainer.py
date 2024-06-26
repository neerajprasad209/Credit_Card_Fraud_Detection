import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

from dataclasses import dataclass
import sys
import os


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
        
    def initate_model_training(self, train_array, test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                "Random Forest Classifier" : RandomForestClassifier(random_state=21,n_estimators=40),
                "Decision Tree Classifer" : DecisionTreeClassifier(random_state=21,criterion="entropy"),
                "Logistic Regression" : LogisticRegression()
            }
            
            model_report : dict= evaluate_model(X_train,y_train, X_test,y_test,models)
            print("\n======================================Model Report======================================\n")
            print(model_report)
            
            logging.info(f"Model Report : {model_report}")
            
            # To get the Mdoel Score From the Dictionary
            print("\n======================================Finding Best Model======================================\n")
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            print(f"Best Model Found , Model Name : {best_model_name}, Accuracy Score :{best_model_score}")
            print("\n=============================================================================================\n")
            
            logging.info(f"Best Model Found, Model Name :{best_model_name}, Accuracy Score :{best_model_score}")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
        except Exception as e:
            logging.info("Exception occured in the Model Traning.")
            raise CustomException(e,sys)