from myutils import load_obj, draw_hist_with_stats

RANKING_FILE_NAME = 'data/ranking_tmp.pkl'  # 3m,6m,1yr

def main():
    ranking = load_obj(RANKING_FILE_NAME)
    for k, v in ranking.iteritems():
        if len(v) < 50:
            continue

        draw_hist_with_stats(v)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass