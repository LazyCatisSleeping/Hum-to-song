from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_audio_workflow_opens_in_both_languages():
    app = AppTest.from_file(
        str(Path(__file__).resolve().parents[1] / "app.py"),
        default_timeout=30,
    ).run()

    assert not app.exception
    assert app.title[0].value == "Hum-to-Song Recognition"
    assert app.radio[0].options == ["Record Humming", "Upload Audio"]
    assert app.button[0].proto.disabled

    app.radio[0].set_value("Upload Audio").run()
    assert not app.exception
    assert app.radio[0].value == "Upload Audio"
    assert app.button[0].proto.disabled

    app.selectbox[0].set_value("中文").run()
    assert not app.exception
    assert app.title[0].value == "哼唱歌曲识别"
    assert app.radio[0].options == ["录制哼唱", "上传音频"]
    assert app.button[0].proto.disabled
