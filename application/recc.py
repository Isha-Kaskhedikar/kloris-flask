from flask import Flask, request
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)


def cluster(og_df,light,minTemp,maxTemp,height,spread):
    categorical_features = ['light']

    dummy = {}
    dummy['id'] = 42
    dummy['scientific name'] = 'sample'
    dummy['common name'] = 'sample'
    dummy['light'] = light
    dummy['min temp'] = minTemp
    dummy['max temp'] = maxTemp
    dummy['height'] = height
    dummy['spread'] = spread

    for i in og_df.columns.tolist():
      og_df[i] = [re.sub(r'\n', '', str(t)) for t in og_df[i]]
      og_df[i] = [re.sub(r'\t', '', str(t)) for t in og_df[i]]

    df = og_df[['id','common name','scientific name','light','min temp','max temp','height','spread']]
    
    for col in df.columns:
      if col not in dummy.keys():
        dummy[col] = np.nan

    df_d = pd.DataFrame(dummy, index=[0])
    df_d.fillna(0, inplace=True)
    data = pd.concat([df,df_d])

    labels = data[['id', 'scientific name','common name']]
    data.drop(columns=['id', 'scientific name','common name'], inplace=True)
    
    data = pd.get_dummies(data, columns=categorical_features, drop_first=True, dummy_na=True)
    features = data.columns.size

    spec=DBSCAN(eps = 2,min_samples = features)
    sc = StandardScaler()
    data_sc = sc.fit_transform(data)
    spec.fit_predict(data_sc)

    data['cluster'] = spec.labels_

    og_df['cluster'] = spec.labels_[:len(spec.labels_)-1]
    out_cluster = spec.labels_[-1]
    
    data = pd.concat([labels, data], axis=1)
    # data.to_excel("DB_predicted.xlsx")
    temp = data.loc[data['cluster'] == out_cluster]
    output = og_df.loc[temp.index]

    return output


def tf_idf(cluster_df,use):
    uses = pd.DataFrame(cluster_df["uses"])
    uses = pd.concat([uses,pd.DataFrame({"uses":[use]})])
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(uses["uses"])
    cosine_similarities = linear_kernel(matrix,matrix)
    sim_scores = list(enumerate(cosine_similarities[-1]))
    # print("--",sim_scores)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:8]       #  top 7 reccos

    indices = [i[0] for i in sim_scores]
    only_scores = [i[1] for i in sim_scores]
    length = cluster_df.shape[0]
    if length in indices:
        indices.remove(length)
    
    return cluster_df.iloc[indices]

@app.route('/recommendations', methods=['POST','GET'])
def get_recommendations():
    # Load dataset
    og_df = pd.read_excel('plantsDB.xlsx')

    # Get user input
    user_input = request.get_json()

    light = user_input['light']
    minTemp = user_input['minTemp']   # from weather api
    maxTemp= user_input['maxTemp']   # from weather api
    height = user_input['height']
    spread = user_input['spread']
    use = user_input['use']       # can be none , in that case perfor only clustering
    # use="Vegetable"
    if use:
        cluster_df = cluster(og_df,light,minTemp,maxTemp,height,spread)
        # cluster_df = cluster(og_df,"Full Sun",20,30,4,2)
        final_df = tf_idf(cluster_df,use)
        return final_df.to_dict('dict')
        
    else:
        return cluster(og_df,"Full Sun",20,30,4,2).sample(10).to_dict('dict')


if __name__ == "__main__":
    app.run(debug=True, port=8000)