#tui chỉ thay đổi giao diện cho nó đẹp với sửa lại cái array, còn lại phần công thức k sửa gì hết tại sợ k hiểu :^)

import turtle
import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
# from mpl_toolkits.mplot3d import art3d

def format_scientific(value):
    #cướp trên stackoverflow
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.4f}×10^{exponent}"

def get_input():
    #cửa sổ nhập input
    result = {'ok': False} #xem thêm dict python, ok để kiểm tra có nhập đúng ko
    
    root = tk.Tk()
    root.title("Mô phỏng từ trường vòng dây tròn")
    root.geometry("400x300")
    
    r_var = tk.StringVar()
    x0_var = tk.StringVar()
    y0_var = tk.StringVar()
    z0_var = tk.StringVar()
    o_var = tk.StringVar()
    
    title = ttk.Label(root, text="Tính toán từ trường vòng dây tròn", 
                     font=("Arial", 14, "bold"))
    title.pack(pady=10)
    
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Bán kính vòng dây (m):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    ttk.Entry(frame, textvariable=r_var, width=20).grid(row=0, column=1, pady=5)
    
    ttk.Label(frame, text="Tọa độ X điểm cần tính (m):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    ttk.Entry(frame, textvariable=x0_var, width=20).grid(row=1, column=1, pady=5)
    
    ttk.Label(frame, text="Tọa độ Y điểm cần tính (m):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
    ttk.Entry(frame, textvariable=y0_var, width=20).grid(row=2, column=1, pady=5)
    
    ttk.Label(frame, text="Tọa độ Z điểm cần tính (m):", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
    ttk.Entry(frame, textvariable=z0_var, width=20).grid(row=3, column=1, pady=5)
    
    ttk.Label(frame, text="Cường độ dòng điện (A):", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
    ttk.Entry(frame, textvariable=o_var, width=20).grid(row=4, column=1, pady=5)
    
    def enter(): #cho nút bấm xác nhận
        try:
            result['r'] = float(r_var.get())
            result['x0'] = float(x0_var.get())
            result['y0'] = float(y0_var.get())
            result['z0'] = float(z0_var.get())
            result['o'] = float(o_var.get())
            result['ok'] = True
            root.destroy() #đóng cửa sổ sang turtle
        except ValueError:
            error_window = tk.Toplevel()
            error_window.title("Lỗi")
            ttk.Label(error_window, text="Vui lòng nhập số hợp lệ!", 
                     font=("Arial", 12), foreground="red").pack(padx=20, pady=20)
            ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
    btn = ttk.Button(root, text="Tính toán và vẽ đồ thị", command=enter)
    btn.pack(pady=20)
    
    root.mainloop()
    return result

def biot_savart(x_point, y_point, z_point, radius, I, scale):
    #tính từ trường tại điểm (x0,y0,z0)
    total = np.array([0.0, 0.0, 0.0])
    
    for i in range(500):
        theta1 = i * 0.72 * np.pi / 180
        theta2 = (i + 1) * 0.72 * np.pi / 180

        a = 250 * np.cos(theta1)
        b = 250 * np.sin(theta1)
        c = 250 * np.cos(theta2)
        d = 250 * np.sin(theta2)

        dl = np.array([(c*scale - a*scale), (d*scale - b*scale), 0])
        vr = np.array([x_point - (c+a)*scale/2, y_point - (d+b)*scale/2, z_point - 0])

        vr_norm = np.linalg.norm(vr)
        if vr_norm > 0:
            db = I * (10**-7) * np.cross(dl, vr) / (vr_norm**3) #tính b?
            total += db
    
    return total

def draw_text_background(turtle_obj, x, y, width, height, color): #backgound cho onclick()
    turtle_obj.penup()
    turtle_obj.goto(x - width/2, y - height/2)
    turtle_obj.pendown()
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(2):
        turtle_obj.forward(width)
        turtle_obj.left(90)
        turtle_obj.forward(height)
        turtle_obj.left(90)
    turtle_obj.end_fill()
    turtle_obj.penup()

#lấy input
input_data = get_input()
#xem dict result ở trên, nếu ok = False thì thoát chương trình
if not input_data['ok']:
    exit()

r = input_data['r']
x0 = input_data['x0']
y0 = input_data['y0']
z0 = input_data['z0']
o = input_data['o']

screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.title("Mô phỏng từ trường - Click chuột để xem từ trường tại điểm đó")
screen.tracer(0)

turtle.speed(0)
turtle.hideturtle()

#text cho onclick
text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.speed(0)

#background
bg_turtle = turtle.Turtle()
bg_turtle.hideturtle()
bg_turtle.speed(0)

#info 
info_turtle = turtle.Turtle()
info_turtle.hideturtle()
info_turtle.speed(0)

#trục oxy
turtle.pensize(2)
turtle.pencolor("gray")
#trục Ox
turtle.penup()
turtle.goto(-350, 0)
turtle.pendown()
turtle.goto(350, 0)
turtle.goto(340, -10)
turtle.goto(350, 0)
turtle.goto(340, 10)
turtle.penup()
turtle.goto(360, -15)
turtle.write("X", font=("Arial", 14, "bold"))

#trục Oy
turtle.penup()
turtle.goto(0, -350)
turtle.pendown()
turtle.setheading(90)
turtle.goto(0, 350)
turtle.goto(-10, 340)
turtle.goto(0, 350)
turtle.goto(10, 340)
turtle.penup()
turtle.goto(10, 360)
turtle.write("Y", font=("Arial", 14, "bold"))

#vạch chia số
turtle.pensize(1)
scale = r / 250

#chia trục Ox
for i in range(-3, 4):
    if i != 0:
        pos = i * 100
        turtle.penup()
        turtle.goto(pos, -5)
        turtle.pendown()
        turtle.goto(pos, 5)
        turtle.penup()
        turtle.goto(pos, -20)
        value = round(pos * scale, 2)
        turtle.write(f"{value}", align="center", font=("Arial", 8, "normal"))

#chia trục Oy
for i in range(-3, 4):
    if i != 0:
        pos = i * 100
        turtle.penup()
        turtle.goto(-5, pos)
        turtle.pendown()
        turtle.goto(5, pos)
        turtle.penup()
        turtle.goto(-35, pos - 5)
        value = round(pos * scale, 2)
        turtle.write(f"{value}", align="right", font=("Arial", 8, "normal"))

#vẽ lưới toạ độ (mấy cái vuông vuông á)
turtle.pencolor("lightgray")
turtle.pensize(0.5)
for i in range(-3, 4):
    if i != 0:
        #trục Oy
        turtle.penup()
        turtle.goto(i * 100, -300)
        turtle.pendown()
        turtle.goto(i * 100, 300)
        #trục Ox
        turtle.penup()
        turtle.goto(-300, i * 100)
        turtle.pendown()
        turtle.goto(300, i * 100)

screen.update()

#vòng dây
turtle.pensize(2)
turtle.goto(250, 0)
turtle.setheading(90)
turtle.pencolor("black")
turtle.pendown()

for i in range(500):
    turtle.forward(np.pi)
    turtle.left(0.72)

screen.update()

#mũi tên chỉ chiều dòng điện
turtle.penup()
turtle.goto(250, 0)
turtle.pendown()
turtle.pencolor("red")
turtle.pensize(3)
turtle.setheading(90)
turtle.forward(30)
turtle.left(150)
turtle.forward(10)
turtle.backward(10)
turtle.right(300)
turtle.forward(10)
turtle.penup()
turtle.goto(260, 35)
turtle.pencolor("red")
turtle.write("I", font=("Arial", 12, "bold"))

screen.update()

#điểm cần tính (x0,y0)
turtle.penup()
turtle.goto(x0/scale, y0/scale)
turtle.dot(10, "red")

screen.update()

#tính từ trường tại điểm (x0,y0) |B|
turtle.goto(250, 0)
turtle.setheading(90)
(a, b, c, d) = (0, 0, 0, 0)
total = np.array([0.0, 0.0, 0.0])
turtle.pencolor("blue")
turtle.pendown()

for i in range(500):
    (a, b) = turtle.pos()
    turtle.forward(math.pi)
    (c, d) = turtle.pos()

    db = biot_savart(x0, y0, z0, r, o, scale)
    total = db
    
    if db[2] >= 0:
        turtle.pencolor("blue")
    else:
        turtle.pencolor("red")
    
    turtle.left(0.72)
    
    # if i % 50 == 0:
    #     screen.update()
    screen.update()

screen.update()

#turtle 
turtle.penup()
turtle.goto(0, -380)
turtle.pencolor("black")
b_magnitude = np.linalg.norm(total)

b_mag_str = format_scientific(b_magnitude)
bx_str = format_scientific(total[0])
by_str = format_scientific(total[1])
bz_str = format_scientific(total[2])

turtle.write(f"Kết quả tại điểm ({x0}, {y0}, {z0}): |B| = {b_mag_str} T\n Bán kính vòng dây: {r} m", 
            align="center", font=("Arial", 11, "bold"))

screen.update()
screen.tracer(1)

#info
info_box_x = 240
info_box_y = 250
info_box_width = 120
info_box_height = 90

#background info
info_turtle.penup()
info_turtle.goto(info_box_x - info_box_width/2, info_box_y - info_box_height/2)
info_turtle.pendown()
info_turtle.fillcolor("#E3F2FD")
info_turtle.begin_fill()
for i in range(2):
    info_turtle.forward(info_box_width)
    info_turtle.left(90)
    info_turtle.forward(info_box_height)
    info_turtle.left(90)
info_turtle.end_fill()

info_turtle.penup()
info_turtle.goto(info_box_x - info_box_width/2, info_box_y - info_box_height/2)
info_turtle.pendown()
info_turtle.pencolor("#1976D2")
info_turtle.pensize(2)
for i in range(2):
    info_turtle.forward(info_box_width)
    info_turtle.left(90)
    info_turtle.forward(info_box_height)
    info_turtle.left(90)

info_turtle.penup()
info_turtle.goto(info_box_x, info_box_y + 30)
info_turtle.pencolor("#1565C0")
info_turtle.write("THÔNG TIN", align="center", font=("Arial", 9, "bold"))

info_turtle.goto(info_box_x, info_box_y + 10)
info_turtle.pencolor("black")
info_turtle.write(f"R = {r} m", align="center", font=("Arial", 8, "normal"))

info_turtle.goto(info_box_x, info_box_y - 5)
info_turtle.write(f"I = {o} A", align="center", font=("Arial", 8, "normal"))

info_turtle.goto(info_box_x, info_box_y - 20)
info_turtle.write(f"Điểm: ({x0}, {y0}, {z0})", align="center", font=("Arial", 7, "normal"))

info_turtle.goto(info_box_x, info_box_y - 35)
info_turtle.write(f"|B| = {b_mag_str} T", align="center", font=("Arial", 7, "normal"))

screen.update()
screen.tracer(1)

#click để xem từ trường tại điểm (x,y) bất kỳ
def on_click(x, y):
    x_real = x * scale
    y_real = y * scale
    
    delta_l = math.sqrt(x_real**2 + y_real**2)

    if delta_l <= r:
        text_turtle.clear()
        bg_turtle.clear()

        text_turtle.penup()
        text_turtle.goto(x, y)
        text_turtle.dot(7, "green")

        b_field = biot_savart(x_real, y_real, r, o, scale)
        b_mag = np.linalg.norm(b_field)
        b_mag_str = format_scientific(b_mag) #định dạng 10^x kiểu vn

        if delta_l < 0.8 * r:
            text_y_offset = 15
            bg_y_offset = 30
        else:
            text_y_offset = -25
            bg_y_offset = -10
        
        bg_turtle.penup()
        bg_turtle.goto(x, y + bg_y_offset)
        bg_width = 140
        bg_height = 35
        draw_text_background(bg_turtle, x, y + bg_y_offset, bg_width, bg_height, "#E8F5E9")
        
        #(x, y)
        text_turtle.goto(x, y + text_y_offset)
        text_turtle.pencolor("darkgreen")
        text_turtle.write(f"({x_real:.3f}, {y_real:.3f})\n|B| = {b_mag_str} T", 
                         align="center", font=("Arial", 9, "bold"))
        
        screen.update()

screen.onclick(on_click)
################################## turtle xong ##################################
#matplotlib
theta = np.linspace(0, 2*np.pi, 200) #200 điểm bằng nhau từ 0 đến 2pi
x = r * np.cos(theta)
y = r * np.sin(theta)
z = np.zeros_like(theta) #z=0 vì vòng dây nằm trên mặt phẳng xy

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, label='Vòng dây', linewidth=2, color='black')

#mũi tên chỉ I
goc_mt = [30, 120, 210, 300]
for i in goc_mt:
    goc1 = i * np.pi / 180

    x_1 = r * np.cos(goc1)
    y_1 = r * np.sin(goc1)

    goc_mt_tt = goc1 + np.pi/2
    l_mt = r * 0.15
    dx = l_mt * np.cos(goc_mt_tt)
    dy = l_mt * np.sin(goc_mt_tt)

    ax.quiver(x_1, y_1, 0,
              dx, dy, 0,
              color='red', arrow_length_ratio=0.3, linewidth=2.5) #vẽ mũi tên

#bỏ comment nếu muốn ghi chú I trên đồ thị
# ax.text(r * 1.1, 0, 0, 'I', fontsize=14, color='red', fontweight='bold')

#(xo, yo, z0) điểm cần tính
ax.scatter([x0], [y0], [z0], color='red', s=100, label=f'Điểm tính ({x0}, {y0}, {z0})')

#vector từ trường B
if b_magnitude > 0:
    b_scaled = total * (r * 0.3 / b_magnitude) #phóng to vector B cho dễ nhìn
else:
    b_scaled = total
#mũi tên B
ax.quiver(x0, y0, z0,
          b_scaled[0], b_scaled[1], b_scaled[2],
          color='blue', arrow_length_ratio=0.2, linewidth=3, label='Véc tơ B')

ax.set_xlabel('X (m)', fontsize=12)
ax.set_ylabel('Y (m)', fontsize=12)
ax.set_zlabel('Z (m)', fontsize=12)
ax.set_title(f'Từ trường tại điểm ({x0}, {y0}, {z0})\n|B| = {b_mag_str} T\n Bán kính vòng dây: {r} m', fontsize=14)
ax.legend()

max_range = r * 1.2
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range/2, max_range/2])

#kết quả dưới đồ thị
textstr = f'Tọa độ: ({x0}, {y0}, {z0})\n|B| = {b_mag_str} T\nChiều I: ngược chiều kim đồng hồ'
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text2D(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.show()
turtle.done()
#done
