import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import re
def preprocess(text) -> str:
    # 화살표 유니코드 변환
    text = re.sub(r"unicode{x27AD}", "rightarrow", text)  # or Rightarrow?
    # [%d pt] 제거 -> 줄바꿈
    text = re.sub(r"\[\dpt]", "", text)
    # mtvec을 동일한 효과를 지닌 overrightarrow로 변환
    text = re.sub(r"mtvec", "overrightarrow", text)
    text = re.sub(r"\\enclose\{longdiv}\{(.*)}", r"\\overline{\1}", text)

    # 이미지: [img_1_1] -> (이미지_1_1) -> latex에서는 (이미지\_1\_1)로 변환해줘야 함
    text = re.sub(r"#\[img(.*?)]#", r"(이미지\1)", text)
    # for a in re.findall(r"(#\[img.*?]#)", text):
    #     replacement = re.sub(r'_', '\_', a)
    #     replacement = re.sub(r"#\[img(.*?)]#", r"(이미지\1)", replacement)
    #     text = text.replace(a, replacement)
    # bbox 내부적 함수 제거
    text = re.sub(r"\\bbox\[.*?]{(.*?)}", r"\1", text)
    # 개념 및 용어 태깅 제거
    text = re.sub(r"#\[.*?\|.*?::(.*?)]#", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"#\(.*?\|.*?::(.*?)\)#", r"\1", text, flags=re.DOTALL)
    # html 문법 제거
    text = re.sub(r"<b>|</b>", "", text)


    # <div></div>안에 <div></div>가 있는 경우도 존재하기 때문에, loop을 돌려서 삭제 # 몇몇의 div의 style class 정의가 안됨 (후처리..?)
    while True:
        result = re.search(r"<div.*?>.*?</div.*?>", text, flags=re.DOTALL)
        print(result)
        if not result:
            break
        else:
            text = re.sub(r"<div.*?>(.*?)</div.*?>", r"\1", text, flags=re.DOTALL)
    print('=' * 20)

    # [] -> $$$$ 변환 (변환하지 않아도, latex 변환에는 문제 없음, 어떤게 chatbot 학습에 이로울까?)
    text = re.sub(r"\\\[(.*?)\\]", r"$$\1$$", text, flags=re.DOTALL)

    text = text.strip()
    return text


def postprocess(text: str) -> str:
    # 모든 $$~$$를 $$\n~\n$$으로 변환
    text = re.sub(r"\$\$(.*?)\$\$", r"$$\n\1\n$$", text)

    # begin 앞에 $$\n 그리고 end 뒤에 \n$$
    #text = re.sub(r"(\\begin{.*?})", r"$$\n\1", text)
    #text = re.sub(r"(\\end{.*?})", r"\1\n$$", text)

    # 연속적으로 \n이 있는 경우, 한개로 통합하는 과정
    text = re.sub(r"\n+", r"\n", text, flags=re.DOTALL)
    text = text.strip()
    return text

def postprocessCBResponse(text: str) -> str:
    # 모든 $$~$$를 $$\n~\n$$으로 변환
    text = re.sub(r"\$\$(.*?)\$\$", r"$$\n\1\n$$", text)

    # begin 앞에 $$\n 그리고 end 뒤에 \n$$
    #text = re.sub(r"(\\begin{.*?})", r"$$\n\1", text)
    #text = re.sub(r"(\\end{.*?})", r"\1\n$$", text)

    # 연속적으로 \n이 있는 경우, 한개로 통합하는 과정
    text = re.sub(r"\n+", r"\n\n", text, flags=re.DOTALL)
    text = text.strip()
    return text
latext=r'''
$\left\\{\begin{array}{ll}(x+1):(-3-2y)=1: 3 & \quad \cdots \\,㉠\\\\3x+y=9 & \quad \cdots \\,㉡\end{array}\right.$
[1단계]: 이차함수 변형하기
우리가 주어진 이차함수는 $y=-2x^2-4x+k$입니다. 이 이차함수를 변형하면 $y=-2(x+1)^2+2+k가 됩니다. 이 변형은 이차함수의 표준형태를 얻기 위해 이루어집니다.

[2단계]: 최솟값을 이용하여 $k$값 구하기
이제 $-3\le x \le 0$에서 이차함수 $y=-2(x+1)^2+2+k$의 최솟값이 $-5$라는 것을 알고 있습니다. 이 최솟값은 $x=-3$일 때 발생합니다. 따라서 이를 이용하여 $k$값을 구할 수 있습니다. $-5=-8+2+k$ 식을 통해 $k=1$을 얻을 수 있습니다.
'''
#st.write(postprocess(latext))
st.write(postprocessCBResponse(latext))

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
