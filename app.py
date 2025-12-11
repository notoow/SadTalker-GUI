"""
SadTalker-GUI: Simple and Clean Interface for SadTalker
Based on SadTalker by OpenTalker (https://github.com/OpenTalker/SadTalker)
"""

import os
import gradio as gr
from pathlib import Path

# SadTalker 경로 설정
SADTALKER_PATH = os.environ.get("SADTALKER_PATH", "../github_pakuri/SadTalker-main")

import sys
sys.path.insert(0, SADTALKER_PATH)

from src.gradio_demo import SadTalker

# 전역 변수
sad_talker = None

def load_model():
    """모델 로드 (lazy loading)"""
    global sad_talker
    if sad_talker is None:
        checkpoint_path = os.path.join(SADTALKER_PATH, "checkpoints")
        config_path = os.path.join(SADTALKER_PATH, "src/config")
        sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)
    return sad_talker

def generate_video(
    source_image,
    driven_audio,
    use_enhancer,
    preprocess,
    still_mode,
    progress=gr.Progress()
):
    """영상 생성"""
    if source_image is None:
        gr.Warning("이미지를 업로드해주세요")
        return None

    if driven_audio is None:
        gr.Warning("음성 파일을 업로드해주세요")
        return None

    progress(0.1, desc="모델 로딩 중...")
    model = load_model()

    progress(0.2, desc="영상 생성 중...")

    try:
        result = model.test(
            source_image=source_image,
            driven_audio=driven_audio,
            preprocess=preprocess,
            still_mode=still_mode,
            enhancer="gfpgan" if use_enhancer else None,
            batch_size=2,
            size=256,
            pose_style=0
        )
        progress(1.0, desc="완료!")
        return result
    except Exception as e:
        gr.Error(f"오류 발생: {str(e)}")
        return None

# 커스텀 CSS
custom_css = """
/* 전체 배경 */
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
}

/* 헤더 스타일 */
.header {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.header p {
    color: #6b7280;
    font-size: 1rem;
}

/* 업로드 박스 */
.upload-box {
    border: 2px dashed #e5e7eb !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.upload-box:hover {
    border-color: #667eea !important;
    background: #f9fafb !important;
}

/* 버튼 스타일 */
.generate-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    font-size: 1.1rem !important;
    padding: 12px 40px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.generate-btn:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* 설정 패널 */
.settings-panel {
    background: #f9fafb;
    border-radius: 12px;
    padding: 16px;
}

/* 푸터 */
.footer {
    text-align: center;
    padding: 20px;
    color: #9ca3af;
    font-size: 0.85rem;
}

.footer a {
    color: #667eea;
    text-decoration: none;
}
"""

# Gradio 인터페이스 생성
with gr.Blocks(css=custom_css, title="SadTalker-GUI", theme=gr.themes.Soft()) as demo:

    # 헤더
    gr.HTML("""
        <div class="header">
            <h1>SadTalker-GUI</h1>
            <p>사진 한 장과 음성으로 말하는 영상을 만들어보세요</p>
        </div>
    """)

    with gr.Row():
        # 왼쪽: 입력
        with gr.Column(scale=1):
            gr.Markdown("### 📷 이미지")
            source_image = gr.Image(
                label="얼굴 사진을 업로드하세요",
                type="filepath",
                elem_classes=["upload-box"]
            )

            gr.Markdown("### 🎤 음성")
            driven_audio = gr.Audio(
                label="음성 파일을 업로드하세요",
                type="filepath",
                elem_classes=["upload-box"]
            )

            # 설정 (접힘)
            with gr.Accordion("⚙️ 고급 설정", open=False):
                use_enhancer = gr.Checkbox(
                    label="얼굴 화질 개선 (GFPGAN)",
                    value=True,
                    info="처리 시간이 늘어나지만 화질이 좋아집니다"
                )
                preprocess = gr.Radio(
                    choices=["crop", "resize", "full"],
                    value="crop",
                    label="이미지 전처리",
                    info="crop: 얼굴만 / resize: 전체 리사이즈 / full: 원본 유지"
                )
                still_mode = gr.Checkbox(
                    label="정지 모드",
                    value=False,
                    info="머리 움직임을 최소화합니다"
                )

            generate_btn = gr.Button(
                "🎬 영상 생성",
                variant="primary",
                elem_classes=["generate-btn"],
                size="lg"
            )

        # 오른쪽: 출력
        with gr.Column(scale=1):
            gr.Markdown("### 🎥 결과")
            output_video = gr.Video(
                label="생성된 영상",
                format="mp4"
            )

    # 푸터
    gr.HTML("""
        <div class="footer">
            <p>
                Based on <a href="https://github.com/OpenTalker/SadTalker" target="_blank">SadTalker</a>
                by OpenTalker (CVPR 2023)
            </p>
            <p>
                <a href="https://github.com/notoow/SadTalker-GUI" target="_blank">GitHub</a>
            </p>
        </div>
    """)

    # 이벤트 연결
    generate_btn.click(
        fn=generate_video,
        inputs=[
            source_image,
            driven_audio,
            use_enhancer,
            preprocess,
            still_mode
        ],
        outputs=[output_video]
    )

if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True
    )
