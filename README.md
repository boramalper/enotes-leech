# enotes-leech

[enotes-leech](https://github.com/boramalper/enotes-leech) is a Python 3 script to downloadd all study guides and e-texts on enotes.com. Instead of subscribing for a year
(or even worse, for years) you can subscribe only for a month and download everything on the website. It might be also useful
in cases where internet connection is slow or unreliable.

## Is it legal?
__Yes, it is legal.__ If you have a eNotes subscription, there is nothing that prohibits you from downloading whatever you can -whether
automatized or not- on eNotes.

You can check their [Terms of Service](https://www.enotes.com/help/tos) yourself (last checked on 16 February 2017).

## How to use?
1. Edit `enotes-leech.py` and enter your username and password.
2. Run
   ```
   python3 ./enotes-leech.py
   ```
       
   wait download to finish. You need to keep an eye in case one of the files fails to download.
   
In case of an error, you can edit* the `guides.json` file in the working directory and remove all the already downloaded guides
(and e-texts) from the list including the erroneous one. Afterwards you can continue downloading by:

    python3 ./enotes-leech.py guides.json
    
*: Sorry for making you edit huge json files. You can use Notepad++ or an equivalent powerful text editor to format JSON before
editing and also to be able to handle large files.

## Requirements
* requests
* BeautifulSoup 4
