import pandas as pd

from pykt.preprocess.utils import (
    change2timestamp,
    format_list2str,
    sta_infos,
    write_txt,
)

KEYS = ["student_id", "skills", "question_id"]
COLS = KEYS + ["submission_time", "correct", "response_time"]


def read_data_from_csv(read_file, write_file):
    stares = []
    df = pd.read_csv(read_file, low_memory=False, usecols=COLS + ["id"])

    ins, us, qs, cs, avgins, avgcq, na = sta_infos(df, KEYS, stares)
    print(
        f"original interaction num: {ins}, user num: {us}, question num: {qs}, concept num: {cs}, avg(ins) per s: {avgins}, avg(c) per q: {avgcq}, na: {na}"
    )

    df["correct"] = df["correct"].astype(int)
    df["submission_time"] = df["submission_time"].apply(
        lambda x: change2timestamp(x, hasf="." in x)
    )
    df["response_time"] = (df["response_time"] * 1000).astype(int)
    df = df.dropna()

    ins, us, qs, cs, avgins, avgcq, na = sta_infos(df, KEYS, stares)
    print(
        f"original interaction num: {ins}, user num: {us}, question num: {qs}, concept num: {cs}, avg(ins) per s: {avgins}, avg(c) per q: {avgcq}, na: {na}"
    )
    user_inters = []
    for user, group in df.groupby("student_id", sort=False):
        group = group.sort_values(["submission_time", "id"])
        seq_skills = group["skills"].tolist()
        seq_ans = group["correct"].tolist()
        seq_response_cost = group["response_time"].tolist()
        seq_start_time = group["submission_time"].tolist()
        seq_problems = group["question_id"].tolist()
        seq_len = len(group)

        assert seq_len == len(seq_skills) == len(seq_ans)

        user_inters.append(
            [
                [str(user), str(seq_len)],
                format_list2str(seq_problems),
                format_list2str(seq_skills),
                format_list2str(seq_ans),
                format_list2str(seq_start_time),
                format_list2str(seq_response_cost),
            ]
        )

    write_txt(write_file, user_inters)
    print("\n".join(stares))


if __name__ == "__main__":
    read_file = "problem_logs.csv"
    read_data_from_csv(read_file, "data.txt")
