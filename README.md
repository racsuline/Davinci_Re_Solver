# Davinci Re-Solver for Linux

![Davinci Re-Solver Screenshot](https://i.imgur.com/gMSPTNO.png)

A simple Python-Flet app I made to practice what I've been learning in university, and honestly, for my own use since I'm on Linux and constantly need to convert videos to a format that works with DaVinci Resolve.

## What is this?

This program is far from being the best or the most sophisticated thing out there. It's basically just a more comfortable way to use ffmpeg tools for video conversion. just gets the job done.

## Why did I make this?

DaVinci Resolve on Linux can be picky with video formats. I got tired of typing ffmpeg commands over and over, so I wrapped them in a GUI. That's it.

## Installation

<a href="https://github.com/racsuline/Davinci_Re-Solver/releases"><img width='240' alt='Download AppImage' src='https://docs.appimage.org/_images/download-appimage-banner.svg'/></a>

Option 1 (Recommended): Integrate it with your system using something like [Gear Level](https://flathub.org/en/apps/it.mijorus.gearlever)

Option 2: Made it executable with `chmod +x DaVinci_Re-Solver-x86_64.AppImage`, then just open it.

## Note

This is a learning project and a personal tool made by a super new student. It works for what I need, but your mileage may vary. Feel free to fork it and have fun with it!

## Dependencies

This application **requires FFmpeg** to be installed on the system, use your package manager or check https://ffmpeg.org/download.html

## Acknowledgements

This project was made thanks to:

- **FFmpeg** – used for video conversion.
- **Flet** – UI framework used by this app.
