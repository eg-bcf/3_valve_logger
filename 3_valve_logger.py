import tkinter as Tkinter
import serial
import time

class App:
    def __init__(self, master):

        frame = Tkinter.Frame(master)

        self.arduino = serial.Serial(
            "COM20",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        self.valve1 = []
        self.valve2 = []
        self.valve3 = []
        self.readStatus = 0

        self.file_path = Tkinter.StringVar()
        self.file_path.set("Sample")
        self.directory_path = Tkinter.StringVar()
        self.directory_path.set("C:\\Users\\egardner\\Desktop")

        self.save_options = Tkinter.LabelFrame(frame, text="Save Options", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.save_options.grid(row=0, column=0, padx=20, pady=20)

        self.directory_label = Tkinter.Label(self.save_options, text="Save the file to this Directory")
        self.directory_label.grid(row=0, column=0, padx=5, pady=5)

        self.directory_name = Tkinter.Entry(self.save_options, textvariable=self.directory_path)
        self.directory_name.grid(row=1,column=0, padx=5, pady=5)

        self.name_label = Tkinter.Label(self.save_options, text="Save the file to this Directory")
        self.name_label.grid(row=2, column=0, padx=5, pady=5)

        self.file_name = Tkinter.Entry(self.save_options, textvariable=self.file_path)
        self.file_name.grid(row=3,column=0, padx=5, pady=5)

        self.save_button = Tkinter.Button(self.save_options, text="Save", bd=10, height=5, width=10, command=self.saveFile)
        self.save_button.grid(row=4, column=0, padx=5, pady=5)

        self.read_button = Tkinter.Button(self.save_options, text="Read", bd=10, height=5, width=10, command=self.readArduino)
        self.read_button.grid(row=5, column=0, padx=5, pady=5)

        self.stop_arduino_button = Tkinter.Button(self.save_options, text="Stop Arduino", bd=10, height=5, width=10, command=self.stopArduino)
        self.stop_arduino_button.grid(row=6, column=0, padx=5, pady=5)

        self.start_arduino_button = Tkinter.Button(self.save_options, text="Start Arduino", bd=10, height=5, width=10, command=self.startArduino)
        self.start_arduino_button.grid(row=7, column=0, padx=5, pady=5)

        self.flush_port_button = Tkinter.Button(self.save_options, text="Flush Port", bd=10, height=5, width=10, command=self.flushPort)
        self.flush_port_button.grid(row=8, column=0, padx=5, pady=5)

        frame.grid(row=0, column=0, padx=20, pady=20)

    def saveFile(self):
        dname = self.directory_path.get()
        fname = self.file_path.get()
        ftype = ".txt"
        full_path = dname + '\\' + fname + ftype
        print(full_path)
        F = open(full_path,"w+")
        for x in range(0,max(len(self.valve1), len(self.valve2), len(self.valve3))-1):
            try:
                F.write(str(self.valve1[x]))
            except:
                print("No Value")
            F.write("\t")
            try:
                F.write(str(self.valve2[x]))
            except:
                print("No Value")
            F.write("\t")
            try:
                F.write(str(self.valve3[x]))
            except:
                print("No Value")
            F.write("\n")
        F.close()

    def readArduino(self):
        self.valve1 = []
        self.valve2 = []
        self.valve3 = []
        self.analogRead()

    def analogRead(self):
        if self.readStatus == 1:
            x = self.arduino.readline()
            decoded = str(x.decode('utf-8').strip())
            value = decoded.split(':')
            if len(value) > 1:
                if value[0] == '0':
                    self.valve1.append(value[1].strip())
                if value[0] == '1':
                    self.valve2.append(value[1].strip())
                if value[0] == '2':
                    print('!!!!')
                    self.valve3.append(value[1].strip())
            root.after(1, self.analogRead)
        else:
            pass

    def startArduino(self):
        self.readStatus = 1
        startString = "<B>"
        self.arduino.write(startString.encode())


    def stopArduino(self):
        self.readStatus = 0
        stopString = "<A>"
        self.arduino.write(stopString.encode())

    def flushPort(self):
        self.arduino.flushInput()

if __name__ == "__main__":
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
