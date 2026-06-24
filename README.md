# 🎵 Digital Lyric Display Companion

The Digital Lyrics Display Companion is an embedded vinyl record companion system designed to enhance the analog listening experience through digital technology. Built around an **Arduino Uno R3**, **1602A LCD**, **SD storage module**, and custom firmware, this system organizes vinyl collections, manages album metadata, and displays synchronized lyrics while a record plays.

The goal of this project is to create a personalized listening experience for vinyl collectors — preserving the physical feel of records while adding modern functionality.

---

## ✨ Features

### 🎛️ Embedded Vinyl Companion System
- Arduino Uno R3 powered control system
- 1602A LCD character display interface
- SD card based album and lyric storage
- Custom firmware for navigation and playback interaction
- Designed for physical vinyl collection management

### 💿 Album Library Management
- Stores album information locally
- Organizes:
  - Artist
  - Album title
  - Track listings
  - Lyrics w/ time stamps
- Optimized file formatting for embedded hardware limitations

### 🎤 Lyric Synchronization Display
- Displays song lyrics directly on the LCD screen
- Custom formatting for the 16x2 character display
- Line wrapping and spacing optimized for readability
- Designed around the limitations of embedded displays

---

# 🛠️ Tools & Technologies

## Hardware
| Component | Purpose |
|---|---|
| Arduino Uno R3 | Main microcontroller |
| 1602A LCD | User interface / lyric display |
| Micro SD Card Module | Storage for albums and lyrics |
| Vinyl Record Player | Analog music source |

## Software
- Arduino C/C++
- Python
- REST APIs
- File parsing
- Embedded system design

---

# 🧠 How It Works

SpinSync uses a combination of embedded firmware and Python automation tools to prepare and display album data.

### 1. Album Catalog Generation

A Python script automates the creation of the vinyl library by:

1. Searching **MusicBrainz** for album metadata
2. Retrieving the album tracklist
3. Querying the **Genius API** for song lyrics
4. Formatting the collected information into files compatible with the Arduino SD card system

This allows new albums to be added quickly without manually entering track information which saves time and adds convience for those with large collections.

---

### 2. Lyric Formatting Pipeline

Because the LCD 1602A has strict display limitations, a second Python utility script prepares lyrics by:

- Splitting long lyric lines
- Formatting text for a 16-character display width
- Removing incompatible formatting
- Creating display-ready lyric files

This script acts as a fallback when automatic lyric retrieval fails or when lyrics require manual cleanup.

---

# 📂 Project Structure
SpinSync/
│
├── Arduino/
│ ├── SpinSync.ino
│ └── libraries/
│
├── Python/
│ ├── album_catalog.py
│ └── lyric_formatter.py
│
├── SD_Card/
│ ├── albums/
│ └── lyrics/
│
└── README.md


---

# 🚀 Future Improvements

- [ ] Implement automatic song detection
- [ ] Add Bluetooth audio metadata support
- [ ] Upgrade to a graphical display
- [ ] Create a companion desktop application
- [ ] Add support for multiple vinyl collections
- [ ] Improve lyric timing synchronization
- [ ] Create a chassis for the system itself.
- [ ] Improve hardware to avoid specific hardware constraints.

---

# 🎯 Project Goals

SpinSync explores the intersection of:

- Embedded systems
- Hardware/software integration
- Digital music services
- Automation scripting
- Human-centered design

The project demonstrates how modern computing can enhance traditional media without replacing the original experience.

---

# 👨‍💻 Author

**Nicolas Capetillo**

I created this project with the intent of creating something unique and important to me. Combining my hobbies with my engineering work allows me to stay creative while continuuing to develop my skills. This project came to me while I was looking for more equipment to add to my record collection and turntable setup. While there are products available with the purpose of audio vidualization through the use of built in microphones, I realized there are very few (if any) smart products designed specifically to display the lyrics of the music being played. In my opinion, adding lyric visualization to a vinyl setup creates a more immersive and personalzed expereince while complementing the aesthetic of a physical music collection. 

Computer Engineering Student at Texas Tech University
Embedded Systems | Software Development | Hardware Projects

---

⭐ If you enjoy the project, consider giving it a star!
