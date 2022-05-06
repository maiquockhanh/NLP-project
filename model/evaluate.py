import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from getCorpusFromGG import searchGG, getContents
import copy

def vectorize(Text):
    return TfidfVectorizer().fit_transform(Text).toarray()

def similarity(doc1, doc2):
    return cosine_similarity([doc1, doc2])

def run_eval(links, text_input):
    contents = getContents(links)
    db = pd.DataFrame (contents, columns = ['content'])
    #db['links'] = links

    vector_sample = [i for i in db['content']]
    vector_sample.append(text_input)

    per_list = []

    vectors = vectorize(vector_sample)

    text_input_vector = vectors[-1]

    db['vector'] = vectors[:-1].tolist()

    for i in range(len(db.index)):
        sim_score = similarity(text_input_vector, db['vector'][i])[0][1]
        per_list.append(sim_score)

    db['percentage'] = per_list

    db = db.drop('vector',1)
    db = db.drop('content',1)
    db_copy = copy.deepcopy(db)
    sorted_key = db_copy.sort_values(by=['percentage'], ascending=False)
    sorted_key_list = [i for i in sorted_key.index]
    # rank = [-1 for index in range(len(sorted_key_list))]
    
    # for index in range(len(sorted_key_list)):
    #     rank[int(sorted_key_list[index])] = index
    
    arr = sorted(range(len(sorted_key_list)), key = lambda k:sorted_key_list[k])
    
    db['sorted_key_list'] = sorted_key_list    
    
    print(db.to_json(orient = 'records'))

    return db.to_json(orient = 'records')

    # print(db.loc[db['percentage'] >= percent])

    # db.to_csv(
    #     'result.csv', encoding='utf-8', index=False)