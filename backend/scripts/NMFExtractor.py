# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import NMF
#
#
#
# def display_topics(model, feature_names, no_top_words):
#     for topic_idx, topic in enumerate(model.components_):
#         print("Topic %d:" % topic_idx)
#         print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
#
#
# def NMF_topics_extractor(documents):
#     no_features = 1000
#     no_topics = 20
#     tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
#     tfidf = tfidf_vectorizer.fit_transform(documents)
#     tfidf_feature_names = tfidf_vectorizer.get_feature_names()
#
#     nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
#
#
# # display_topics(nmf, tfidf_feature_names, no_top_words)