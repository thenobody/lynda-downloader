# Installation

```
    brew install chromedriver
```

# Running

To initialise the script:
```
    git clone git@github.com:thenobody/lynda-downloader.git
    cd lynda-downloader
    python lynda
```

Afterwards, use the Directory dialog to select the where the downloaded videos will be stored. The dialog might be opened in the background, just click to bring into focus.

After selecting the output directory, a Chrome window opens. Use this browser to:

1. navigate to the course you want to download (do this first!)
1. log in using the login form (do this second)

Logging in should automatically close the browser and the download should start automatically.

The output in the shell should look like this:

```
    ...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Waiting for browser login...
    Obtained session token: aaaaaa-ffff-1111.....
    Obtained course URL: https://www.lynda.com/The-course-you-selected/Some-page/12345-6.html
    
    (1/64) Downloading from https://lynda_files2-a.akamaihd.net/secure/courses/...mp4
    [#######                         ] 1234/8355 - 00:00:02
```

Finally, after downloading all the files the script should exit with message

```
    DONE!
``` 
  