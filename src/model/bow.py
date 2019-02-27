from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import GradientBoostingClassifier

def bow_pipeline(X_train, y_train):
    pipeline = Pipeline([    
    ('countvect', CountVectorizer(analyzer='word',
                                    min_df=0.0,
                                    max_df=0.7,
                                    ngram_range=(1,2))),
    ('GradientBoosting', GradientBoostingClassifier(n_estimators=200))
    ])
    model = pipeline.fit(X_train,y_train)
    return model
