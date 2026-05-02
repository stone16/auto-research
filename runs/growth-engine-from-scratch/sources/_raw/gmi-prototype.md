# Repo: gmi-prototype

## README.md
```markdown
# GMI Cloud Video Generation Prototype

A simple Python prototype for generating videos using GMI Cloud's VideoGen API with an interactive interface.

## ✅ Features

- **Interactive video generation** with model selection
- **18+ GMI Cloud models** (Veo3, WAN-AI, Kling, Luma)
- **Batch video generation** (1-10 videos per session)
- **Automatic local storage** in `./generated_videos/`
- **Real-time progress monitoring**
- **Robust error handling**

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config.yaml and add your GMI Cloud API key
   ```

3. **Run video generation:**
   ```bash
   python generate_videos.py
   ```

## 🎬 Interactive Experience

The script guides you through:

1. **📋 Model Selection**: Choose from available models
   - Google Veo (Veo3, Veo3-Fast)
   - WAN-AI models (2.1, 2.2 variants)
   - Kling models (Text2Video, Image2Video)
   - Luma Ray2

2. **🔢 Video Count**: Specify 1-10 videos to generate

3. **✍️ Custom Prompt**: Enter your video description

4. **🎬 Automatic Generation**: Videos saved to `./generated_videos/`

## ⚙️ Configuration

Edit `config/config.yaml` with your GMI Cloud credentials:

```yaml
gmi_cloud:
  videogen:
    api_key: "your-gmi-api-key-here"
    base_url: "https://console.gmicloud.ai/api/v1"
```

## 📋 Sample Usage

```bash
$ python generate_videos.py

🎬============================================================🎬
       GMI CLOUD VIDEO GENERATION
🎬============================================================🎬

📋 Step 1: Loading Available Models
✅ Found 18 available models

📋 Step 2: Select Video Generation Model
🎬 Google Veo:
  1. Veo3-Fast
  2. Veo3
🎬 WAN-AI:
  3. Wan-AI_Wan2.2-T2V-A14B
  ...

Select model (1-18): 1
✅ Selected: Veo3-Fast

📋 Step 3: Number of Videos
Enter number of videos (1-10): 2
✅ Will generate 2 videos

📋 Step 4: Video Description  
Your prompt: A cat playing in a sunny garden
✅ Prompt: A cat playing in a sunny garden

📋 Step 5: Video Generation
🎬 Generating videos...
✅ Videos saved to ./generated_videos/
```

## 📁 Project Structure

```
gmi-prototype/
├── generate_videos.py              # 🎬 Main interactive script
├── README.md                       # 📖 This file
├── requirements.txt                # 📦 Dependencies
├── config/
│   ├── config.example.yaml         # 📝 Configuration template
│   └── config.yaml                 # 🔑 Your credentials
└── src/
    ├── core/config_manager.py      # ⚙️ Configuration management
    ├── services/videogen_service.py # 🎥 GMI Cloud API integration
    └── utils/exceptions.py         # ❌ Error handling
```

## 🔧 Technical Details

- **API Endpoints**: Uses official GMI Cloud documented endpoints
- **Model Support**: All 18+ current GMI video generation models
- **Async Architecture**: Efficient handling of long-running video generation
- **Error Handling**: Comprehensive error management and user feedback
- **Type Safety**: Full type hints throughout codebase

## 📋 Requirements

- Python 3.8+
- GMI Cloud account with credits
- Valid GMI Cloud API key

## 💡 Next Steps

1. **Add Credits**: Log into https://console.gmicloud.ai and add credits
2. **Run Generation**: Execute `python generate_videos.py`
3. **Enjoy Videos**: Find your generated videos in `./generated_videos/`

---

Built with ❤️ for GMI Cloud VideoGen API
```
