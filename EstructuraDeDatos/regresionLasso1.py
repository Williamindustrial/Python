import pandas as pd
import sklearn

from  sklearn.linear_model import  LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

if __name__=="__main__":
    dataset=  pd.read_csv('./data/whr2017.csv')
    print(dataset.describe())
    X=dataset[['gdp','family','lifexp','freedom', 'corruption','generosity','dystopia']]
    y= dataset[['score']]
    
    print(X.shape)
    print(y.shape)
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.25)
    modelLinear= LinearRegression().fit(x_train,y_train)
    y_predict_linear= modelLinear.predict(x_test)
    
    
    modelLasso= Lasso(alpha=0.02).fit(x_train, y_train) # entre mas grande sea el alpha existe mayor penalización
    y_predict_lasso= modelLasso.predict(x_test)
    
    modelRidge= Ridge(alpha=1).fit(x_train, y_train)
    y_predict_ridge= modelRidge.predict(x_test)
    
    linear_loss= mean_squared_error(y_test, y_predict_linear)
    print("Linear_loss ", linear_loss)
    
    loss_lasso= mean_squared_error(y_test, y_predict_lasso)
    print("Lasso_loss ",loss_lasso)
    
    loss_ridge= mean_squared_error(y_test, y_predict_ridge)
    print("loss_ridge ",loss_ridge)
    print(loss_ridge)
    print("="*32)
    print('Coef Lasso')
    print(modelLasso.coef_)
    print("="*32)
    print('Coef ridge')
    print(modelRidge.coef_)
    