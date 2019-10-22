
def load_data(path):
    players = []
    with open(path) as f:
        for line in f:
            data = line.split(',');
            stats = [];
            for stat in data[5:]:
                if stat == '':
                    stat = 0;
                try:
                    stats.append(float(stat));
                except ValueError:
                    continue;
            players.append(stats);
    return players[1:];
