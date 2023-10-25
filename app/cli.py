import argparse

from .lyrics import print_spotify_now_playing_lyrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', help='foo help')

    print_spotify_now_playing_lyrics()
