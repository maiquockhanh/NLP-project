import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from getCorpusFromGG import searchGG, getContents

def vectorize(Text):
    return TfidfVectorizer().fit_transform(Text).toarray()


def similarity(doc1, doc2):
    return cosine_similarity([doc1, doc2])

filename = input('Enter the student file name you want to check: ')
text_input = open(filename, encoding='utf-8').read()
percent = float(input("Enter the percentage: "))/100

db = searchGG(text_input)
db = getContents(db)

print(db['content'])

vector_sample = [i for i in db['content']]
vector_sample.append(text_input)

per_list = []

vectors = vectorize(vector_sample)

text_input_vector = vectors[-1]

db['vector'] = vectors[:-1].tolist()

for i in range(len(db.index)):
    print(i)
    sim_score = similarity(text_input_vector, db['vector'][i])[0][1]
    per_list.append(sim_score)

db['percentage'] = per_list

db = db.drop('vector',1)
db = db.drop('content',1)
db = db.sort_values(by=['percentage'], ascending=False)

# print(db.loc[db['percentage'] >= percent])

db.to_csv(
    'result.csv', encoding='utf-8', index=False)
