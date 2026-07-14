
# Summer 2026
# Assignment 2 - Process Monitor
# Sources:
# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
# https://www.geeksforgeeks.org/python-pandas-dataframe-groupby/
# https://psutil.readthedocs.io/
#

import time
import os
import psutil
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# Obtain a list of running processes
# ----------------------------------------------------------
def list_processes(sort_column="Memory %"):
    proc_list = []

    for proc in psutil.process_iter():
        try:
            pid = proc.pid
            ppid = proc.ppid()
            username = proc.username()
            name = proc.name()
            status = proc.status()

            mem_pct = proc.memory_percent()

            cpu_times = proc.cpu_times()
            cpu_time = cpu_times.user + cpu_times.system

            proc_list.append(
                (
                    pid,
                    ppid,
                    username,
                    name,
                    status,
                    mem_pct,
                    cpu_time
                )
            )

        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
        ):
            pass

    columns = [
        "PID",
        "PPID",
        "Username",
        "Name",
        "Status",
        "Memory %",
        "CPU Time"
    ]

    df = pd.DataFrame(proc_list, columns=columns)

    if sort_column in df.columns:
        df = df.sort_values(
            by=sort_column,
            ascending=False
        )

    return df


# ----------------------------------------------------------
# Display process table
# ----------------------------------------------------------
def display_processes(df, top_n=20):
    print("\nTOP PROCESSES\n")
    print(df.head(top_n).to_string(index=False))


# ----------------------------------------------------------
# Create HTML report
# ----------------------------------------------------------
def create_html_report(df):

    html_content = f"""
    <html>
    <head>
        <title>Assignment02 - Process Monitor</title>
    </head>
    <body>
        <h1>Process Monitor Report</h1>
        {df.to_html(index=False)}
    </body>
    </html>
    """

    with open("Assignment02.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Assignment02.html created successfully")
    print("HTML location:", os.path.abspath("Assignment02.html"))


# ----------------------------------------------------------
# Create bar graph
# ----------------------------------------------------------
def create_graph(df,
                 metric="Memory %",
                 top_n=10):

    top_df = df.head(top_n)

    plt.figure(figsize=(12, 6))

    labels = (
        top_df["Name"]
        + " ("
        + top_df["PID"].astype(str)
        + ")"
    )

    plt.bar(
        labels,
        top_df[metric]
    )

    plt.title(
        f"Top {top_n} Processes by {metric}"
    )

    plt.xlabel("Process")
    plt.ylabel(metric)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("Assignment02.png")

    print("Assignment02.png created successfully")
    print("PNG location:", os.path.abspath("Assignment02.png"))

    plt.show()


# ----------------------------------------------------------
# Group processes by username
# ----------------------------------------------------------
def summarize_by_user(df):

    print("\nPROCESS COUNT BY USERNAME\n")

    grouped = (
        df.groupby("Username")
        .size()
        .reset_index(name="Process Count")
        .sort_values(
            by="Process Count",
            ascending=False
        )
    )

    print(grouped.to_string(index=False))


# ----------------------------------------------------------
# Refresh process list at fixed intervals
# ----------------------------------------------------------
def run_monitor(
        interval_seconds=5,
        iterations=3,
        sort_column="Memory %"
):

    for i in range(iterations):

        print("\n" + "=" * 70)
        print("REFRESH", i + 1)
        print("=" * 70)

        df = list_processes(sort_column)

        display_processes(df)

        summarize_by_user(df)

        time.sleep(interval_seconds)

    return df


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
def main():

    print("Process Monitor Starting...\n")

    df = run_monitor(
        interval_seconds=5,
        iterations=3,
        sort_column="Memory %"
    )

    print("\nFinished monitoring processes.\n")

    create_html_report(df)

    create_graph(
        df,
        metric="Memory %",
        top_n=10
    )


if __name__ == "__main__":
    main()