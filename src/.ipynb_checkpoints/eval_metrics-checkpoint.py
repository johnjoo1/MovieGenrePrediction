def precision_recall(gt,preds):
    TP=0
    FP=0
    FN=0
    for t in gt:
        if t in preds:
            TP+=1
        else:
            FN+=1
    for p in preds:
        if p not in gt:
            FP+=1
    if TP+FP==0:
        precision=0
    else:
        precision=TP/float(TP+FP)
    if TP+FN==0:
        recall=0
    else:
        recall=TP/float(TP+FN)
    return precision,recall

def generate_predictions(Genre_ID_to_name, X_test, preds):
    genre_list=sorted(list(Genre_ID_to_name.keys()))
    predictions=[]
    for i in range(X_test.shape[0]):
        pred_genres=[]
        movie_label_scores=preds[i]
        for j in range(len(genre_list)):
            #print j
            if movie_label_scores[j]!=0:
                genre=Genre_ID_to_name[genre_list[j]]
                pred_genres.append(genre)
        predictions.append(pred_genres)
    return predictions

def precsc_recs(test_movies, movies_with_overviews, Genre_ID_to_name, predictions):
    precs=[]
    recs=[]
    for i in range(len(test_movies)):
        if i%1==0:
            pos=test_movies[i]
            test_movie=movies_with_overviews[pos]
            gtids=test_movie['genre_ids']
            gt=[]
            for g in gtids:
                g_name=Genre_ID_to_name[g]
                gt.append(g_name)
    #         print predictions[i],movies_with_overviews[i]['title'],gt
            a,b=precision_recall(gt,predictions[i])
            precs.append(a)
            recs.append(b)
    return precs, recs



