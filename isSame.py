import pandas as pd
from scipy import stats

if __name__ == "__main__":
    yokohama_pd = pd.read_csv("representatives_yokohama.csv")
    sapporo_pd = pd.read_csv("representatives_sapporo.csv")

    y_mean = yokohama_pd["mean"][0]
    s_mean = sapporo_pd["mean"][0]

    y_ubstd = yokohama_pd["ubstd"][0]
    y_ubvar = y_ubstd ** 2
    s_ubstd = sapporo_pd["ubstd"][0]
    s_ubvar = s_ubstd ** 2
    print(f"y_ubvar: {y_ubvar}, s_ubvar: {s_ubvar}")

    yn = yokohama_pd["n"][0]
    sn = sapporo_pd["n"][0]
    print(f"yn: {yn}, sn: {sn}")

    df1 = yn - 1 if y_ubvar > s_ubvar else sn - 1
    df2 = sn - 1 if y_ubvar > s_ubvar else yn - 1

    f = y_ubvar / s_ubvar if y_ubvar > s_ubvar else s_ubvar / y_ubvar
    f_lim = stats.f.ppf(1 - 0.05, df1, df2)

    print(f"F value: {f}, limit F value: {f_lim}")
    print(f"F value {"≦ " if (f <= f_lim) else ">"} limit F value")
    print(f, "≦ " if (f <= f_lim) else ">", f_lim)
    
    dif_t = abs((y_mean - s_mean) / ((((yn - 1) * y_ubvar + (sn - 1) * s_ubvar) / ((yn - 1) + (sn - 1)) * (1 / yn + 1 / sn)) ** (1/2)))
    t = stats.t.ppf(1 - 0.025, yn + sn - 2)
    print(f"dif_t: {dif_t}, t: {t}")
    print(f"dif_t {"≦ " if (dif_t <= t) else ">"} t")
    print(dif_t, "≦ " if (dif_t <= t) else ">", t)