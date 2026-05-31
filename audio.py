import os
from paths import resource_path

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect


music_player = None
music_output = None

click_sound = None
win_sound = None
error_sound = None

def repeat_music(status):
    if status == QMediaPlayer.MediaStatus.EndOfMedia:
        music_player.setPosition(0)
        music_player.play()

def setup_audio():
    global music_player, music_output
    global click_sound, win_sound, error_sound

    music_player = QMediaPlayer()
    music_output = QAudioOutput()
    music_player.setAudioOutput(music_output)
    music_player.mediaStatusChanged.connect(repeat_music)
    click_sound = QSoundEffect()
    win_sound = QSoundEffect()
    error_sound = QSoundEffect()

    music_path = resource_path("assets/music/background.mp3")
    click_path = resource_path("assets/sounds/click.wav")
    win_path = resource_path("assets/sounds/win.wav")
    error_path = resource_path("assets/sounds/error.wav")

    if os.path.exists(music_path):
        music_player.setSource(QUrl.fromLocalFile(music_path))

    if os.path.exists(click_path):
        click_sound.setSource(QUrl.fromLocalFile(click_path))

    if os.path.exists(win_path):
        win_sound.setSource(QUrl.fromLocalFile(win_path))

    if os.path.exists(error_path):
        error_sound.setSource(QUrl.fromLocalFile(error_path))


def play_music():
    if music_player is not None and not music_player.source().isEmpty():
        music_player.play()


def stop_music():
    if music_player is not None:
        music_player.stop()


def set_music_volume(value):
    if music_output is not None:
        music_output.setVolume(value / 100)


def set_sound_volume(value):
    volume = value / 100

    if click_sound is not None:
        click_sound.setVolume(volume)

    if win_sound is not None:
        win_sound.setVolume(volume)

    if error_sound is not None:
        error_sound.setVolume(volume)


def play_click():
    if click_sound is not None and not click_sound.source().isEmpty():
        click_sound.play()


def play_win():
    if win_sound is not None and not win_sound.source().isEmpty():
        win_sound.play()


def play_error():
    if error_sound is not None and not error_sound.source().isEmpty():
        error_sound.play()