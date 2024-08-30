from colorama import Fore
from random import choice as rand
from shutil import get_terminal_size


banner1 = """             zeeeeee-
           d$$$$$$"
         d$$$$$P
      .$$$$$$"
    4$$$$$$$$$$$$$"
   \"\"\"\"\"\"\"3$$$$$"
        d$$$$"
     z$$$$$"
   d$$$$$$$$$$"
       .$$$"
     4$P"
   zP
"""


banner2 = """ *         .         ,AZZZZZZZZZZZ  `ZZ,_
                ,ZZZZZZV'      ZZZZ   `Z,`\\
              ,ZZZ    ZZ   .    ZZZZ   `V
    *      ZZZZV'     ZZ         ZZZZ    \\_
           V   l   .   ZZ        ZZZZZZ          .
           l    \\       ZZ,     ZZZ  ZZZZZZ,
          /            ZZ l    ZZZ    ZZZ `Z,
                      ZZ  l   ZZZ     Z Z, `Z,
            .        ZZ      ZZZ      Z  Z, `l
                     Z        ZZ      V  `Z   \\
                     V        ZZC     l   V
       Z             l        V ZR        l      .
        \                     l  ZA
                                  C          
                                  K      

"""


def get_line_len(text: str):
    """ get the longest line and return the lenght"""
    return max(len(line) for line in text.splitlines())


def centerText(text: str):
    """ center the text on the shell """
    terminal_size = get_terminal_size().columns
    line = get_line_len(text)
    space = " " * ((terminal_size - line) // 2)
    text = "\n".join(space + line for line in text.splitlines())

    return text


def banner():
    """ print a random banner with a random color """
    colors = [Fore.BLUE, Fore.RED, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW]
    banners = [banner1, banner2]

    random_banner = rand(banners)
    final_banner = centerText(random_banner)

    return (rand(colors) + final_banner + Fore.RESET)
