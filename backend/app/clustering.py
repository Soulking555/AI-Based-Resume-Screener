from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from app.database import candidates_collection

def run_clustering(num_clusters=3):
    rows = list(candidates_collection.find({}, {"_id": 1, "resume_text": 1}))
    
    if len(rows) < num_clusters:
        return {"message": "Not enough candidates to cluster. Need at least 3."}
        
    ids = [r["_id"] for r in rows]
    texts = [r["resume_text"] for r in rows]
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # We can assign human readable names based on top terms per cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    cluster_names = {}
    for i in range(num_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :3]]
        cluster_names[i] = f"Group: {', '.join(top_terms)}"
    
    for doc_id, label in zip(ids, labels):
        candidates_collection.update_one(
            {"_id": doc_id},
            {"$set": {"cluster": cluster_names[label]}}
        )
        
    return {"message": "Clustering complete", "clusters": cluster_names}
