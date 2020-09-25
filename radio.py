#!/usr/bin/python
import os
import sys
import time
import tty
import termios

import vlc
import requests

ABSOLUTE_PATH = '/home/waldemar/PycharmProjects/Radio/'
ANNOUNCEMENT_VOLUME = 120
STREAM_VOLUME = 50


def check_internet_connection(url='http://www.google.com/', timeout=3):
    try:
        r = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError as ex:
        return False


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def start(station_name, volume=50):
    os.system('tmux new -s {} -d'.format(station_name))
    os.system('tmux send-keys -t {} "mplayer -volume {} {}" ENTER'.format(station_name,
                                                                          volume,
                                                                          name_to_url[station_name]))


def stop(station_name):
    os.system('tmux kill-session -t {}'.format(station_name))


def play_announcement_vlc(announcement,
                          volume=120):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(announcement)
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()
    time.sleep(0.2)
    duration = player.get_length() / 1000
    time.sleep(duration)


def play_announcement_mplayer(announcement,
                              volume=120):
    os.system('mplayer -volume {} {}'.format(volume, announcement))


name_to_announcement = {
    'nowy_swiat': 'odtwarzam_radio_nowy_swiat.mp3',
    'pogoda': 'odtwarzam_radio_pogoda.mp3',
    'tok_fm': 'odtwarzam_radio_tokfm.mp3',
    'zlote_przeboje': 'odtwarzam_radio_zlote_przeboje.mp3',
    'rmf_fm': 'odtwarzam_radio_rmffm.mp3',
    'zet': 'odtwarzam_radio_zet.mp3',
    'bon_ton': 'odtwarzam_radio_bon_ton.mp3'
}
intro_announcement = 'intro.mp3'
outro_announcement = 'outro.mp3'
resume_announcement = 'resume.mp3'
stop_announcement = 'stop.mp3'
select_announcement = 'wybierz_stacje.mp3'
wrong_announcement = 'bledny_numer_stacji.mp3'

name_to_url = {
    'nowy_swiat': 'http://stream.rcs.revma.com/ypqt40u0x1zuv',
    'pogoda': 'http://stream10.radioagora.pl:80/tuba38-1.mp3',
    'tok_fm': 'http://olsztyn.radio.pionier.net.pl:8000/z/radiotok4.ogg',
    'zlote_przeboje': 'http://stream14.radioagora.pl:80/tuba8936-1.mp3',
    'rmf_fm': 'http://31.192.216.8:80/rmf_fm',
    'zet': 'http://zet-net-01.cdn.eurozet.pl:8400',
    'bon_ton': 'https://streaming.inten.pl:8020/bonton.mp3'
}

char_to_name = {
    '1': 'nowy_swiat',
    '2': 'pogoda',
    '3': 'tok_fm',
    '4': 'zlote_przeboje',
    '5': 'rmf_fm',
    '6': 'zet',
    '7': 'bon_ton'
}


if __name__ == '__main__':

    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + intro_announcement,
                              volume=ANNOUNCEMENT_VOLUME)
    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + select_announcement,
                              volume=ANNOUNCEMENT_VOLUME)

    if not check_internet_connection(timeout=1):
        print("No internet connection.")
        sys.exit()
    last_station_name = None
    while True:
        press = getch()
        print(press)
        print(ord(press))
        print()
        if ord(press) != 10:
            if ord(press) == 115:
                if last_station_name is not None:
                    stop(last_station_name)
                    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + stop_announcement,
                                              volume=ANNOUNCEMENT_VOLUME)

            elif ord(press) == 112:
                if last_station_name is not None:
                    stop(last_station_name)
                    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + resume_announcement,
                                              volume=ANNOUNCEMENT_VOLUME)
                    start(station_name=last_station_name,
                          volume=STREAM_VOLUME)

            elif ord(press) == 13:
                if last_station_name is not None:
                    stop(last_station_name)
                play_announcement_mplayer(outro_announcement)
                break

            else:
                if press in char_to_name.keys():
                    if last_station_name is not None:
                        stop(last_station_name)
                    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + name_to_announcement[char_to_name[press]],
                                              volume=ANNOUNCEMENT_VOLUME)
                    start(station_name=char_to_name[press],
                          volume=STREAM_VOLUME)
                    last_station_name = char_to_name[press]
                else:
                    if last_station_name is not None:
                        stop(last_station_name)
                    play_announcement_mplayer(announcement=ABSOLUTE_PATH + 'records/' + wrong_announcement,
                                              volume=ANNOUNCEMENT_VOLUME)
                    print('Wrong station number.')
