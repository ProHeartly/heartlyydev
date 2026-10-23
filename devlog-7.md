# MAILING CODE: SUCESS!

So I wanted to make like mailing system for addressing the code for authorization. SO, I used the mail that hackclub.app gave aka da @user.hackclub.app mail.

# Progress:
1) I initially thought of using my own mail from domain: @heartlyy.dev but turns out there are many issues to it; like the mail going into spam, needing dedicated ipv4 host and many more. So I switched to @user.hackclub.app mail.
![alt text](images/image17.png)

**Direction for recreation:**
* make a .env file with
    ```
        ADMIN_MAIL= {mail of the one to recieve code}
        MAIL_PASS= {password of @user.hackclub.app}
        SESSION_SECRET=Xk3v9Qm_2LpZ8wRt # a long session text or jebrish
    ```