def plot_tsne(data, labels):

    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    """ Input: 
            - model weights to fit into t-SNE
            - labels (no one hot encode)
            - num_classes
    """
    n_components = 2

    tsne = TSNE(n_components=n_components, init='pca', perplexity=5, random_state=0)
    tsne_res = tsne.fit_transform(data)

    v = pd.DataFrame(data,columns=[str(i) for i in range(data.shape[1])])
    v['Class'] = labels
    v['Class'] = v['Class'].apply(lambda i: ['email', 'video', 'videocall', 'webpage'][i])
    # v['label'] = v['y'].apply(lambda i: ['email', 'video', 'videocall', 'webpage'][i])
    v["t1"] = tsne_res[:,0]
    v["t2"] = tsne_res[:,1]

    sns.scatterplot(
        x="t1", y="t2",
        hue="Class",
        palette=sns.color_palette(["#52D1DC", "#FF7800", "#E44658", "#63C100"]),#, "#E44658", "#63C100", "#FF7800"]),
        legend=True,
        data=v,
    )
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('')
    plt.ylabel('')
    plt.show()

def plot_confusion_matrix(matrix):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    index = ['Email', 'Video', 'VideoCall', 'WebPage']

    df_cm = pd.DataFrame(matrix, index=index, columns=index)

    cmap = sns.cubehelix_palette(light=1, as_cmap=True)

    res = sns.heatmap(df_cm, annot=True, vmin=0, vmax=20, cmap=cmap)

    plt.yticks([0.5,1.5,2.5,3.5], index, va='center')

    plt.title('Confusion Matrix')
    plt.show()