import pygame
import os
import glob
import time
import random
import configparser

CONFIG_FILE = 'config.ini'

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print(f"错误：配置文件 {CONFIG_FILE} 不存在。")
        print(f"将创建默认配置文件 {CONFIG_FILE}，请根据您的需求修改路径。")
        config['Settings'] = {
            'folder_a': './A',  # 默认A文件夹在程序同级目录
            'folder_b': './B',  # 默认B文件夹在程序同级目录
            'play_a_randomly': 'false'
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            print(f"已创建默认配置文件 {CONFIG_FILE}。")
        except IOError as e:
            print(f"错误：无法创建默认配置文件 {CONFIG_FILE}: {e}")
            return None
        # 即使创建了，也返回 None 提示用户检查并首次运行可能需要重启
        # 或者直接使用这些默认值继续，但最好是提示用户
        print("请检查并修改配置文件后重新运行程序，或确保默认文件夹A和B存在。")
        # return None # 如果希望强制用户配置

    try:
        config.read(CONFIG_FILE, encoding='utf-8')
    except Exception as e:
        print(f"错误：读取配置文件 {CONFIG_FILE} 失败: {e}")
        return None
    
    settings = {}
    try:
        # 使用 os.path.abspath 确保我们处理的是绝对路径，这在打包后更可靠
        # 如果config中的路径已经是绝对路径，abspath不会改变它
        # 如果是相对路径，它会相对于当前工作目录转换（脚本运行时就是脚本所在目录）
        settings['folder_a'] = os.path.abspath(config.get('Settings', 'folder_a', fallback='./A'))
        settings['folder_b'] = os.path.abspath(config.get('Settings', 'folder_b', fallback='./B'))
        settings['play_a_randomly'] = config.getboolean('Settings', 'play_a_randomly', fallback=False)
    except configparser.NoSectionError:
        print(f"错误：配置文件 {CONFIG_FILE} 中缺少 [Settings] 部分。")
        return None
    except configparser.NoOptionError as e:
        print(f"错误：配置文件 {CONFIG_FILE} 中缺少选项: {e.option}")
        return None
    except ValueError as e:
        print(f"错误：配置文件中的值格式不正确 (例如 play_a_randomly 应该是 true/false): {e}")
        return None
        
    # 确保配置的文件夹存在，如果不存在则尝试创建
    for folder_key, folder_path in [('folder_a', settings['folder_a']), ('folder_b', settings['folder_b'])]:
        if not os.path.isdir(folder_path):
            print(f"警告：配置的文件夹 '{folder_path}' (用于 {folder_key}) 不存在。")
            try:
                print(f"尝试创建文件夹: {folder_path}")
                os.makedirs(folder_path, exist_ok=True)
                print(f"已创建文件夹: {folder_path}")
            except OSError as e:
                print(f"错误：无法创建文件夹 {folder_path}: {e}")
                print("请手动创建该文件夹或检查路径权限。")
                return None # 创建失败则无法继续
    return settings

def get_audio_files(folder_path, sort_key_func=None, shuffle=False):
    """
    获取指定文件夹中的WAV文件列表。
    folder_path: 文件夹路径。
    sort_key_func: 用于排序的函数 (例如 os.path.getmtime)。如果为None，则按名称排序。
    shuffle: 是否随机打乱列表。
    """
    if not os.path.isdir(folder_path):
        # print(f"文件夹 {folder_path} 不存在或不是一个目录。") # 主循环中会打印，这里可以静默
        return []
    
    # 使用绝对路径查找，避免相对路径问题
    wav_files = glob.glob(os.path.join(os.path.abspath(folder_path), "*.wav"))
    # 再次确保获取的是绝对路径，glob有时在特定情况下可能返回相对的
    wav_files = [os.path.abspath(f) for f in wav_files]

    if shuffle:
        random.shuffle(wav_files)
    elif sort_key_func:
        # 对于可能的文件名数字排序，可以考虑更复杂的排序键，但标准sort对一般情况够用
        wav_files.sort(key=sort_key_func)
    else:
        wav_files.sort() # 默认按名称排序
        
    return wav_files

def play_audio_file(file_path):
    """
    播放单个音频文件并等待其结束。
    返回 True 如果播放成功结束，否则返回 False。
    """
    if not os.path.exists(file_path):
        print(f"  错误：音频文件 {file_path} 不存在，跳过。")
        return False
    if not pygame.mixer.get_init():
        print("  错误：Pygame mixer尚未初始化，无法播放。")
        return False
        
    try:
        print(f"  > 正在播放: {os.path.basename(file_path)}")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # 等待音乐播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30) # 降低CPU占用，每秒检查约30次
            # 允许pygame事件处理，例如QUIT事件（虽然我们这里是控制台应用）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("  Pygame请求退出...")
                    return False # 提前终止播放
        # print(f"  --播放完成: {os.path.basename(file_path)}") # 调试信息
        return True
    except pygame.error as e:
        print(f"  错误：播放音频 {os.path.basename(file_path)} 失败: {e}")
        # 尝试停止并卸载以防万一
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except pygame.error:
                pass # 忽略停止/卸载时的错误
        return False
    except Exception as e:
        print(f"  错误：播放时发生未知错误 {os.path.basename(file_path)}: {e}")
        return False

def main():
    """主程序逻辑"""
    print("--- 音频播放器启动 ---")
    config = load_config()
    if not config:
        print("无法加载配置或配置文件夹创建失败，程序退出。")
        input("按 Enter 键退出...")
        return

    folder_a = config['folder_a']
    folder_b = config['folder_b']
    play_a_randomly = config['play_a_randomly']

    print(f"A文件夹路径: {folder_a}")
    print(f"B文件夹路径: {folder_b}")
    print(f"A文件夹播放模式: {'随机' if play_a_randomly else '顺序'}")
    print(f"B文件夹播放模式: 名称顺序")
    print("------------------------")


    try:
        pygame.init() # 初始化所有pygame模块，包括mixer
        pygame.mixer.init() # 显式初始化mixer，可以指定参数如frequency, channels等
        print("Pygame Mixer 已成功初始化。")
    except pygame.error as e:
        print(f"严重错误：无法初始化Pygame Mixer: {e}")
        print("请确保您的系统已正确安装声卡驱动和相关音频库。")
        print("程序无法继续。")
        input("按 Enter 键退出...")
        return

    current_a_playlist = []
    current_a_index = 0
    running = True

    try:
        while running:
            # --- A 文件夹处理 ---
            if not current_a_playlist or current_a_index >= len(current_a_playlist):
                print("\n[A] 正在加载/刷新 A 文件夹播放列表...")
                current_a_playlist = get_audio_files(folder_a, shuffle=play_a_randomly)
                current_a_index = 0
                if not current_a_playlist:
                    print(f"[A] 文件夹 '{os.path.basename(folder_a)}' 为空或没有 .wav 文件。等待10秒后重试...")
                    for _ in range(100): # 10秒，每0.1秒检查一次退出
                        time.sleep(0.1)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: running = False; break
                        if not running: break
                    if not running: break
                    continue
                print(f"[A] 播放列表已加载 ({len(current_a_playlist)} 个文件)。模式: {'随机' if play_a_randomly else '顺序'}")

            if not running: break # 检查循环条件

            a_file_to_play = current_a_playlist[current_a_index]
            print(f"\n[A] 准备播放: {os.path.basename(a_file_to_play)}")
            played_a_successfully = play_audio_file(a_file_to_play)
            
            # 播放完A文件后，卸载它以释放句柄，特别是如果和B中文件重名或路径问题
            if played_a_successfully and pygame.mixer.get_init():
                try:
                    pygame.mixer.music.unload()
                    # print(f"  --已卸载 A 文件: {os.path.basename(a_file_to_play)}") # 调试
                except pygame.error as e:
                    print(f"  警告: 卸载A文件 {os.path.basename(a_file_to_play)} 时发生错误: {e}")
            
            current_a_index += 1
            if not running: break # 检查循环条件

            # --- B 文件夹处理 ---
            print(f"\n[B] 检查 B 文件夹 '{os.path.basename(folder_b)}'...")
            b_files = get_audio_files(folder_b) # 默认按名称排序

            if b_files:
                print(f"[B] 在 B 文件夹中找到 {len(b_files)} 个音频文件，将优先播放 (按名称顺序)。")
                for b_file_path in b_files:
                    if not running: break # 允许在B文件播放队列中途退出

                    print(f"[B] 准备播放: {os.path.basename(b_file_path)}")
                    b_played_successfully = play_audio_file(b_file_path)
                    
                    if b_played_successfully: 
                        # 关键：播放完B文件后，停止、卸载并稍作等待，然后删除
                        if pygame.mixer.get_init():
                            try:
                                pygame.mixer.music.stop()  # 确保停止
                                pygame.mixer.music.unload()# 卸载以释放文件句柄
                                # print(f"  --已卸载 B 文件: {os.path.basename(b_file_path)}") # 调试
                            except pygame.error as e:
                                print(f"  警告: 停止/卸载B文件 {os.path.basename(b_file_path)} 时发生错误: {e}")
                        
                        time.sleep(0.3) # 给系统时间释放文件句柄，可根据情况调整

                        try:
                            os.remove(b_file_path)
                            print(f"  >> 已删除 B 文件: {os.path.basename(b_file_path)}")
                        except OSError as e:
                            print(f"  错误：无法删除文件 {os.path.basename(b_file_path)}: {e}")
                        except Exception as e: 
                            print(f"  错误：删除文件时发生未知错误 {os.path.basename(b_file_path)}: {e}")
                    else:
                        print(f"  未能成功播放 B 文件 {os.path.basename(b_file_path)}，跳过删除。")
                    
                    if not running: break # 检查循环条件
                
                if running: # 只有在未被中断的情况下才打印完成信息
                    print("[B] B 文件夹中的音频已全部处理完毕。")
            else:
                if running: # 只有在未被中断的情况下才打印
                    print("[B] 文件夹为空或没有 .wav 文件。")

            # 在下一次循环前处理pygame事件，并稍作延时
            if running:
                for event in pygame.event.get(): # 处理pygame队列中的事件
                    if event.type == pygame.QUIT: # 虽然是控制台，但pygame内部可能有此事件
                        running = False
                time.sleep(0.1) # 短暂延时，避免CPU空转过快

    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，程序正在退出...")
        running = False #确保循环会终止
    except Exception as e:
        print(f"\n发生未处理的致命异常: {e}")
        import traceback
        traceback.print_exc() # 打印详细的堆栈跟踪
        running = False
    finally:
        print("\n--- 播放器正在停止 ---")
        if pygame.mixer.get_init(): 
            print("停止所有播放并退出Mixer...")
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        if pygame.get_init(): # 如果pygame主模块也初始化了
            pygame.quit() # 清理所有pygame模块
        print("播放器已停止。")
        input("按 Enter 键关闭窗口...")


if __name__ == '__main__':
    # 确保在打包后，相对路径是相对于可执行文件的
    # 如果脚本是直接运行，os.path.dirname(os.path.abspath(__file__))是脚本所在目录
    # 如果是通过pyinstaller打包的 --onefile 模式，sys.executable 是exe的路径
    # getattr(sys, 'frozen', False) 可以判断是否是打包状态
    import sys
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # 如果是 PyInstaller 打包的，并且是 one-file 模式
        # 程序的工作目录通常是exe所在的目录，所以相对路径 `./A` `./B` 和 `config.ini` 会在exe旁边查找
        # 但如果config.ini中指定了绝对路径，则以绝对路径为准
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path) # 确保当前工作目录是exe所在目录
        print(f"程序运行目录 (打包后): {application_path}")
    else:
        # 如果是直接运行 .py 文件
        application_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(application_path) # 确保当前工作目录是脚本所在目录
        print(f"程序运行目录 (脚本): {application_path}")
        
    main()