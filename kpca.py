#Usando kernels para clasificar funciones
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import KernelPCA
from sklearn.decomposition import IncrementalPCA
 
from sklearn.linear_model import LogisticRegression
 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
 
if __name__ == "__main__":
    
    # Cargamos los datos del dataframe de pandas
    dt_heart = pd.read_csv('data/heart.csv')
  
    # Imprimimos un encabezado con los primeros 5 registros
    print(dt_heart.head())
    
    dt_features= dt_heart.drop(['target'],axis=1)
    dt_target=dt_heart['target']
    dt_features= StandardScaler().fit_transform(dt_features)
    X_train, X_test, y_train, y_test= train_test_split(dt_features,
                                                     dt_target, test_size= 0.3, random_state=40)
    
    
    kpca= KernelPCA(n_components=4, kernel='poly')# se puede cambiar el tipo de kernel, ver la documentación de sklearn
    #entrenar con los datos de entrenamiento
    kpca.fit(X_train)
    
    dt_train=kpca.transform(X_train)
    dt_test= kpca.transform(X_test)
    
    logistic= LogisticRegression(solver='lbfgs')
    
    logistic.fit(dt_train, y_train)
    
    print("SCORE PCA: ", logistic.score(dt_test, y_test))

    
    