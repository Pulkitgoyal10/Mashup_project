# 🎵 Magic Mashup Generator

A fully automated web application built with **Streamlit** that creates a music mashup of your favorite artist. It downloads songs from YouTube, trims relevant audio clips, merges them into a single track, and emails the final MP3 file to your inbox.

## 🚀 Features

* **User-Friendly Interface:** Simple form input for artist name, number of songs, and duration.
* **Automated Downloading:** Uses `yt-dlp` to search and download high-quality audio from YouTube.
* **Audio Processing:** Uses `pydub` to trim start times (removing intros) and merge clips seamlessly.
* **Email Delivery:** Automatically sends the generated mashup file as an attachment via SMTP.
* **Input Validation:** Ensures minimum constraints (e.g., >10 videos, >20s duration) are met.

## 🛠️ Prerequisites

Before running this project, ensure you have the following installed:

1.  **Python 3.7+**
2.  **FFmpeg:** This is **strictly required** for audio processing.
    * *Windows:* [Download FFmpeg](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your System PATH.
    * *Mac:* `brew install ffmpeg`
    * *Linux:* `sudo apt install ffmpeg`

## Website Interface

<img width="880" height="727" alt="image" src="https://github.com/user-attachments/assets/c87b7d7f-48c1-4ac4-9a5a-7d237127ac0f" />


## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Pulkitgoyal10/Mashup_project.git](https://github.com/Pulkitgoyal10/Mashup_project.git)
    cd Mashup_project
    ```

2.  **Create a virtual environment (Optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file (if not present) with the contents below and install:
    ```bash
    pip install streamlit yt-dlp pydub
    ```

## 🔐 Configuration (Secrets)

To use the email feature, you must configure your email credentials securely using Streamlit Secrets.

1.  Create a folder named `.streamlit` in your project root.
2.  Inside that folder, create a file named `secrets.toml`.
3.  Add your email credentials:

```toml
# .streamlit/secrets.toml
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
