import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    yokohama_pd = pd.read_csv("budget_yokohama.csv")
    sapporo_pd = pd.read_csv("budget_sapporo.csv")

    min_val = yokohama_pd['予算'].min()
    max_val = yokohama_pd['予算'].max()
    bins = np.arange(0, max_val + 500, 500)
    plt.hist(yokohama_pd['予算'], bins=bins, density=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, np.mean(yokohama_pd['予算']), np.std(yokohama_pd['予算']))
    plt.plot(x, p, 'k', linewidth=2)
    plt.title("average budget around yokohama st.")
    plt.show()

    w, p = stats.shapiro(yokohama_pd['予算'].dropna())
    print(f"W: {w}, p value: {p}\n")

    stats.probplot(yokohama_pd['予算'].dropna(), dist='norm', plot=plt)
    plt.title("QQ plot (yokohama)")
    plt.show()
    
    freq, edges = np.histogram(yokohama_pd['予算'], bins=bins)
    hist_df = pd.DataFrame({
        "lower lim": edges[:-1],
        "upper lim": edges[1:],
        "freq": freq
    })
    print(hist_df, "\n")
    hist_df.to_csv("hist_yokohama.csv", index=False)

    mean = np.nanmean(yokohama_pd['予算'])
    median = np.nanmedian(yokohama_pd['予算'])
    mode_idx = np.argmax(freq)
    mode = edges[mode_idx] + 250
    stdev = np.std(yokohama_pd['予算'])
    coeff = stdev / mean

    data = yokohama_pd['予算'].dropna()
    ubstd = np.std(data, ddof=1)
    n = len(data)
    skew = (n / ((n - 1) * (n - 2))) * np.sum((yokohama_pd['予算'].dropna() / stdev) ** 3)
    se = ubstd / np.sqrt(n)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
    print(f"reliable range: {ci[0]} <= budget <= {ci[1]}\n")

    repre_df = pd.DataFrame([{
        "mean": mean,
        "median": median,
        "mode": mode,
        "stdev": stdev,
        "coeff": coeff,
        "ubstd": ubstd,
        "skew": skew,
        "W": w,
        "p": p,
        "n": n
    }])
    print(repre_df, "\n")
    repre_df.to_csv("representatives_yokohama.csv", index=False)

    plt.clf()
    
    min_val = sapporo_pd['予算'].min()
    max_val = sapporo_pd['予算'].max()
    bins = np.arange(0, max_val + 500, 500)
    plt.hist(sapporo_pd['予算'], bins=bins, density=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, np.mean(sapporo_pd['予算']), np.std(sapporo_pd['予算']))
    plt.plot(x, p, 'k', linewidth=2)
    plt.title("average budget around sapporo st.")
    plt.show()

    w, p = stats.shapiro(sapporo_pd['予算'].dropna())
    print(f"W: {w}, p value: {p}\n")

    stats.probplot(sapporo_pd['予算'].dropna(), dist='norm', plot=plt)
    plt.title("QQ plot (yokohama)")
    plt.show()
    
    freq, edges = np.histogram(sapporo_pd['予算'], bins=bins)
    hist_df = pd.DataFrame({
        "lower lim": edges[:-1],
        "upper lim": edges[1:],
        "freq": freq
    })
    print(hist_df, "\n")
    hist_df.to_csv("hist_sapporo.csv", index=False)

    mean = np.nanmean(sapporo_pd['予算'])
    median = np.nanmedian(sapporo_pd['予算'])
    mode_idx = np.argmax(freq)
    mode = edges[mode_idx] + 250
    stdev = np.std(sapporo_pd['予算'])
    coeff = stdev / mean

    data = sapporo_pd['予算'].dropna()
    ubstd = np.std(data, ddof=1)
    n = len(data)
    skew = (n / ((n - 1) * (n - 2))) * np.sum((sapporo_pd['予算'].dropna() / stdev) ** 3)
    se = ubstd / np.sqrt(n)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
    print(f"reliable range: {ci[0]} <= budget <= {ci[1]}\n")

    repre_df = pd.DataFrame([{
        "mean": mean,
        "median": median,
        "mode": mode,
        "stdev": stdev,
        "coeff": coeff,
        "ubstd": ubstd,
        "skew": skew,
        "W": w,
        "p": p,
        "n": n
    }])
    print(repre_df, "\n")
    repre_df.to_csv("representatives_sapporo.csv", index=False)