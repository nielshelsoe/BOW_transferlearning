from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def get_metrics(model, X_test, y_test):
    y_pre = model.predict(X_test)

    print('roc_auc_score')
    print(roc_auc_score(y_test, y_pre))
    print('-------------------')
    print('classification_report')
    print(classification_report(y_test, y_pre))
    print('-------------------')
    print('confusion_matrix')
    print(confusion_matrix(y_test,y_pre))
    print('-------------------')
