import tkinter as tk
import customtkinter as ctk
from PIL import Image
from Main import Main
from Logs import Logs
import threading
import os
from Tooltip import ToolTip


class CragListUi:
    def __init__(self):
        super().__init__()
        self.root = ctk.CTk()
        self.root.title('Craglist Scrap')
        self.root.geometry('550x500')

        self.images = {
            'bg_img': ctk.CTkImage(
                light_image=Image.open("app_bg.png"),
                dark_image=Image.open("app_bg.png"),
                size=(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            ),
            'info': ctk.CTkImage(
                light_image=Image.open("info.png"),
                dark_image=Image.open("info.png"),
                size=(20, 20)
            ),
        }

        self.radio_var = None
        self.button = None
        self.heading = None
        self.sub_heading = None
        self.delete_frames = []
        self.time_slider = None
        self.t_slider = None
        self.main = Main()
        self.logs = Logs()
        self.prev_log = ""
        self.stop = False
        self.browser = None
        self.car_bike = None
        self.scrollable_frame = None
        

    def stop_app(self):
        self.stop = False
        self.main.stop_thread()

        # Change button back to Next
        if self.button:
            self.button.configure(text="Next", command=lambda: self.get_config(self.time_slider, self.t_slider, self.browser, self.car_bike))

        # Destroy scraping log frame if exists
        if self.scrollable_frame and self.scrollable_frame.winfo_exists():
            self.scrollable_frame.destroy()

        # Restore config page
        self.start_app()

    def update_logs(self):
        """Update logs safely in UI."""
        if not self.stop:
            return

        if not (self.scrollable_frame and self.scrollable_frame.winfo_exists()):
            return

        log = self.logs.read_latest_data_from_file()
        if self.prev_log != log and log != "":
            self.prev_log = log
            try:
                label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text_color="#FFFFFF",
                    text=log,
                    bg_color="#1d1028",
                    font=("Montserrat", 12)
                )
                label.pack()
            except tk.TclError:
                return

        self.root.after(2000, self.update_logs)

    def main_page(self):
        for frame in self.delete_frames:
            try:
                if frame.winfo_exists():
                    frame.destroy()
            except Exception:
                pass

        self.sub_heading.configure(text="Scrapping Logs")

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.root, width=400, height=250, fg_color="#1d1028"
        )
        self.scrollable_frame.place(relx=0.1, rely=0.3)

        self.button.configure(text="Stop", command=self.stop_app)

        if self.stop:
            self.update_logs()
            
    

    def start_thread(self):
        print("OKAYYY")
        self.stop = True

        # run UI updates inside mainloop
        self.root.after(0, self.main_page)

        # run backend scraper in thread
        backend = threading.Thread(
            target=self.main.backend_app,
            args=(self.t_slider, self.time_slider, self.browser, self.car_bike),
            daemon=True
        )
        backend.start()

    def get_config(self, time_slider, t_slider, browser, car_bike):
        self.time_slider = int(time_slider.get())
        self.t_slider = int(t_slider.get())
        self.browser = browser.get()
        if car_bike:
            self.car_bike = car_bike.get()
        self.start_thread()

    def start_app(self):
        try:
            os.remove("crag_all_log.txt")
            os.remove("ERROR.txt")
            os.remove("SUCCESS.txt")
        except Exception:
            pass

        image_label = ctk.CTkLabel(self.root, image=self.images['bg_img'], text="")
        image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.heading = ctk.CTkLabel(
            self.root, text="CragList SCRAP", text_color="white",
            font=("Montserrat", 20), fg_color="#110618"
        )
        self.heading.pack(anchor='n', pady=20)

        self.sub_heading = ctk.CTkLabel(
            self.root, text="Configure Bot", text_color="white",
            font=("Montserrat", 20), fg_color="#110618"
        )
        self.sub_heading.pack(anchor='n', pady=40)

        for frame in self.delete_frames:
            try:
                if frame.winfo_exists():
                    frame.destroy()
            except Exception:
                pass

        config_frame = ctk.CTkFrame(
            master=self.root,
            width=self.root.winfo_screenwidth() - 200,
            height=self.root.winfo_screenheight() - 200,
            fg_color="#280b3b"
        )
        config_frame.place(relx=0.05, rely=0.4)

        # Threshold slider
        thresh_info = ctk.CTkLabel(config_frame, image=self.images['info'], text="")
        thresh_info.grid(row=0, column=0, sticky='w')
        ToolTip(thresh_info, "Threshold = number of days scraper should fetch with phone number")

        slide_label = ctk.CTkLabel(
            config_frame, text_color="#FFFFFF", text="Threshold",
            bg_color="#280b3b", font=("Montserrat", 18)
        )
        slide_label.grid(row=0, column=0, padx=25, sticky='w')

        t_slider = ctk.CTkSlider(
            config_frame, from_=0, to=5000,
            bg_color="#280b3b", fg_color="black",
            progress_color="#cc92f2", button_color="#cc92f2",
            button_hover_color="#cc92f2"
        )
        t_slider.grid(row=0, column=1, padx=30, sticky='w')
        t_slider.set(0)

        t_label = ctk.CTkLabel(
            config_frame, text="", text_color="#FFFFFF",
            bg_color="#280b3b", font=("Montserrat", 18)
        )
        t_label.grid(row=0, column=2, sticky='w')

        def update_value_t(val):
            t_label.configure(text=str(int(t_slider.get())) + ">>")

        t_slider.configure(command=update_value_t)

        # Sleep slider
        time_info = ctk.CTkLabel(config_frame, image=self.images['info'], text="")
        time_info.grid(row=1, column=0, sticky='w')
        ToolTip(time_info, "Adjust sleep time depending on internet speed")

        time_label = ctk.CTkLabel(
            config_frame, text_color="#FFFFFF", text="Sleep",
            bg_color="#280b3b", font=("Montserrat", 18)
        )
        time_label.grid(row=1, column=0, padx=25, pady=5, sticky='w')

        time_slider = ctk.CTkSlider(
            config_frame, from_=0, to=100,
            bg_color="#280b3b", fg_color="black",
            progress_color="#cc92f2", button_color="#cc92f2",
            button_hover_color="#cc92f2"
        )
        time_slider.grid(row=1, column=1, padx=35, sticky='w')
        time_slider.set(0)

        time_val = ctk.CTkLabel(
            config_frame, text="", text_color="#FFFFFF",
            bg_color="#280b3b", font=("Montserrat", 18)
        )
        time_val.grid(row=1, column=2, sticky='w')

        def update_value_time(val):
            time_val.configure(text=str(int(time_slider.get())) + "s")

        time_slider.configure(command=update_value_time)

        # Car or Bike
        car_info = ctk.CTkLabel(config_frame, image=self.images['info'], text="")
        car_info.grid(row=2, column=0, sticky='w')
        ToolTip(car_info, "Choose whether to scrape Cars or Bikes")

        car_bike_label = ctk.CTkLabel(
            config_frame, text_color="#FFFFFF", text="Choose the target",
            bg_color="#280b3b", font=("Montserrat", 18)
        )
        car_bike_label.grid(row=2, column=0, padx=25, pady=5, sticky='w')

        car_or_bike = ctk.CTkComboBox(
            config_frame, values=["Cars/Trucks", "Bike"],
            text_color="#FFFFFF", fg_color="#280b3b",
            bg_color="#280b3b", button_color="#cc92f2",
            border_color="#cc92f2", button_hover_color="#cc92f2"
        )
        car_or_bike.grid(row=2, column=1, padx=30, pady=5, sticky='w')

        # Browser type
        brow_info = ctk.CTkLabel(config_frame, image=self.images['info'], text="")
        brow_info.grid(row=3, column=0, sticky='w')
        ToolTip(brow_info, "Head = visible browser\nHeadless = hidden browser")

        browser_target = ctk.CTkLabel(
            config_frame, text="Choose the Type",
            bg_color="#280b3b", font=("Montserrat", 18), text_color="#FFFFFF"
        )
        browser_target.grid(row=3, column=0, padx=25, pady=5, sticky='w')

        head_headless = ctk.CTkComboBox(
            config_frame, values=["Headless", "Head"],
            text_color="#FFFFFF", fg_color="#280b3b",
            bg_color="#280b3b", button_color="#cc92f2",
            border_color="#cc92f2", button_hover_color="#cc92f2"
        )
        head_headless.grid(row=3, column=1, padx=30, pady=5, sticky='w')

        self.button = ctk.CTkButton(
            self.root, text="Next", fg_color="#cc92f2",
            hover_color="#2e044a",
            command=lambda: self.get_config(time_slider, t_slider, head_headless, car_or_bike)
        )
        self.button.place(relx=0.35, rely=0.9)

        self.delete_frames.append(config_frame)
        self.root.mainloop()


if __name__ == "__main__":
    KU = CragListUi()
    KU.start_app()
