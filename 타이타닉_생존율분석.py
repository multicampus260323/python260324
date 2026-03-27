import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_and_clean_titanic_data():
    # seaborn 내장 타이타닉 데이터셋 로드
    df = sns.load_dataset("titanic")

    # 필요한 열만 선택
    df = df[["sex", "survived"]].copy()

    # 결측치 제거
    df = df.dropna(subset=["sex", "survived"])

    # sex 컬럼을 문자열로 변환(안정성)
    df["sex"] = df["sex"].astype(str)

    return df


def calculate_survival_rate(df):
    survival_rate_by_sex = (
        df.groupby("sex")["survived"]
        .mean()
        .reset_index()
        .rename(columns={"survived": "survival_rate"})
    )
    return survival_rate_by_sex


def plot_survival_rate(survival_rate_by_sex):
    plt.figure(figsize=(8, 6))

    x = survival_rate_by_sex['sex']
    y = survival_rate_by_sex['survival_rate']

    bars = plt.bar(x, y, color=['skyblue', 'lightcoral'])
    plt.ylim(0, 1)
    plt.title('Titanic Survival Rate by Sex')
    plt.xlabel('Sex')
    plt.ylabel('Survival Rate')

    for bar, rate in zip(bars, y):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.02, f'{rate:.2f}',
                 ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('titanic_survival_rate.png', dpi=150)
    plt.show()


def plot_survival_counts(df):
    plt.figure(figsize=(8, 6))

    grouped = df.groupby(['sex', 'survived']).size().unstack(fill_value=0)
    labels = ['male', 'female'] if 'male' in df['sex'].values and 'female' in df['sex'].values else grouped.index.tolist()

    x = list(range(len(labels)))
    width = 0.35

    dead = grouped.loc[labels, 0]
    survived = grouped.loc[labels, 1]

    plt.bar([i - width/2 for i in x], dead.values, width=width, label='No', color='salmon')
    plt.bar([i + width/2 for i in x], survived.values, width=width, label='Yes', color='mediumseagreen')

    plt.title('Titanic Survival Count by Sex')
    plt.xlabel('Sex')
    plt.ylabel('Count')
    plt.xticks(x, labels)
    plt.legend(title='Survived')

    for idx, label in enumerate(labels):
        d = dead[label]
        s = survived[label]
        plt.text(idx - width/2, d + 5, str(d), ha='center')
        plt.text(idx + width/2, s + 5, str(s), ha='center')

    plt.tight_layout()
    plt.savefig('titanic_survival_counts.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    data = load_and_clean_titanic_data()
    print("Data sample:")
    print(data.head())

    survival_rate = calculate_survival_rate(data)
    print("\nSurvival rate by sex:")
    print(survival_rate)

    plot_survival_rate(survival_rate)
    plot_survival_counts(data)
