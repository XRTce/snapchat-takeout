# snapchat-takeout
## Snapchat Takeout (GDPR) Memories Downloader
### This Python3 application downloads your media files ( known as memories) from Snapchat servers to your local disk.

When [requesting your data from Snapchat](https://accounts.snapchat.com/accounts/downloadmydata) they sadly only include a .json file which contains a seperate download link for each memory file.
This application parses the .json file and does it's best to download the files to local disk.

**Iam grateful for any suggestions/tips for improvement. This is my first Python project**

### Features:
- File Handling
  - Apply naming sheme (Default: "Snapchat-YYYY-MM-DD_HHMMSS\[\_1..n\].ext")
  - Recursive naming of files created with same timestamp (the optional \[\_1..n] part above)
  - Existing Files are skipped
- Error Handling
  - Log failed Downloads
- Restart download at any time (download progress is logged)
- Stats after completion
- Status output while downloading
- maybe i forgot some, it's been a long day ¯\\\_(ツ)\_/¯

### Disclaimer:
I promise: i did my best not making any mistakes but Iam just a human as you are. (worse: iam a Student) Well, you guessed it: we make mistakes so please **Don't trust this application before you read and understood the code, it is commented. I will not take any damage coaused by this application on me**

### Usage
1. Put your `memories_history.json` file into the project's root folder
2. Run `app.py`

You should end up with the following file structure:
- `./media/Snapchat-xxx` <-- Your downloaded files
- `./errors.txt` <-- Failed files including failed download links
- `./downloaded.txt` <-- All successfull downloaded Links

If the app is stopped during runtime it resumes after the last downloaded file (for this to work dont delete `downloaded.txt`)
It is possible to change the timezone for appling the file naming sheme, media folder and the file naming sheme inside the code as you should've noticed becuase you read and understood the code ;) 

### Screenshots
Downloading files:
---
![downloading](https://github.com/cmd-k/snapchat-takeout/raw/master/screenshots/downloading.png)

Skipping existing files:
---
![skipped](https://github.com/cmd-k/snapchat-takeout/raw/master/screenshots/skipped.png)

Duplicate file handling:
---
![duplicate](https://github.com/cmd-k/snapchat-takeout/raw/master/screenshots/duplicate.png)

Download error:
---
![error](https://github.com/cmd-k/snapchat-takeout/raw/master/screenshots/error.png)

Stats after finished task:
---
![stats](https://github.com/cmd-k/snapchat-takeout/raw/master/screenshots/stats.png)
