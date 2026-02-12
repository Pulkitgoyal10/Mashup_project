import streamlit as st
import os
import smtplib
import shutil
import yt_dlp
from pydub import AudioSegment
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# --- 1. CORE MASHUP LOGIC ---
def create_mashup(singer_name, n_videos, duration, output_filename):
    """
    Downloads videos, trims them, and merges them.
    Returns the path to the output file or None if failed.
    """
    temp_dir = "temp_download_folder"
    
    # Validation
    if n_videos <= 10:
        st.error("Number of videos must be greater than 10.")
        return None
    if duration <= 20:
        st.error("Audio duration must be greater than 20 seconds.")
        return None

    # Cleanup start
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        status_text = st.empty()
        status_text.info(f"🔍 Searching and downloading {n_videos} videos for {singer_name}...")
        
        search_query = f"ytsearch{n_videos}:{singer_name}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(search_query, download=True)

        downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
        
        if not downloaded_files:
            st.error("No audio files were downloaded.")
            return None

        status_text.info("✂️ Trimming and merging audio files...")
        final_mashup = AudioSegment.empty()

        # Create a progress bar
        progress_bar = st.progress(0)
        
        for i, file in enumerate(downloaded_files):
            file_path = os.path.join(temp_dir, file)
            audio = AudioSegment.from_file(file_path)

            # Logic: Remove first 30s, take next 'duration' seconds
            start_point = 30 * 1000
            end_point = start_point + (duration * 1000)
            
            # Handle clips shorter than expected
            if len(audio) > start_point:
                trimmed = audio[start_point:min(end_point, len(audio))]
                final_mashup += trimmed
            
            # Update progress
            progress_bar.progress((i + 1) / len(downloaded_files))

        final_mashup.export(output_filename, format="mp3")
        status_text.success("✅ Mashup created successfully!")
        
        # Cleanup temp folder but keep output
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            
        return output_filename

    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        return None

# --- 2. EMAIL LOGIC ---
def send_email(recipient_email, file_path):
    """
    Sends the generated MP3 file to the user's email.
    """
    # LOAD SECRETS (See Step 4)
    SENDER_EMAIL = st.secrets["EMAIL_ADDRESS"]
    SENDER_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "Your Generated Music Mashup 🎵"

    body = "Here is the mashup you requested via the Streamlit App. Enjoy!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")
        msg.attach(part)

        # Connect to Gmail SMTP (Change if using Outlook/Yahoo)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# --- 3. STREAMLIT UI ---
st.title("🎵 Magic Mashup Generator")
st.markdown("Generate a mashup of your favorite artist and get it delivered to your inbox!")

with st.form("mashup_form"):
    singer = st.text_input("Singer Name", placeholder="e.g., Sharry Maan")
    col1, col2 = st.columns(2)
    with col1:
        n_videos = st.number_input("Number of Videos (>10)", min_value=11, value=11, step=1)
    with col2:
        duration = st.number_input("Duration per song (sec, >20)", min_value=21, value=30, step=1)
    
    email_id = st.text_input("Your Email Address")
    output_file = "mashup.mp3"
    
    submitted = st.form_submit_button("Generate & Email Mashup")

if submitted:
    if not singer or not email_id:
        st.warning("Please fill in all fields.")
    else:
        # Run the mashup logic
        result_file = create_mashup(singer, n_videos, duration, output_file)
        
        if result_file:
            # Send Email
            with st.spinner("📧 Sending email..."):
                success = send_email(email_id, result_file)
                if success:
                    st.success(f"Email sent to {email_id}!")
                else:
                    st.error("Could not send email. Please check the logs.")

            # Provide Direct Download as Backup
            with open(result_file, "rb") as f:
                st.download_button("Download Mashup Manually", f, file_name="mashup.mp3")