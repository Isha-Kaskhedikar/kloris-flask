import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from itertools import combinations
import re,string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def recommend(titles,top_k):
    st="application/plantsDB.xlsx"
    data = pd.read_excel(st)
    data.fillna(" ",inplace=True)
    data['light'] = [re.sub(r'\n', '', t) for t in data['light']]
    data['water'] = [re.sub(r'\n', '', t) for t in data['water']]
    data['soil pH'] = [re.sub(r'\n', '', t) for t in data['soil pH']]
    data['flower time'] = [re.sub(r'\n', '', t) for t in data['flower time']]

    data['uses'] = [re.sub(r'\n', '', t) for t in data['uses']]
    data['common name'] = [re.sub(r'\n', '', t) for t in data['common name']]
    data['miscellaneous'] = [re.sub(r'\n', '', t) for t in data['miscellaneous']]

    data['light'] = [re.sub(' ','',t) for t in data['light']]
    data['water'] = [re.sub(' ','',t) for t in data['water']]
    data['soil pH'] = [re.sub(' ','',t) for t in data['soil pH']]
    data['flower time'] = [re.sub(' ','',t) for t in data['flower time']]

    data["details"] = data['light'] + '  ' + data['water'] + ' ' + data['soil pH'] + ' ' + data['flower time']

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(data["details"])
    cosine_similarities = linear_kernel(matrix,matrix)
    plant_id = data["id"]
    plant_label = data['label']
    plant_name = data['common name']
    plant_sci_name=data['scientific name']
    plant_image = data["image"]

    indices = pd.Series(data.index, index=data['common name'])

    title_dict={}    # key: index, value: movie_indices, similar plants indices to idx
    lst = []
    for title in titles:
      idx = indices[title]
      sim_scores = list(enumerate(cosine_similarities[idx]))
      sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
      sim_scores = sim_scores[1:top_k+1]
      movie_indices = [i[0] for i in sim_scores]
      lst.append(movie_indices)
      title_dict.update({idx:movie_indices})
    #   print("----",title_dict)
      # only_scores = [i[1] for i in sim_scores]
    common_list = list(set.intersection(*[set(x) for x in lst])) 
    # print(title_dict, common_list)
    if common_list:
      print(title_dict, common_list)
      return  [["From All Plants",
                plant_name.iloc[common_list].tolist(),
                plant_sci_name.iloc[common_list].tolist(),
                plant_id.iloc[common_list].tolist(),
                plant_image.iloc[common_list].tolist(),1000]]
    else:
      l=[]
      for k,v in title_dict.items():
        print(k)
        l.append([plant_label.iloc[k],
                  plant_name.iloc[v[:2]].tolist(),
                  plant_sci_name.iloc[v[:2]].tolist(),
                  plant_id.iloc[v[:2]].tolist(),
                  plant_image.iloc[v[:2]].tolist(),
                  int(plant_id.iloc[k])])
      return l




# if __name__ == "__main__":
#     app.run(debug=True, port=8000)