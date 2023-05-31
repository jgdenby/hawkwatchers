import random as rd
import pickle

from Stellar import ktechnets as ktch
from Stellar import path_searching as ps

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os

os.environ["SPOTIPY_CLIENT_ID"] = "2264f498fc3b44b897dec6e300ba3974"
os.environ["SPOTIPY_CLIENT_SECRET"] = "720541f593de483bafe58fcd1d70c847"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:1410/"


D = 1
R = False

excl_names = [
    "Various Artists",
    "Love",
    "Owen",
    "Joey Bada$$",
    "+/-",
    "Air",
    "!!!  Out Hud",
    "!!! / Out Hud",
    "James",
    "America",
    "Canada" "Death",
    "Love",
    "Dave",
    "Girls",
    "Lee",
    "Home",
    "George",
    "South",
    "Earth",
    "Songs",
    "Stars",
    "Ghost",
]

alb_metrics = ["releaseyear", "score"]
sound_metrics = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

### Helper functions
def load_artnet(
    filepath="Stellar/artnetUND-2023-merged.pickle",
    direct=True,
    excl_names=None,
):
    if not direct:
        artinfdict = ktch.get_net(df, excl_names, build=False, writeFolder=filepath)
        artnet, art_infsums = ktch.get_count_nets(artinfdict)
        artnet = ktch.add_metrics(df, artnet, alb_metrics, sound_metrics)
    else:
        with open(filepath, "rb") as handle:
            artnet = pickle.load(handle)

    return artnet


def getpath(artnet, tgnode, avg_sound_metrics, dist_thresh, rand, k):

    art_path = ps.bfk(
        artnet,
        tgnode,
        metrics=avg_sound_metrics,
        mweights=None,  # [1 for s in avg_sound_metrics]
        dist_thresh=dist_thresh,
        rand=rand,
        k=k,
    )

    art_pathcln = []
    for art in art_path:
        if "  " in art:
            arts = art.split("  ")
            art_pathcln.append(arts[0])
            art_pathcln.append(arts[1])
        else:
            art_pathcln.append(art)

    return list(set(art_pathcln))


####

scope = "playlist-modify-public"
username = "elena.badillo.g"  #'1276781402'
token = SpotifyOAuth(scope=scope, username=username)
# token = 'BQA2FOasRLOkyizQ72_QFHwOahpnY_mBj5R1eWhPqvLPfWDInraKVKj9a0l4Bb1BJr1V-1FSJ-CTl-RTSr2SEpZrbnmJwlaZcGHwrDdeSqGAl8-lnyvruXniEmsL_A4T76HVFnC-zmSwVKbeTsKr2j7hHuAatp2Jj2wJ0DdvW5sH7odzSrhwR-5DhlHIRm0m86TaZyJOktsx2ivLsh-jBbeW6AwEvJrszWVNNWXTPhG8v47w7CLTaI1hSbSc580MotAAHpNNKSKDd6MIeIk'

spotifyObject = spotipy.Spotify(auth_manager=token)

###


avg_alb_metrics = ["avg_" + x for x in alb_metrics]
avg_sound_metrics = ["avg_" + x for x in sound_metrics]


artnet = load_artnet(
    excl_names=excl_names
)  # "artist_infdict-2022.pickle" if not direct


def get_playlist(tgnode, method, size):

    method = None
    size = int(size)

    if tgnode.lower() == "idk":
        tgnode = rd.choice(list(artnet.keys()))

    if tgnode in artnet:

        playlist_desc = "A playlist based on " + tgnode + " ~ by KTechNets©"
        playlist_name = "<<" + tgnode + ">>KTechNet"

        spotifyObject.user_playlist_create(
            user=username, name=playlist_name, description=playlist_desc
        )

        art_pathcln = getpath(
            artnet,
            tgnode,
            avg_sound_metrics=avg_sound_metrics,
            dist_thresh=D,
            rand=R,
            k=size,
        )

        mxc = 0

        while len(art_pathcln) < size + 1:

            art_pathclnO = art_pathcln
            art_pathcln2 = getpath(
                artnet, tgnode, avg_sound_metrics, dist_thresh=D * 10, rand=True, k=size
            )
            art_pathcln = list(set(art_pathcln + art_pathcln2))
            if art_pathcln == art_pathclnO:
                mxc += 1
            if mxc > 3:
                break

        ###

        artID_path = []
        for art in art_pathcln:
            try:
                artID_path.append(
                    spotifyObject.search(
                        art, limit=1, offset=0, type="artist", market=None
                    )["artists"]["items"][0]["id"]
                )
            except:
                pass

        tracklist = []
        for art in artID_path:
            try:
                t = rd.choice(
                    list(spotifyObject.artist_top_tracks(art, country="US")["tracks"])
                )
                tracklist.append(t["id"])
            except:
                pass

        tracklist = list(set(tracklist))
        prePlaylist = spotifyObject.user_playlists(user=username)
        playlist = prePlaylist["items"][0]["id"]

        spotifyObject.user_playlist_add_tracks(
            user=username, playlist_id=playlist, tracks=tracklist
        )

        plink = "https://open.spotify.com/playlist/" + playlist

        return True, art_pathcln, tgnode, plink

    else:
        return (
            False,
            [],
            "Oops :( This artist is not on our radar (yet) Maybe try another one?..",
            "",
        )


# Next:
# match qneigbor artist's song AND target artist's album which coinnected them with qneighboor
##music numbers (the song that brst fits the album in question)
# build a monthly personal net and sort by kcentrality: that's the pay disyribution sggestion
# an option to "zoom" into a given artist
