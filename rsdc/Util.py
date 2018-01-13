

def parse_artist_title(a_file_name):
    path = '%s/%s/' % (downloadDir, sub)
    track = file[len(path):-4]
    split = track.split('-')
    if len(split) > 2:
        a = split[0] + split[1]
        t = split[2]
    elif len(split) < 2:
        a = track
        t = ''
    elif len(split) == 2:
        a = split[0]
        t = split[1]
    else:
        split = file.split(' ')
        a = split[0]
        t = split - split[0]
    return (a, t)