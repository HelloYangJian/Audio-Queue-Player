# Audio-Queue-Player
一个基于Python的Windows音频播放器，可以播放主文件夹(A)中的WAV文件，并优先插播次文件夹(B)中的音频，支持可配置的播放模式。


# Audio Player Project

A Python-based audio player designed to run on Windows (x64). This program plays WAV audio files from a primary folder ("Folder A") either sequentially or randomly in a loop. It also monitors a secondary folder ("Folder B") for new WAV files. If files are found in Folder B, they are prioritized for playback (sorted by modification time, oldest first) after the currently playing audio from Folder A finishes. Once a file from Folder B is played, it is deleted. After all files in Folder B are processed, playback уютA continues from Folder A.

一个基于Python的音频播放器，专为Windows (x64) 系统设计。该程序可以循环播放主文件夹（“A文件夹”）中的WAV音频文件，支持顺序播放或随机播放。同时，它会监视一个次文件夹（“B文件夹”）中的新WAV文件。如果在B文件夹中检测到文件，它们将在当前A文件夹音频播放完毕后被优先播放（按修改时间从旧到新排序）。B文件夹中的文件每播放完毕一个即被删除。当B文件夹清空后，程序将继续播放A文件夹中的音频。

## Features 主要功能

*   **Primary Folder (Folder A) Playback A文件夹播放**:
    *   Plays all `.wav` files from a specified folder.
    *   Supports sequential or random playback mode (configurable).
    *   Loops playback indefinitely.
    *   从指定文件夹播放所有 `.wav` 文件。
    *   支持顺序或随机播放模式（可配置）。
    *   无限循环播放。
*   **Secondary/Interrupt Folder (Folder B) Playback B文件夹（插播）播放**:
    *   Monitors a specified folder for `.wav` files.
    *   If files are present, they are played after the current track from Folder A finishes.
    *   Files in Folder B are always played in order of their last modification time (oldest to newest).
    *   Each file from Folder B is deleted immediately after playback.
    *   监视指定文件夹中的 `.wav` 文件。
    *   如果存在文件，它们将在A文件夹当前曲目播放完毕后播放。
    *   B文件夹中的文件始终按其最后修改时间（从最早到最新）的顺序播放。
    *   B文件夹中的每个文件在播放完毕后立即被删除。
*   **Configuration via `config.ini` 通过 `config.ini` 配置**:
    *   Specify paths for Folder A and Folder B.
    *   Set playback mode for Folder A (random or sequential).
    *   指定A文件夹和B文件夹的路径。
    *   设置A文件夹的播放模式（随机或顺序）。
*   **Stable and Resource-Friendly 稳定且资源友好**:
    *   Uses `pygame` for audio playback.
    *   Designed to be stable and minimize system resource usage.
    *   使用 `pygame` 进行音频播放。
    *   设计力求稳定并最小化系统资源占用。
*   **Packagable 可打包**:
    *   Can be packaged into a standalone `.exe` executable using PyInstaller for use on Windows machines without a Python environment.
    *   可以使用 PyInstaller 打包成独立的 `.exe` 可执行文件，以便在没有Python环境的Windows机器上使用。

## Prerequisites 系统要求

*   Windows 11 (x64) (Tested on, should work on other Windows versions with x64 architecture)
*   Python 3.11.0 (x64) (for development or running from source)
*   Windows 11 (x64) （已在该系统测试，理论上支持其他x64架构的Windows版本）
*   Python 3.11.0 (x64) （用于开发或从源码运行）

## Setup and Installation 设置与安装

### 1. For Running from Source (从源码运行)

   a. **Clone the repository (克隆仓库):**
      ```bash
      git clone https://github.com/your-username/your-repository-name.git
      cd your-repository-name
      ```

   b. **(Recommended) Create a virtual environment (推荐创建虚拟环境):**
      ```bash
      python -m venv venv
      # On Windows
      .\venv\Scripts\activate
      # On macOS/Linux
      # source venv/bin/activate
      ```

   c. **Install dependencies (安装依赖):**
      Make sure your `pip` is using a fast mirror (e.g., Tsinghua mirror for users in China):
      ```bash
      pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
      ```
      Then install `pygame` and `configparser` (though `configparser` is standard in Python 3):
      ```bash
      pip install pygame
      ```

   d. **Configure `config.ini` (配置 `config.ini`):**
      Create or modify the `config.ini` file in the project root directory:
      ```ini
      [Settings]
      folder_a = ./A
      folder_b = ./B
      play_a_randomly = false
      # Set play_a_randomly to true for random playback of Folder A, false for sequential.
      # Paths can be relative (./A) or absolute (C:/Path/To/A).
      ```
      Ensure the specified `folder_a` and `folder_b` directories exist, or the program will attempt to create them. Place your `.wav` files accordingly.

   e. **Run the script (运行脚本):**
      ```bash
      python audio_player.py
      ```

