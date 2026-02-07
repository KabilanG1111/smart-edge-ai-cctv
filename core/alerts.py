import winsound

# 🔔 VERY LOUD motion beep (system speaker)
def motion_beep():
    try:
        # Frequency (Hz), Duration (ms)
        winsound.Beep(2500, 700)  # HIGH pitch, long, aggressive
    except Exception as e:
        print("Motion sound error:", e)


# 🚨 Suspicious alert siren (keep WAV)
def alert_siren():
    try:
        winsound.PlaySound(
            "alert.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )
    except Exception as e:
        print("Alert sound error:", e)


def alert_console(duration):
    print(f"\033[91m⚠ ALERT: Suspicious activity | Duration: {duration:.2f}s\033[0m")
