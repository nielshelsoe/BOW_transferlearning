import gensim
from src.data.load_data import load_trustpilot_data
from src.preprocessing.text_pre import clean_text
df_trust = load_trustpilot_data()
df_trust = clean_text(df_trust, 'features')

def gensim_list(df):
    for index,row in df.iterrows():
        yield gensim.utils.simple_preprocess (row['features'])

documents = list (gensim_list (df_trust))

model = gensim.models.Word2Vec(
        documents,
        size=150,
        window=10,
        min_count=2,
        workers=10)
model.train(documents, total_examples=len(documents), epochs=10)

model.save('../../data/models/word2vec.model')