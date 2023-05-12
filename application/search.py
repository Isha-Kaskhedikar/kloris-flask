## for data
import pandas as pd
import numpy as np
## for nlp
from sklearn import feature_extraction, metrics

dtf_right = pd.read_excel("D:/RNH/kloris/kloris-flask/application/plantsDB.xlsx")
a="s"
lst_b = dtf_right.iloc[:,1].tolist()  #list of strings

vectorizer = feature_extraction.text.CountVectorizer()
X = vectorizer.fit_transform([a]+lst_b).toarray()
lst_vectors = [vec for vec in X]
cosine_sim = metrics.pairwise.cosine_similarity(lst_vectors)

scores = cosine_sim[0][1:]

threshold = 0.7
match_scores = scores[scores >= threshold]
match_idxs = [i for i in np.where(scores >= threshold)[0]] 
match_strings = [lst_b[i] for i in match_idxs]

top = 3
dtf_match = pd.DataFrame(match_scores, columns=[a], 
                         index=match_strings)
dtf_match = dtf_match[~dtf_match.index.duplicated(keep='first')
                 ].sort_values(a, ascending=False).head(top)

print(dtf_match[a].index.tolist())