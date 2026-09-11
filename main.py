import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 페이지 설정
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
    "영화와 시간에 따른 관객수 변화를 살펴봅니다."
)


# ==================================================
# 데이터 불러오기
# ==================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 열 이름의 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 변환
    number_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in number_columns:
        if column in df.columns:
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


# 필요한 열 확인
required_columns = [
    "날짜",
    "순위",
    "영화코드",
    "영화명",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "데이터에 필요한 열이 없습니다: "
        + ", ".join(missing_columns)
    )
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


movie_list = sorted(
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


if movie_list:

    selected_movie = st.selectbox(
        "영화를 선택하세요.",
        movie_list
    )

    movie_df = df[
        df["영화명"].astype(str) == selected_movie
    ].copy()

    movie_df = movie_df.dropna(
        subset=["날짜", "일관객"]
    )

    movie_df = movie_df.sort_values("날짜")


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

else:
    st.warning("영화 데이터가 없습니다.")


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


movie_total = (
    df.dropna(
        subset=["영화명", "일관객"]
    )
    .groupby("영화명")["일관객"]
    .sum()
    .reset_index()
    .sort_values(
        "일관객",
        ascending=False
    )
)


top5_movies = movie_total.head(5)["영화명"].tolist()


top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.dropna(
    subset=["날짜", "일관객", "영화명"]
)

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


if not top5_df.empty:

    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
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
        legend_title="영화"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:
    st.warning("그래프 2를 만들 수 있는 데이터가 없습니다.")


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


daily_total = (
    df.dropna(
        subset=["날짜", "일관객"]
    )
    .groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)


top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values(
        "일관객",
        ascending=False
    )
    .reset_index(drop=True)
)


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
            bgcolor="white",
            bordercolor="gray",
            borderwidth=1,
            borderpad=4
        )

    if max_value > 0:

        fig3.update_yaxes(
            range=[
                0,
                max_value * 1.25
            ]
        )

    fig3.update_layout(
        height=550,
        xaxis_title="날짜",
        yaxis_title="10위권 일관객 합계(명)",
        hovermode="x"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:
    st.warning("날짜별 데이터를 계산할 수 없습니다.")


st.write("**일관객 합계가 가장 컸던 3일**")

top3_display = top3_days.copy()

top3_display.insert(
    0,
    "순위",
    range(1, len(top3_display) + 1)
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


# 영화별 일관객 합계
movie_total_4 = (
    df.dropna(
        subset=["영화명", "일관객"]
    )
    .groupby("영화명")["일관객"]
    .sum()
    .reset_index()
)

movie_total_4 = movie_total_4.rename(
    columns={
        "일관객": "기간 일관객 합계"
    }
)


# 영화별 10위권 등장 일수
movie_days_4 = (
    df.dropna(
        subset=["영화명", "날짜"]
    )
    .groupby("영화명")["날짜"]
    .nunique()
    .reset_index()
)

movie_days_4 = movie_days_4.rename(
    columns={
        "날짜": "10위권에 든 날수"
    }
)


# 두 데이터 합치기
movie_summary_4 = pd.merge(
    movie_total_4,
    movie_days_4,
    on="영화명",
    how="inner"
)


# TOP 10
top10_movies = (
    movie_summary_4
    .sort_values(
        "기간 일관객 합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# 그래프용 정렬
top10_graph = (
    top10_movies
    .sort_values(
        "기간 일관객 합계",
        ascending=True
    )
)


if not top10_graph.empty:

    fig4 = px.bar(
        top10_graph,
        x="기간 일관객 합계",
        y="영화명",
        orientation="h",
        title="기간 일관객 합계 TOP 10",
        labels={
            "영화명": "영화",
            "기간 일관객 합계": "기간 일관객 합계"
        }
    )

    fig4.update_traces(
        customdata=top10_graph[
            ["10위권에 든 날수"]
        ].to_numpy(),

        hovertemplate=
        "영화: %{y}"
        "<br>기간 일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )

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


# TOP 10 표
st.write("**기간 일관객 합계 TOP 10**")

top10_display = top10_movies.copy()

top10_display.insert(
    0,
    "순위",
    range(1, len(top10_display) + 1)
)

top10_display = top10_display.rename(
    columns={
        "영화명": "영화"
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


st.subheader("그래프 4로 알 수 있는 것")

st.text_area(
    "가로 막대그래프로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph4_explanation"
)


# ==================================================
# 그래프 5
# ==================================================

st.divider()

st.header("📊 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 "
    "월별·요일별 10위권 일관객 합계를 히트맵으로 나타냅니다."
)


# --------------------------------------------------
# 히트맵용 데이터 만들기
# --------------------------------------------------

heatmap_df = df.dropna(
    subset=["날짜", "일관객"]
).copy()


# 월
heatmap_df["월"] = heatmap_df["날짜"].dt.month


# 요일 번호
heatmap_df["요일번호"] = (
    heatmap_df["날짜"].dt.weekday
)


# 요일 이름
weekday_names = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}


heatmap_df["요일"] = (
    heatmap_df["요일번호"]
    .map(weekday_names)
)


# --------------------------------------------------
# 월 × 요일 합계
# --------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(
        ["월", "요일"],
        as_index=False
    )["일관객"]
    .sum()
)


# --------------------------------------------------
# 피벗
# --------------------------------------------------

heatmap_pivot = heatmap_data.pivot(
    index="요일",
    columns="월",
    values="일관객"
)


# --------------------------------------------------
# 요일 순서
# --------------------------------------------------

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


heatmap_pivot = heatmap_pivot.reindex(
    index=weekday_order
)


# 1월~12월 순서
heatmap_pivot = heatmap_pivot.reindex(
    columns=range(1, 13)
)


# --------------------------------------------------
# 히트맵
# --------------------------------------------------

fig5 = px.imshow(
    heatmap_pivot,
    x=[f"{i}월" for i in range(1, 13)],
    y=weekday_order,
    aspect="auto",
    title="월 × 요일별 10위권 일관객 합계",
    labels={
        "x": "월",
        "y": "요일",
        "color": "일관객 합계"
    }
)


# 마우스를 올렸을 때 표시
fig5.update_traces(
    hovertemplate=
    "월: %{x}"
    "<br>요일: %{y}"
    "<br>일관객 합계: %{z:,}명"
    "<extra></extra>"
)


fig5.update_layout(
    height=500,
    xaxis_title="월",
    yaxis_title="요일"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# ==================================================
# 그래프 5로 알 수 있는 것
# ==================================================

st.subheader("그래프 5로 알 수 있는 것")

st.text_area(
    "히트맵으로 내가 알아낸 것은,",
    placeholder="그래프를 보고 알게 된 내용을 직접 입력하세요.",
    height=100,
    key="graph5_explanation"
)
