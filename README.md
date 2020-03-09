# snapchat-takeout
## Snapchat Takeout (GDPR) Memories Downloader
This Python application downloads memories from Snapchat servers to local disk

When [requesting your data from Snapchat](https://accounts.snapchat.com/accounts/downloadmydata) they sadly only include a .json file which contains a seperate download link for each memory file.
This application parses the .json file and does it's best to download the files to local disk.

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
I promise that i did my best not to do any bullshit but Iam just a human as you are. (To make things worse: Iam Student atm) Well, you guessed it: we make mistakes so please __Don't trust this application in any means. I will not take any damage coaused by this application on me__
