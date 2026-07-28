# Startup
We create the codechef contest and enter the URL in the config file (.seb) and the config file is shared when you click on start contest.
Important things to configure in SEB:
- Allowed/blocked applications
- Clipboard restrictions
- Browser restrictions
- Kiosk mode/fullscreen lock
- Start URL (For them to decide)
- Quit password (Decided every new round)

# User is using SEB
1. Check if SEB is there in user-agent header

# Don't forget while configuring
1. Full Kiosk mode
2. URL Filtering
3. Regex \.*$
4. Quit password
5. Config is for starting exam
6. Admin password
7. Allow our process
    - Recorder
    - Sender
8. Set encryption key
9. Allow uploading our media files
10. Remove edit config file option
11. The recorder set to auto-start

# Script should
1. Check whether windows or macOS
- If .exe, download a script (whose relative location I'll pass) to "C:\ProgramData\ExamRecorder\recorder.exe"
- Else, download to ~/Applications/recorder.app
2. Open .seb, also from url
3. Wait n (passed in env) hours and then kill the recorder, delete it and then itself as well
Obviously, after they download it, they'll manually run the .exe/.app

# Doubts
1. What all websites to allow ?
- W3schools
- The local URL, allow network to our endpoints
    - Verifying
    - Storing
2. What all browsers to allow ?
- Chrome
- Firefox
- Edge
- Brave