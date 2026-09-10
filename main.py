import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화의 시간에 따른 관객수 변화를 살펴봅니다."
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형으로 변환
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


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.error(str(e))
    st.stop()


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
st.success(
    f"총 {len(df):,}개의 박스오피스 기록을 불러왔습니다."
)


# ==================================================
# 그래프 1
# ==================================================
st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화가 박스오피스 10위권에 "
    "기록된 날짜의 일관객 변화를 확인할 수 있습니다."
)


# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().unique().tolist()
)


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# --------------------------------------------------
# 그래프
# --------------------------------------------------
if len(movie_df) > 0:

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

    # 마우스를 올렸을 때 표시되는 정보
    fig.update_traces(
        hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>"
    )

    # 그래프 크기
    fig.update_layout(
        height=500,
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("선택한 영화의 데이터가 없습니다.")


# --------------------------------------------------
# 그래프 설명
# --------------------------------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "선택한 영화의 날짜별 일관객 변화를 통해 "
    "시간이 지나면서 관객수가 어떻게 증가하거나 감소했는지 알 수 있습니다."
)


# ==================================================
# 다음 그래프를 위한 구역
# ==================================================
st.divider()

st.header("📊 그래프 2")

st.info(
    "다음 그래프를 추가할 공간입니다."
)


# ==================================================
# 그래프 3을 위한 구역
# ==================================================
st.divider()

st.header("📊 그래프 3")

st.info(
    "앞으로 새로운 그래프를 추가할 공간입니다."
)
