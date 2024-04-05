import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
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
   print(X_train.shape)
   print(y_train.shape)
   # Si n_components no tiene valor asignado  sera = ()
   pca= PCA(n_components=3)
   pca.fit(X_train)
   
   ipca= IncrementalPCA(n_components=3, batch_size=10)
   ipca.fit(X_train)
   
   plt.plot(range(len(pca.explained_variance_)), pca.explained_variance_ratio_)
   
   logistic=LogisticRegression(solver='lbfgs')
   
   dt_train=pca.transform(X_train)
   dt_test=pca.transform(X_test)
   logistic.fit(dt_train, y_train)
   
   print("SCORE PCA: ", logistic.score(dt_test, y_test))
   