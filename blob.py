# blobfish_reference_match.py
# N을 입력하면 참고 이미지와 동일한 구도/색감의 블롭피쉬를 N×N PNG로 저장

import pathlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, PathPatch
from matplotlib.path import Path as MplPath

def draw_blobfish(n: int, outfile: str) -> str:
    dpi = 100
    fig = plt.figure(figsize=(n/dpi, n/dpi), dpi=dpi)
    ax = fig.add_axes([0,0,1,1])
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.set_facecolor("white")  # 레퍼런스와 동일한 흰 배경

    s  = n/512.0
    lw = max(1.6, 2.6*s)       # 외곽선 두께(레퍼런스 분위기)

    # 1) 몸통: 둥근 삼각형(rounded triangle) 실루엣
    start = (0.23, 0.34)   # 좌측 바닥
    top   = (0.50, 0.80)   # 꼭대기
    right = (0.77, 0.34)   # 우측 바닥
    bot_c1= (0.62, 0.24)   # 바닥 곡률 제어점들
    bot_c2= (0.38, 0.24)

    verts = [start, (0.28,0.66), top, (0.72,0.66), right, bot_c1, bot_c2, start, start]
    codes = [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.CURVE3,
             MplPath.CURVE3, MplPath.CURVE3, MplPath.CURVE3, MplPath.CURVE3,
             MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(verts, codes),
                           facecolor="#f6b3c4", edgecolor="#e58fa4",
                           linewidth=lw, joinstyle="round"))

    # 2) 하이라이트(상단 좌측)
    ax.add_patch(Ellipse((0.42,0.72), 0.12, 0.06, angle=10,
                         facecolor="white", edgecolor="none", alpha=0.95))

    # 3) 눈(작은 점)
    ax.add_patch(Circle((0.45,0.53), 0.018, color="black"))
    ax.add_patch(Circle((0.55,0.53), 0.018, color="black"))

    # 4) 크게 처진 입(두 개의 2차 베지어로 연속 곡선)
    mouth_verts = [(0.34,0.42), (0.44,0.34), (0.50,0.32), (0.56,0.34), (0.66,0.42)]
    mouth_codes = [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.CURVE3, MplPath.CURVE3]
    ax.add_patch(PathPatch(MplPath(mouth_verts, mouth_codes),
                           edgecolor="#9a6272", facecolor="none",
                           linewidth=max(3.0, 4.2*s), capstyle="round"))

    # 5) 양쪽 작은 지느러미
    ax.add_patch(Ellipse((0.30,0.34), 0.12, 0.06, facecolor="#f6b3c4",
                         edgecolor="#e58fa4", linewidth=lw))
    ax.add_patch(Ellipse((0.70,0.34), 0.12, 0.06, facecolor="#f6b3c4",
                         edgecolor="#e58fa4", linewidth=lw))

    out = pathlib.Path(outfile); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor=ax.get_facecolor(), edgecolor="none", pad_inches=0)
    plt.close(fig)
    return str(out)

if __name__ == "__main__":
    N = int(input("크기 입력: ").strip())                 # 예: 512
    print(draw_blobfish(N, f"./blobfish_{N}.png"))