### 2. For Using the Packaged Executable (使用打包好的EXE)

   (If an `.exe` is provided in releases or you package it yourself)
   (如果在Releases中提供了EXE文件，或者你自行打包)

   a. **Download/Obtain `AudioPlayer.exe` (下载/获取 `AudioPlayer.exe`).**
   b. **Create the necessary folder structure (创建必要的文件夹结构):**
      Place `AudioPlayer.exe` in a directory. In the same directory, create:
      *   A `config.ini` file (see example above).
      *   An `A` folder (or the path specified in `config.ini` for `folder_a`).
      *   A `B` folder (or the path specified in `config.ini` for `folder_b`).
      Example structure:
      ```
      MyAudioPlayer/
      ├── AudioPlayer.exe
      ├── config.ini
      ├── A/
      │   └── song1.wav
      │   └── sound_effect.wav
      └── B/
          └── alert.wav
      ```
   c. **Run `AudioPlayer.exe` (运行 `AudioPlayer.exe`).**

## Packaging (打包为 EXE)

If you want to package the script into a standalone executable:
如果你想将脚本打包成独立的可执行文件：

1.  **Install PyInstaller (安装 PyInstaller):**
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to the project directory in your terminal (在终端中进入项目目录).**
3.  **Run PyInstaller (运行 PyInstaller):**
    To create a single executable file (may show a console window):
    要创建一个单独的EXE文件（可能会显示控制台窗口）：
    ```bash
    pyinstaller --name AudioPlayer --onefile audio_player.py
    ```
    To create a single executable that doesn't show a console window (useful for background operation, but hides error messages):
    要创建一个不显示控制台窗口的EXE文件（适用于后台运行，但会隐藏错误信息）：
    ```bash
    pyinstaller --name AudioPlayer --onefile --windowed audio_player.py
    ```
    You can also add an icon:
    你也可以添加图标：
    ```bash
    pyinstaller --name AudioPlayer --onefile --icon=your_icon.ico audio_player.py
    ```
    (Replace `your_icon.ico` with the path to your icon file.)

4.  The executable `AudioPlayer.exe` will be found in the `dist` subfolder. Remember to distribute it along with `config.ini` and the `A`/`B` folder structure if relative paths are used in `config.ini`.
    可执行文件 `AudioPlayer.exe` 将位于 `dist` 子文件夹中。如果 `config.ini` 中使用了相对路径，请记得将其与 `config.ini` 以及 `A`/`B` 文件夹结构一起分发。

## Troubleshooting 故障排除

*   **"Pygame Mixer not initialized"**: Ensure your sound card drivers are up to date and working. Pygame might have issues with some audio setups.
    “Pygame Mixer 未初始化”：确保你的声卡驱动程序是最新的并且工作正常。Pygame 可能与某些音频设置存在兼容性问题。
*   **Audio files not playing or player "stuck"**:
    *   Ensure files are in `.wav` format. Pygame's WAV support is generally good for standard PCM WAVs. Very high bit-rate or unusual WAV encodings might cause issues.
    *   Try converting problematic WAV files to a standard format (e.g., 16-bit PCM, 44.1kHz or 48kHz) using an audio editor like Audacity.
    *   Check console output for error messages.
    音频文件不播放或播放器“卡住”：
    *   确保文件是 `.wav` 格式。Pygame 对标准 PCM WAV 的支持通常很好。非常高的比特率或不常见的WAV编码可能会导致问题。
    *   尝试使用像 Audacity 这样的音频编辑软件将有问题的WAV文件转换为标准格式（例如，16位 PCM，44.1kHz 或 48kHz）。
    *   检查控制台输出以获取错误信息。
*   **Files in Folder B not being deleted**: Check file permissions and ensure no other program is locking the files.
    B文件夹中的文件未被删除：检查文件权限，并确保没有其他程序正在锁定这些文件。

## Contributing 贡献

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.
欢迎贡献代码！请随时提交 Pull Request 或开启 Issue。

## License 许可证

This project is open-source. You can specify a license here (e.g., MIT, Apache 2.0). If you don't have one yet, MIT is a simple and permissive choice.
Example:
