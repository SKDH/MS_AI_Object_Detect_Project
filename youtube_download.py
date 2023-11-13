# 모듈 임포트
from pytube import YouTube
from moviepy import editor

# 비디오 다운로드
link = "https://www.youtube.com/watch?v=ufWa8VVZAFY"  # 다운로드할 비디오의 링크
yt = YouTube(link)
stream = (
    yt.streams.filter(progressive=True, file_extension="mp4")
    .order_by("resolution")
    .desc()
    .first()
)  # 다운로드 가능한 형식 중에서 가장 높은 화질을 가진 스트림 선택
stream.download(filename="asian_black_bear.mp4")
# stream.download()

# 원하는 구간 추출
start_time = 83  # 시작 시간 (초)
end_time = 147  # 종료 시간 (초)
video = editor.VideoFileClip("asian_black_bear.mp4").subclip(start_time, end_time)

# 추출한 구간 저장
video.write_videofile("asian_black_bear_clip.mp4", fps=25)
