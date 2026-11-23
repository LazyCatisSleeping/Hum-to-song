# Hum-to-Song User Manual

Hum-to-Song lets you record a hum or upload audio in your browser. You can listen to the clip and save a prepared WAV file. The current sprint ends with that WAV file. Song matching and song titles are planned for a later sprint.

## Install and open the app

1. Install [Python 3.12](https://www.python.org/downloads/). You also need a web browser and an internet connection to install the packages. Use a microphone if you want to record.
2. In the [project repository](https://github.com/LazyCatisSleeping/Hum-to-song), select **Code → Download ZIP** and extract the folder. If you use Git, run `git clone https://github.com/LazyCatisSleeping/Hum-to-song.git`.
3. If you are reviewing a pull request, choose its branch before downloading, or switch to that branch after cloning. Open the folder in VS Code and open a terminal where you can see `app.py` and `requirements.txt`.
4. Run the commands for your computer.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS or Linux**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

5. Open the **Local URL** shown in the terminal, usually `http://localhost:8501`. Leave the terminal open while you use the app. Press Ctrl+C in the terminal when you finish.

Use **Language / 语言** to choose English or 中文.

## Record or upload a clip

**Record Humming**

1. Choose **Record Humming**. Allow microphone access if your browser asks.
2. Start the recording, hum a short melody, and stop the recording. Play the preview to check that you can hear it.
3. Click **Submit Audio for Processing**. Wait for the success message.

**Upload Audio**

1. Choose **Upload Audio** and select a WAV, FLAC, or OGG file up to 15 MiB.
2. Play the preview if you want to check the clip. Click **Submit Audio for Processing** and wait for the success message.

The app uses the first 30 seconds of a recording or upload.

## Play and save the result

After a successful submission, find **Prepared Audio** below the submit button. The app shows the sample rate and duration. Play the prepared clip or click **Download Prepared WAV** to save `prepared_humming.wav`. The file is mono WAV at 22,050 Hz with 16-bit PCM audio.

Look for the success message each time you submit a different clip. If a submission fails, the page can still show an earlier result.

## Common problems

| What you see | What to try |
| --- | --- |
| The page does not open | Check that Streamlit is running and open the Local URL shown in the terminal. |
| The recorder cannot start | Check the browser's microphone permission and input device, or upload an audio file. |
| Submit is disabled | Make a recording or choose a file first. |
| The file is rejected | Use a WAV, FLAC, or OGG file under the size limit. Try a file that plays on your computer if the app cannot decode it. |
| The app says the audio is silent | Record again and check the preview before you submit. |

## Report a bug

Open **Issues → New issue** in the project repository. Give the report a short title. Include your operating system and browser, the steps you took, what you expected, and what happened. Copy the error message if you saw one. For audio issues, include the format, file size, and duration if you know them. If a clip helps, attach a short sample that you can share. [Project issues](https://github.com/LazyCatisSleeping/Hum-to-song/issues)
