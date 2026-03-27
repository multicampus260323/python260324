import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows 환경에서 작동)
font_path = 'C:/Windows/Fonts/malgun.ttf'
if font_manager.findfont(font_manager.FontProperties(fname=font_path)):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
else:
    # 시스템에 한글 폰트가 없을 때 fall-back, 데스크탑 환경에선 설치 필요
    rc('font', family='DejaVu Sans')

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False


def load_and_clean(file_path):
    # 첫 번째 시트에 년도별 통계가 들어있음
    df = pd.read_excel(file_path, sheet_name=0)

    # 첫 열 이름을 알아보기 쉬운 이름으로 설정
    first_col = df.columns[0]
    df = df.rename(columns={first_col: '지표'})

    # 연도 컬럼: 숫자 형태만 (1970~2025)
    year_cols = [c for c in df.columns if str(c).strip().isdigit()]
    df = df[['지표'] + year_cols]

    # 수치로 변환 (가능한 경우)
    df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

    # 지표 이름 정리 (공백 제거)
    df['지표'] = df['지표'].astype(str).str.strip()

    return df, year_cols


def select_series(df):
    # 출생아수/합계출산율을 포함하는 행 찾기
    birth_mask = df['지표'].str.contains('출생|출생아', na=False)
    tfr_mask = df['지표'].str.contains('합계|출산율', na=False)

    if birth_mask.any():
        birth = df.loc[birth_mask].iloc[0]
    else:
        birth = df.iloc[0]

    if tfr_mask.any():
        tfr = df.loc[tfr_mask].iloc[0]
    else:
        # 합계출산율은 대략 6~8번째 줄이라 예비 처리
        tfr = df.iloc[6] if len(df) > 6 else df.iloc[-1]

    return birth, tfr


def analysis(birth, tfr, year_cols):
    birth_series = birth[year_cols].astype('float64')
    tfr_series = tfr[year_cols].astype('float64')

    summary = {
        'birth_mean': birth_series.mean(),
        'birth_median': birth_series.median(),
        'birth_first_year': birth_series.iloc[0],
        'birth_last_year': birth_series.iloc[-1],
        'birth_change_pct': (birth_series.iloc[-1] - birth_series.iloc[0]) / birth_series.iloc[0] * 100,
        'tfr_mean': tfr_series.mean(),
        'tfr_last_year': tfr_series.iloc[-1],
    }

    # 연도별 증감
    birth_change = birth_series.diff()
    tfr_change = tfr_series.diff()

    return birth_series, tfr_series, birth_change, tfr_change, summary


def plot_combined_birth_tfr(year_cols, birth_series, tfr_series):
    years = [int(y) for y in year_cols]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(years, birth_series, marker='o', color='navy', label='출생아 수')
    ax1.set_xlabel('연도')
    ax1.set_ylabel('출생아 수 (명)', color='navy')
    ax1.tick_params(axis='y', labelcolor='navy')

    ax2 = ax1.twinx()
    ax2.plot(years, tfr_series, marker='s', color='darkred', label='합계출산율')
    ax2.set_ylabel('합계출산율', color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('년도별 출생아 수 및 합계출산율 추이 (통합)')
    ax1.grid(True, linestyle='--', alpha=0.4)

    # 축 레전드 병합
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    fig.tight_layout()
    fig.subplots_adjust(top=0.88)
    plt.savefig('birth_and_tfr_combined.png', dpi=150)
    plt.show()


if __name__ == '__main__':
    file_path = '인구동태건수_및_동태율_추이_출생_사망_혼인_이혼__20260327152043.xlsx'

    df, years = load_and_clean(file_path)
    birth, tfr = select_series(df)

    birth_series, tfr_series, birth_change, tfr_change, summary = analysis(birth, tfr, years)

    print('\n=== 데이터 클렌징 완료 ===')
    print(df.head(8))

    print('\n=== 출생아 수 (월) / 합계출산율 선택 결과 ===')
    print('출생 지표:', birth['지표'])
    print('합계출산율 지표:', tfr['지표'])

    print('\n=== 분석 요약 ===')
    for k, v in summary.items():
        print(f'{k}: {v}')

    print('\n=== 연도별 출생아수 성장률 (첫 몇행) ===')
    print(birth_change.head())

    print('\n=== 연도별 합계출산율 변화 (첫 몇행) ===')
    print(tfr_change.head())

    plot_combined_birth_tfr(years, birth_series, tfr_series)
