class SemanticSearch():

    def __init__(self,n_neighbors):
        # self.use = tensorflow_hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        # self.fitted = False
        # self.embeddings = embeddings
        self.n_neighbors = n_neighbors

    def fit(self, data, batch=1000):
        self.embeddings = data
        # global embeddings
        n_neighbors = min(self.n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        # self.fitted = True


    def __call__(self, text, data,return_data=True):
        inp_emb = text

        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [data[i] for i in neighbors]
        else:
            return neighbors


    # def get_text_embedding(self, texts, batch=1000):
    #     embeddings = []
    #     for i in tqdm(range(0, len(texts), batch)):
    #         text_batch = texts[i:(i+batch)]
    #         emb_batch = self.use(text_batch)
    #         embeddings.append(emb_batch)
    #     embeddings = np.vstack(embeddings)
    #     return embeddings

