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
    number_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in number_columns:
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


# 영화 목록
movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
    .tolist()
)


# 영화 선택
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# 그래프 1
if not movie_df.empty:

    fig1 = px.line(
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

    fig1.update_traces(
        hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>"
    )

    fig1.update_layout(
        height=500,
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="x"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

else:
    st.warning("선택한 영화의 데이터가 없습니다.")


# 그래프 1 설명
st.subheader("그래프 1로 알 수 있는 것")

st.text_area(
    "선 그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph1_explanation"
)


# ==================================================
# 그래프 2
# ==================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계가 가장 큰 5편")

st.write(
    "이 기간 동안 일관객 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 한 선 그래프에서 비교합니다."
)


# 영화별 일관객 합계
movie_total = (
    df.dropna(
        subset=["영화명", "일관객"]
    )
    .groupby(
        "영화명",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)


# 상위 5편
top5_movies = movie_total.head(5)["영화명"].tolist()


# 상위 5편 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.dropna(
    subset=["날짜", "일관객", "영화명"]
)

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


# 그래프 2
if not top5_df.empty:

    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        markers=False,
        title="일관객 합계가 가장 큰 5편의 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수",
            "영화명": "영화"
        }
    )

    fig2.update_traces(
        hovertemplate=
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )

    fig2.update_layout(
        height=550,
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="closest",
        legend_title="영화",
        legend=dict(
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:
    st.warning("그래프를 만들 수 있는 데이터가 없습니다.")


# 상위 5편 목록
st.write("**일관객 합계 상위 5편**")

top5_display = movie_total.head(5).copy()

top5_display = top5_display.rename(
    columns={
        "영화명": "영화",
        "일관객": "기간 일관객 합계"
    }
)

top5_display["기간 일관객 합계"] = (
    top5_display["기간 일관객 합계"]
    .round()
    .astype("int64")
)

st.dataframe(
    top5_display,
    hide_index=True,
    use_container_width=True
)


# 그래프 2 설명
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

st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "날짜별로 그날 박스오피스 10위권 영화의 "
    "일관객을 모두 합산하여 영역 그래프로 나타냅니다."
)


# 날짜별 일관객 합계
daily_total = (
    df.dropna(
        subset=["날짜", "일관객"]
    )
    .groupby(
        "날짜",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values("날짜")
)


# 가장 큰 날 3개
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values(
        "일관객",
        ascending=False
    )
    .reset_index(drop=True)
)


# 그래프 3
if not daily_total.empty:

    fig3 = px.area(
        daily_total,
        x="날짜",
        y="일관객",
        title="날짜별 10위권 일관객 합계",
        labels={
            "날짜": "날짜",
            "일관객": "10위권 일관객 합계"
        }
    )

    fig3.update_traces(
        hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )

    fig3.update_layout(
        height=550,
        xaxis_title="날짜",
        yaxis_title="10위권 일관객 합계(명)",
        hovermode="x"
    )

    # 가장 큰 3일 표시
    max_value = daily_total["일관객"].max()

    for i, row in top3_days.iterrows():

        rank = i + 1
        date_text = row["날짜"].strftime("%Y-%m-%d")
        value = row["일관객"]

        fig3.add_annotation(
            x=row["날짜"],
            y=value,
            text=(
                f"{rank}위<br>"
                f"{date_text}<br>"
                f"{value:,.0f}명"
            ),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-60,
            font=dict(size=12),
            bgcolor="white",
            bordercolor="gray",
            borderwidth=1,
            borderpad=4
        )

    fig3.update_yaxes(
        range=[0, max_value * 1.25]
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:
    st.warning(
        "날짜별 일관객 데이터를 계산할 수 없습니다."
    )


# 가장 컸던 3일 표
st.write("**일관객 합계가 가장 컸던 3일**")

top3_display = top3_days.copy()

top3_display.insert(
    0,
    "순위",
    [1, 2, 3]
)

top3_display["날짜"] = (
    top3_display["날짜"]
    .dt.strftime("%Y-%m-%d")
)

top3_display = top3_display.rename(
    columns={
        "일관객": "10위권 일관객 합계"
    }
)

top3_display["10위권 일관객 합계"] = (
    top3_display["10위권 일관객 합계"]
    .round()
    .astype("int64")
)

st.dataframe(
    top3_display,
    hide_index=True,
    use_container_width=True
)


# 그래프 3 설명
st.subheader("그래프 3으로 알 수 있는 것")

st.text_area(
    "영역 그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph3_explanation"
)


# ==================================================
# 그래프 4
# ==================================================

st.divider()

st.header("📊 그래프 4. 기간 일관객 TOP 10")

st.write(
    "영화별로 이 기간의 일관객을 모두 더해 "
    "관객이 많은 영화 TOP 10을 가로 막대그래프로 보여줍니다."
)


# --------------------------------------------------
# 영화별 일관객 합계 + 10위권에 든 날수 계산
# --------------------------------------------------

movie_summary = (
    df.dropna(
        subset=["영화명", "일관객", "날짜"]
    )
    .groupby("영화명")
    .agg(
        기간_일관객_합계=("일관객", "sum"),
        10위권_등장_일수=("날짜", "nunique")
    )
    .reset_index()
)


# --------------------------------------------------
# 일관객 합계 TOP 10
# --------------------------------------------------

top10_movies = (
    movie_summary
    .sort_values(
        "기간_일관객_합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# 그래프에 표시할 순서를 위해
# 관객이 적은 순 → 많은 순으로 정렬
# (가로 막대그래프에서 많은 영화가 위쪽에 오도록 설정)
top10_graph = (
    top10_movies
    .sort_values(
        "기간_일관객_합계",
        ascending=True
    )
)


# --------------------------------------------------
# 그래프 4
# --------------------------------------------------

if not top10_graph.empty:

    fig4 = px.bar(
        top10_graph,
        x="기간_일관객_합계",
        y="영화명",
        orientation="h",
        title="기간 일관객 합계 TOP 10",
        labels={
            "영화명": "영화",
            "기간_일관객_합계": "기간 일관객 합계"
        }
    )

    # 마우스를 올렸을 때 표시되는 정보
    fig4.update_traces(
        hovertemplate=
        "영화: %{y}"
        "<br>기간 일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata}일"
        "<extra></extra>",
        customdata=top10_graph[
            "10위권_등장_일수"
        ]
    )

    # 관객이 많은 영화가 위쪽에 오도록
    fig4.update_layout(
        height=600,
        xaxis_title="기간 일관객 합계(명)",
        yaxis_title="영화",
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

else:

    st.warning(
        "TOP 10 그래프를 만들 수 있는 데이터가 없습니다."
    )


# --------------------------------------------------
# TOP 10 표
# --------------------------------------------------

st.write("**기간 일관객 합계 TOP 10**")

top10_display = top10_movies.copy()

top10_display.insert(
    0,
    "순위",
    range(1, len(top10_display) + 1)
)

top10_display = top10_display.rename(
    columns={
        "영화명": "영화",
        "기간_일관객_합계": "기간 일관객 합계",
        "10위권_등장_일수": "10위권에 든 날수"
    }
)

top10_display["기간 일관객 합계"] = (
    top10_display["기간 일관객 합계"]
    .round()
    .astype("int64")
)

st.dataframe(
    top10_display,
    hide_index=True,
    use_container_width=True
)


# --------------------------------------------------
# 그래프 4에서 알 수 있는 것
# --------------------------------------------------

st.subheader("그래프 4로 알 수 있는 것")

st.text_area(
    "가로 막대그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph4_explanation"
)
