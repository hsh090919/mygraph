
import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 기본 설정
# ==================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# 제목
# ==================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용하여 "
    "영화의 시간에 따른 관객수 변화를 살펴봅니다."
)


# ==================================================
# 데이터 불러오기
# ==================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# ==================================================
# 데이터 불러오기
# ==================================================

try:

    df = load_data()

except Exception as e:

    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.error(str(e))
    st.stop()


# ==================================================
# 데이터 확인
# ==================================================

st.success(
    f"총 {len(df):,}개의 박스오피스 기록을 불러왔습니다."
)


# ==================================================
# 그래프 1
# ==================================================

st.divider()

st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)


# --------------------------------------------------
# 영화 선택
# --------------------------------------------------

movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
    .tolist()
)


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# --------------------------------------------------
# 선택한 영화 데이터
# --------------------------------------------------

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# --------------------------------------------------
# 그래프 1 그리기
# --------------------------------------------------

if not movie_df.empty:

    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"「{selected_movie}」 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수"
        }
    )

    # 마우스를 올렸을 때 날짜와 관객수 표시
    fig.update_traces(
        hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>"
    )

    fig.update_layout(
        height=500,
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="x"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "선택한 영화의 데이터가 없습니다."
    )


# ==================================================
# 그래프 1에서 알 수 있는 것
# ==================================================

st.subheader("그래프 1로 알 수 있는 것")

st.text_area(
    "선 그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100
)


# ==================================================
# 그래프 2
# ==================================================

st.divider()

st.header("📊 그래프 2. 기간 일관객 합계 상위 5편 비교")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 한 그래프에서 비교합니다."
)


# --------------------------------------------------
# 영화별 일관객 합계 계산
# --------------------------------------------------

movie_total = (
    df.dropna(subset=["영화명", "일관객"])
    .groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)


# --------------------------------------------------
# 일관객 합계 상위 5편
# --------------------------------------------------

top5_movies = movie_total.head(5)["영화명"].tolist()


# --------------------------------------------------
# 상위 5편 데이터만 추출
# --------------------------------------------------

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["영화명", "날짜"]
)


# --------------------------------------------------
# 그래프 2 그리기
# --------------------------------------------------

if not top5_df.empty:

    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        markers=True,
        title="일관객 합계가 가장 큰 5편의 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수",
            "영화명": "영화"
        }
    )

    # 마우스를 올렸을 때 날짜와 관객수 표시
    fig2.update_traces(
        hovertemplate=
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>"
    )

    fig2.update_layout(
        height=600,
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="x"
    )

    # 범례를 클릭하면 영화별 선을 켜고 끌 수 있음
    fig2.update_layout(
        legend_title_text="영화"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:

    st.warning(
        "그래프를 만들 수 있는 데이터가 없습니다."
    )


# --------------------------------------------------
# 상위 5편 확인
# --------------------------------------------------

st.write("**일관객 합계 상위 5편**")

top5_display = movie_total.head(5).copy()

top5_display["일관객"] = (
    top5_display["일관객"]
    .round()
    .astype("int64")
)

top5_display = top5_display.rename(
    columns={
        "영화명": "영화",
        "일관객": "기간 일관객 합계"
    }
)

st.dataframe(
    top5_display,
    hide_index=True,
    use_container_width=True
)


# ==================================================
# 그래프 2에서 알 수 있는 것
# ==================================================

st.subheader("그래프 2로 알 수 있는 것")

st.text_area(
    "선 그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph2_explanation"
)


# ==================================================
# 그래프 3
# ==================================================

st.divider()

st.header("📊 그래프 3")

st.write(
    "앞으로 새로운 그래프를 추가할 공간입니다."
)


# ==================================================
# 그래프 3에서 알 수 있는 것
# ==================================================

st.subheader("그래프 3으로 알 수 있는 것")

st.text_area(
    "그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph3_explanation"
)
