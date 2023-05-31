import math
import pickle
import numpy as np


#%precision 3


def weightedL2(a, b, w):
    if w:
        q = a - b
        return np.sqrt((w * q * q).sum())
    else:
        return np.linalg.norm(a - b)


def getNNdist(graph, m_art, oth_art, metrics, mweights):

    v1 = [graph[m_art][m] for m in metrics]
    v2 = [graph[oth_art][m] for m in metrics]

    v1 = [m if m else 1 for m in v1]
    v2 = [m if m else 1 for m in v2]

    v1 = [np.nan_to_num(m, 1) for m in v1]
    v2 = [np.nan_to_num(m, 1) for m in v2]

    n1 = np.linalg.norm([graph[m_art][m] for m in metrics if graph[m_art][m]])
    n2 = np.linalg.norm([graph[oth_art][m] for m in metrics if graph[oth_art][m]])

    d1, d2 = v1 / n1, v2 / n2
    nnd = weightedL2(d1, d2, mweights)

    return nnd


def get_best_match(graph, m_art, matchtype, alb_metrics, sound_metrics, mweights):
    best_match = None
    nn_dist = nn_timediff = 100000000000000
    nn_score = 0
    if m_art:
        for art in graph[m_art]:
            if art not in alb_metrics + sound_metrics + [
                "avg_sonics",
                "avg_releaseyear",
                "avg_score",
            ]:
                if matchtype == "sim":
                    sc = getNNdist(graph, m_art, art, sound_metrics, mweights)
                    if not np.isnan(sc):
                        if sc < nn_dist:
                            nn_dist = sc
                            best_match = art
                elif matchtype == "best":
                    sc = graph[art]["avg_score"]
                    if sc > nn_score:
                        nn_score = sc
                        best_match = art
                elif matchtype == "year":
                    nn_year = graph[m_art]["avg_releaseyear"]
                    sc = graph[art]["avg_releaseyear"]
                    if abs(sc - nn_year) < nn_timediff:
                        nn_year = sc
                        best_match = art

    return best_match


def isPropNoun(x, rev_corpus):
    blob_object = textblob.TextBlob(rev_corpus)
    parsed_rev = blob_object.tags
    nouns = [w[0] for w in parsed_rev if w[1] == "NNP"]
    return x in nouns


def get_net(df, excl_names, build=False, writeFolder=None):
    if build:
        # remove odd chrs
        for punct in ["/", "\\", "\x92", "\x86", "\xa0"]:
            df["review"] = df["review"].apply(lambda x: str(x).replace(punct, ""))
            df["artist"] = df["artist"].apply(lambda x: str(x).replace(punct, ""))

        # set of artists in the dataset
        artists = [
            a
            for a in df.artist.unique()
            if (type(a) != float and a not in excl_names and len(a) > 2)
        ]

        artist_infdict = {
            mentd_main_art: [] for mentd_main_art in artists
        }  # inicemos un dict para cada artista con lista vacia

        # Who did main_art influence?

        for mentd_main_art in artist_infdict:
            for art in artists:
                reviews = [
                    rev
                    for rev in list(df[df.artist == art]["review"])
                    if type(rev) != float
                ]
                if mentd_main_art != art:
                    for rev in reviews:
                        if len(mentd_main_art.split(" ")) == 1:
                            revl = rev.split()
                        else:
                            revl = rev
                        if mentd_main_art in revl:
                            if (
                                len(mentd_main_art.split(" ")) == 1
                            ):  # this is in order to avoid, for instance, artist "A" being counted every time the preposition "A" appears
                                if isPropNoun(mentd_main_art, rev):
                                    artist_infdict[mentd_main_art].append(art)
                            else:  # if we have a > 2 word artist name the above is almost surely not the case
                                artist_infdict[mentd_main_art].append(art)
        if writeFolder:
            with open(writeFolder, "wb") as handle:
                pickle.dump(artist_infdict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open(writeFolder, "rb") as handle:
            artist_infdict = pickle.load(handle)

    return artist_infdict


def get_count_nets(artist_infdict):

    artnet = {
        main_art: {ma: mntd_arts.count(ma) for ma in mntd_arts}
        for main_art, mntd_arts in artist_infdict.items()
    }

    for ma, d_cnts in artnet.items():
        artnet[ma] = dict(
            sorted(d_cnts.items(), key=lambda item: item[1], reverse=True)
        )

    art_infsums = {ma: sum(artnet[ma].values()) for ma, others_dict in artnet.items()}
    art_infsums = dict(
        sorted(art_infsums.items(), key=lambda item: item[1], reverse=True)
    )

    return artnet, art_infsums


# Add sonic / chrono / other numerical variables as artist attributes:
def add_metrics(df, adct, alb_metrics, sound_metrics):

    metrics = set(alb_metrics + sound_metrics)
    for art in adct:
        artdf = df[df.artist == art]
        for m in metrics:
            if m in df.columns:
                avg_m = artdf[m].mean()
                adct[art]["avg_" + m] = avg_m
            else:
                adct[art]["avg_" + m] = None

        avg_sonics = artdf[sound_metrics].mean(axis=1)
        adct[art]["avg_sonics"] = avg_sonics

    return adct
