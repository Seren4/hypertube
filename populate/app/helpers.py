
def prct(idx_loop, max_loop):
    return (100 * idx_loop) / max_loop


def generate_magnet(hash):
    magnet = "magnet:?xt=urn:btih:{hash}&{trackers}".format(hash=hash, trackers="&tr=".join(t for t in get_trackers()))
    return magnet


def get_trackers():
    return [
        "udp://glotorrents.pw:6969/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://torrent.gresille.org:80/announce",
        "udp://tracker.openbittorrent.com:80",
        "udp://tracker.coppersurfer.tk:6969",
        "udp://tracker.leechers-paradise.org:6969",
        "udp://p4p.arenabg.ch:1337",
        "udp://tracker.internetwarriors.net:1337"
    ]
