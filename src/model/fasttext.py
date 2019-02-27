from src.model.sciWrapFasttext import sk_Fasttext
from sklearn.pipeline import Pipeline

def fasttext_pipeline(X_train=None, y_train=None, load_model_params=None):
    if load_model_params:
        model = sk_Fasttext(
                                            #word featurs
                                            minCount=5,
                                            minCountLabel=0,
                                            wordNgrams=2,
                                            bucket = 2000000,
                                            minn=0,
                                            maxn=0,
                                            #training fatures
                                            lr= 0.25,
                                            lrUpdateRate = 100,
                                            dim = 140,
                                            ws = 4,
                                            epoch = 150, 
                                            neg = 0,
                                            loss = 'softmax',
                                            thread = 12
                                            )
        return model
    else:
        pipeline = Pipeline([
                    ("fastText", sk_Fasttext(
                                            #word featurs
                                            minCount=5,
                                            minCountLabel=0,
                                            wordNgrams=2,
                                            bucket = 2000000,
                                            minn=0,
                                            maxn=0,
                                            #training fatures
                                            lr= 0.25,
                                            lrUpdateRate = 100,
                                            dim = 140,
                                            ws = 4,
                                            epoch = 150, 
                                            neg = 0,
                                            loss = 'softmax',
                                            thread = 12
                                            ))
                            ])
        
        model = pipeline.fit(X_train,y_train)
        return model
