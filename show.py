import os 
import sys
import tkinter
from PIL import Image, ImageTk
from datetime import date

# showtime is in milliseconds so for a day 1000 * 60 * 60 * 24
def show_image_in_fullscreen(img_path, show_time = 2000 ):

    pilImage = Image.open(img_path)
    app = tkinter.Tk()
    w, h = app.winfo_screenwidth(), app.winfo_screenheight()
    app.overrideredirect(1)
    app.geometry("%dx%d+0+0" % (w, h))
    app.focus_set()    
    app.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(app,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w / 2, h / 2, image=image)
    app.after(show_time, lambda: app.destroy()) 
    app.mainloop()


def load_images(path):

    img_paths = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.lower().endswith(".jpg"):
                img_paths.append(os.path.join(root,f))
    return img_paths


def get_pic_of_the_day(img_paths, test_date=None):

    if not test_date:
        today = date.today()
        formatted_date = today.strftime("%Y-%m-%d")
    else:
        formatted_date = test_date
    for img_path in img_paths:
        if formatted_date in img_path:
            return img_path
    # return dummy path if nothing found
    return None

if __name__ == "__main__":

    image_paths = load_images(sys.argv[1])
    while True:
        pic_of_the_day = get_pic_of_the_day(image_paths, test_date="2020-09-23")
        if pic_of_the_day:
            show_image_in_fullscreen(pic_of_the_day)
        else:
            break
