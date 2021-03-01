import tkinter as tk
import Login as log
import OCR as ocr

window = tk.Tk()
window.title('教务查询For正方System')
window.geometry('670x400')
typing1 = tk.Entry(window, font=('微软雅黑', 14))
typing2 = tk.Entry(window, show="*", font=('微软雅黑', 14))
typing3 = tk.Entry(window, font=('微软雅黑', 14), width=5)
typing4 = tk.Entry(window, font=('微软雅黑', 14), width=4)
typing5 = tk.Entry(window, font=('微软雅黑', 14))
text1 = tk.Label(window, text="教务账号：", font=('微软雅黑', 14))
text2 = tk.Label(window, text="教务密码：", font=('微软雅黑', 14))
text3 = tk.Label(window, text="查询年份：", font=('微软雅黑', 14))
text4 = tk.Label(window, text="查询学期：", font=('微软雅黑', 14))
text5 = tk.Label(window, text="教务验证码：", font=('微软雅黑', 14))
text6 = tk.Label(window, text="信息如下:", font=('微软雅黑', 14))

text1.place(x=50, y=20)
typing1.place(x=150, y=17)
text2.place(x=50, y=50)
typing2.place(x=150, y=47)
text3.place(x=50, y=80)
typing3.place(x=150, y=77)
text4.place(x=200, y=80)
typing4.place(x=279, y=77)
text5.place(x=50, y=110)
typing5.place(x=150, y=107)
text6.place(x=50, y=200)
text = tk.Text(window, width=85, height=10)
text.place(x=30, y=220)


def check():
    id = typing1.get()
    year = int(typing3.get())
    semester = typing4.get()
    text.delete(0.0, tk.END)
    global session
    session = log.get_check_code()
    global image
    image = tk.PhotoImage(file="check.jpg")
    imgLabel = tk.Label(window, image=image)
    imgLabel.place(x=350, y=50)
    # checkcode = ocr.get_check() # 使用ocr识别验证码并填入验证框
    # typing5.delete(0, tk.END)
    # typing5.insert("insert", checkcode[0])
    if bool_check1.get() and bool_check2.get():
        text.insert("insert", "输入的账号为：" + id + "\n" +
                    "查询的年份为：" + str(year) + "-" + str(year + 1) + " 学期为：" + semester + "\n" +
                    "全部查询\n" +
                    "OCR自动识别的验证码为：" + "如有误请手动输入,如无误请点击查询按钮。")
    elif bool_check1.get():
        text.insert("insert", "输入的账号为：" + id + "\n" +
                    "查询的年份为：" + str(year) + "-" + str(year + 1) + " 学期为：" + semester + "\n" +
                    "查询成绩\n" +
                    "OCR自动识别的验证码为：" + "如有误请手动输入,如无误请点击查询按钮。")
    elif bool_check2.get():
        text.insert("insert", "输入的账号为：" + id + "\n" +
                    "查询的年份为：" + str(year) + "-" + str(year + 1) + " 学期为：" + semester + "\n" +
                    "查询课表\n" +
                    "OCR自动识别的验证码为：" + "如有误请手动输入,如无误请点击查询按钮。")
    else:
        text.insert("insert", "请选择查询项目\n")


def get_score(cookies, year, semester):
    data = log.get_score(cookies, int(year), int(semester))
    text.insert("insert",
                "学年：    " + "学期：" +
                "课程号：" + "课程名称：" +
                "	原始课程性质：" + "互认课程性质:" +
                "课程归属:" + "学分:" + "绩点："
                + "分数:" + "开课单位" + "\n")
    count = 0
    for i in range(len(data)):
        if count != 14:
            text.insert("insert", data[i] + " ")
            count += 1
        else:
            text.insert("insert", data[i] + "\n")
            count = 0


def get_table(cookies):
    table = log.into_curriculum(cookies)
    text.insert("insert", "课表内容：\n")
    for st in table:
        text.insert("insert", st.getText() + "\n")


def post():
    id = typing1.get()
    passwords = typing2.get()
    checkcode = typing5.get()
    year = typing3.get()
    semester = typing4.get()
    cookies = log.login(session, id, passwords, checkcode)
    text.delete(0.0, tk.END)
    if bool_check1.get() and bool_check2.get():
        get_score(cookies, year, semester)
        get_table(cookies)
    elif bool_check1.get():
        get_score(cookies, year, semester)
    elif bool_check2.get():
        get_table(cookies)
    else:
        text.insert("insert", "没选不能查询啦\n")


bool_check1 = tk.BooleanVar()
bool_check2 = tk.BooleanVar()
check_case1 = tk.Checkbutton(window, text='成绩查询', variable=bool_check1)
check_case2 = tk.Checkbutton(window, text='课表查询', variable=bool_check2)
check_case1.place(x=200, y=140)
check_case2.place(x=280, y=140)
button1 = tk.Button(window, text="确认", width=6, height=2, command=check).place(x=300, y=170)
button2 = tk.Button(window, text="查询", width=6, height=2, command=post).place(x=380, y=170)

window.mainloop()
