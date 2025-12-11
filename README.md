# SadTalker-GUI

A simple and clean web interface for [SadTalker](https://github.com/OpenTalker/SadTalker) - generating talking face videos from a single image and audio.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Clean, modern UI design
- Simple drag-and-drop interface
- Korean language support
- GFPGAN face enhancement option
- Advanced settings in collapsible panel
- Progress indicator during generation

## Screenshots

*(Coming soon)*

## Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- [SadTalker](https://github.com/OpenTalker/SadTalker) installed

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/notoow/SadTalker-GUI.git
cd SadTalker-GUI
```

### 2. Install SadTalker

Follow the [SadTalker installation guide](https://github.com/OpenTalker/SadTalker#install) first.

### 3. Install dependencies

```bash
pip install gradio>=4.0.0
```

### 4. Set SadTalker path

```bash
export SADTALKER_PATH="/path/to/SadTalker-main"
```

Or edit `app.py` directly:
```python
SADTALKER_PATH = "/path/to/SadTalker-main"
```

## Usage

```bash
python app.py
```

Open http://localhost:7860 in your browser.

## How to Use

1. Upload a face image (portrait photo works best)
2. Upload an audio file (MP3, WAV supported)
3. (Optional) Adjust settings:
   - **Face Enhancement**: Improves output quality using GFPGAN
   - **Preprocess**: crop (face only) / resize / full
   - **Still Mode**: Minimizes head movement
4. Click "Generate" button
5. Download the result video

## Credits

This project is based on **SadTalker** by OpenTalker.

### Citation

```bibtex
@article{zhang2023sadtalker,
  title={SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation},
  author={Zhang, Wenxuan and Cun, Xiaodong and Wang, Xuan and Zhang, Yong and Shen, Xi and Guo, Yu and Shan, Ying and Wang, Fei},
  journal={CVPR},
  year={2023}
}
```

### Related Projects

- [SadTalker](https://github.com/OpenTalker/SadTalker) - Original project
- [GFPGAN](https://github.com/TencentARC/GFPGAN) - Face enhancement

## License

MIT License - see [LICENSE](LICENSE) file.

## Disclaimer

This software is for educational and research purposes. Please use responsibly and respect others' privacy and rights. The developers are not responsible for any misuse of this software.
