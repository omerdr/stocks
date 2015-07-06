import pickle
from matplotlib import pyplot as plt
from numpy import mean, std, median

RANKING_FILE_NAME = 'data/ranking_tmp.pkl'  # 3m,6m,1yr

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def draw_hist(values):
        h = plt.hist(v, bins=20, range=(0.2, 2.0), facecolor='green')  #, normed=1, alpha=0.5)
        m = mean(ranking[k])
        med = median(ranking[k])
        s = std(ranking[k])
        max_count = max(h[0])
        plt.axvline(m, color='r', linestyle='-')
        plt.axvline(m+s, color='r', linestyle='--')
        plt.axvline(m-s, color='r', linestyle='--')
        plt.axvline(med, color='b', linestyle='-')
        #plt.text(100, 0, "mu=%.2g, std=%.2g" % (m,s))
        plt.annotate("%0.4g" % m, xy=(m, max_count-5))
        plt.annotate("%0.4g" % (m+s), xy=(m+s, max_count-5))
        plt.annotate("%0.4g" % med, xy=(med, max_count-8))
        # plt.annotate('mean', xy=(m, max_count), xytext=(m-0.2, max_count+5),
        #     arrowprops=dict(facecolor='black', shrink=0.05))

        # Prettify
        #plt.suptitle(k)
        plt.title("Rank: %s, median: %0.4g, mean: %0.4g, std: %0.4g" % (k,med,m,s))
        plt.xlabel('1-year Percentage Change')
        plt.ylabel('Count')
        plt.subplots_adjust(left=0.15) # tweak spacing to prevent clipping of y-label
        plt.show()
        # plt.savefig('data/hists/' + k + '.jpg')
        # plt.close()
        # print k


def main():
    ranking = load_obj(RANKING_FILE_NAME)
    for k, v in ranking.iteritems():
        if len(v) < 50:
            continue

        draw_hist(v)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass