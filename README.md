# SCDP project page

[Spatially Conditioned Diffusion Policy: Learning Precise and Robust Manipulation with a Single RGB Camera](https://arxiv.org/abs/2606.14535)의 영상 중심 프로젝트 페이지 초안입니다. Academic Project Page Template을 바탕으로 만들었으며, DexUMI의 실험 영상 중심 구성을 참고했습니다.

## 로컬 미리보기

저장소 루트에서 실행합니다. 별도의 빌드나 npm 설치가 필요하지 않습니다.

```bash
python -m http.server 8085 --bind 127.0.0.1
```

브라우저에서 **http://localhost:8085** 를 엽니다. 이미 서버가 실행 중이면 바로 접속하면 됩니다. 터미널에서 `Ctrl+C`로 종료할 수 있습니다.

원격 서버 또는 개발 컨테이너를 사용한다면 편집기의 포트 전달 기능으로 **8085 → localhost:8085**를 연결합니다. 현재 미리보기는 루프백 주소에만 바인딩합니다.

## 페이지 구성

1. 논문 제목, 저자, 소속, Paper / Video / Code 버튼
2. Method: 논문 아키텍처 그림, 방법 설명, 펼쳐 보는 초록
3. Precision at the point of contact: USB Insertion / Battery Insertion
4. Distractor Robustness: USB Insertion w/ Distractors / Battery Insertion w/ Distractors
5. Long Horizon: 서랍 열기 → 바나나 집기 → 넣기 → 서랍 닫기 (2× 영상)
6. More Experiments: Cup Handle Grasping / Cup Handle Grasping w/ Distractors / Cup Wall Grasping / Push Cube w/ Distractors
7. Humanoid: Separating Paper Cup / Erasing White Board
8. BibTeX와 복사 버튼

현재 `video/`의 영상 11개를 연결했습니다. USB Insertion은 4×, Battery Insertion은 2× 데모를 표시합니다. 제목의 **S·C·D·P**와 **Single RGB Camera**를 파란색으로 강조합니다.

## 수정할 파일

- `index.html`: 제목, 저자, 설명, 영상 배치, 논문 링크, 인용
- `static/css/index.css`: 색상, 타이포그래피, 데스크톱/모바일 레이아웃
- `static/js/index.js`: 화면에 보이는 영상의 자동 재생, BibTeX 복사
- `video/`: 제공한 원본 영상 (실제 폴더명은 `videos/`가 아닌 `video/`)
- `static/videos/scdp/`: 페이지에서 재생하는 웹용 MP4
- `static/images/scdp/`: 영상 썸네일, 논문 Figure 2, 프로젝트 파비콘
- `static/images/scdp/gripper-logo.png`: `video/IMG_7031.JPEG`에서 그리퍼·USB와 주변 distractor(바나나, 딸기, 테이프, 배터리), USB 허브까지 넓게 추출한 투명 PNG 로고. 상단·하단 로고와 `gripper-icon-*`, `gripper-favicon.ico` 탭 아이콘으로 활용합니다.

정적 HTML/CSS/JS와 상대경로로 구성되어 GitHub Pages의 저장소 하위 경로에서도 사용할 수 있습니다. jQuery나 외부 CDN 없이 동작합니다. 배포 주소는 https://scdp-project.github.io/이며, 저장소는 https://github.com/SCDP-project/scdp-project.github.io 입니다. 원본 영상은 `.gitignore`로 제외하고 웹용 영상만 업로드합니다.

## 영상 갱신

원본을 교체한 뒤 아래 명령을 실행합니다. Python과 `ffmpeg`가 필요합니다.

```bash
python scripts/prepare_videos.py
```

폴더를 `videos/`로 변경한 경우:

```bash
python scripts/prepare_videos.py --source videos
```

MP4와 MOV 원본(대소문자 구분 없음)을 보존하면서 720p H.264 MP4 영상과 포스터를 만듭니다. HDR 영상은 SDR로 톤 매핑해 일반 브라우저에서도 색상이 자연스럽게 보이도록 변환합니다. 같은 파일명의 MP4와 MOV를 함께 넣으면 출력 충돌을 방지하기 위해 오류를 표시합니다. 웹용 영상은 무음이며, 재생 시작을 빠르게 하는 `faststart` 옵션을 사용합니다. 파일명에 표시된 배속(1×/2×/4×)은 이미 영상에 적용되어 있으므로 브라우저에서는 추가로 가속하지 않습니다. 새 파일을 추가하면 `index.html`에도 해당 영상과 설명을 추가합니다. 파일을 삭제하거나 이름을 변경하면 페이지의 영상 경로·배속을 함께 갱신하고, 더 이상 참조하지 않는 웹용 영상과 포스터도 제거합니다.

Paper Cup 영상은 로봇 크기를 White Board 영상에 맞추기 위해 약 1.33× 크롭을 적용합니다. 이 설정은 `scripts/prepare_videos.py`의 `CROP_FILTERS`에 있으며, 크롭 설정 변경 후에는 `--force`로 영상과 포스터를 다시 만들 수 있습니다.

화면 밖의 영상과 비활성 탭의 영상은 일시정지합니다. 운영체제의 동작 줄이기 설정 또는 브라우저의 데이터 절약 설정이 켜져 있으면 자동 재생을 기본으로 끕니다. 각 영상의 기본 재생 컨트롤은 그대로 사용할 수 있습니다.

## 콘텐츠 출처와 초안 메모

- 제목, 저자 소속, 공동 1저자 표기, 초록과 방법 설명: arXiv:2606.14535v1 및 PDF.
- `Young Jin Heo`는 PDF 표기를 따랐습니다. arXiv 메타데이터에는 `Yeong Jin Heo`로 표기되어 있어 최종 공개 시 선호 표기를 확인하면 됩니다.
- 휴머노이드 영상은 arXiv v1 본문에 없으므로 추가 데모 섹션으로 소개했습니다. USB/배터리의 distractor 영상에도 논문에 없는 성공률 수치를 부여하지 않았습니다.
- Code 버튼은 https://github.com/IRSL-robotics/SCDP 로 연결됩니다.
- Video 버튼은 YouTube 주소가 정해지기 전까지 `Coming soon` 상태입니다. `index.html`의 `video-resource` 버튼을 링크로 바꾸고 `resource-note`를 제거하면 활성화할 수 있습니다.
- Method는 논문 Figure 2의 Multi-Scale Image Encoder / Spatial Conditioning Module / Action Denoising Network 구성과 visual attention anchors 용어를 따릅니다.
- 공유 이미지, canonical, `og:url`은 https://scdp-project.github.io/ 주소로 설정했습니다.
- 템플릿의 기존 샘플 파일은 보존했지만 새 페이지에서는 참조하지 않습니다.

## Acknowledgments & license

Built with [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template), adapted from [Nerfies](https://nerfies.github.io/). Video-led layout inspired by [DexUMI](https://dex-umi.github.io/).

The website template is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). This attribution refers to the website template; paper and media rights remain with their respective owners.
