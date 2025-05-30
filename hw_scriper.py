from playwright.sync_api import sync_playwright
import tkinter as tk
import threading
from datetime import datetime, timedelta
import queue
import time
url_of_scupibb = "https://pibb.scu.edu.cn/"
class AppState:
    def __init__(self):
        self.running = True
        self.assignments = []
        self.queue = queue.Queue()
def usr_ipt():
    username = input("请输入账号：")
    password = input("请输入密码：")
    save_condition = input("是否保存密码? (y/n)")
    if save_condition.lower() == 'y':
        with open('credentials.txt', 'w') as f:
            f.write(f"{username}\n{password}")
        print("账号密码已保存，稍后你可以在同一目录中credentials.txt中修改")
    return username, password
def load_credentials():
    try:
        with open('credentials.txt', 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
        return username, password
    except FileNotFoundError:
        return None, None
def analyze_assignments(page):
    assignments = []
    try:
        assignment_elements = page.locator('li[style*="margin-bottom: 15px;"]').all()
        for item in assignment_elements:
            try:
                title = item.locator('strong').text_content()
                a=item.locator('a')
                subject = a.text_content()
                due_date_div = item.locator('div:has-text("Due:")')
                due_date_str = due_date_div.text_content().replace('Due:', '').strip()
                try:
                    due_date = datetime.strptime(due_date_str, "%B %d, %Y at %I:%M %p")
                except ValueError:
                    due_date = datetime.strptime(due_date_str, "%b %d, %Y at %I:%M %p")
                current_time = datetime.now()
                delta = due_date - current_time
                if delta.total_seconds() > 0:
                    days = delta.days
                    seconds = delta.seconds
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    seconds = seconds % 60
                    countdown_parts = []
                    if days > 0:
                        countdown_parts.append(f"{days}天")
                    if hours > 0:
                        countdown_parts.append(f"{hours}小时")
                    if minutes > 0:
                        countdown_parts.append(f"{minutes}分钟")
                    countdown = " ".join(countdown_parts)
                else:
                    countdown = "已过期"
                assignments.append({
                    'title': title,
                    'subject': subject,
                    'due_date': due_date_str,
                    'countdown': countdown,
                    'due_datetime': due_date
                })
            except Exception as e:
                print(f"提取单个作业信息失败: {e}")
                continue
        assignments.sort(key=lambda x: x['due_datetime'])
        return assignments
    except Exception as e:
        print(f"提取作业列表失败: {e}")
        return []
def create_gui(state):
    root = tk.Tk()
    root.title("📅 你在SCUPI最近的ddl")
    root.attributes('-topmost', True)
    root.configure(bg="#f4ffb0")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 550
    x_position = screen_width - window_width - 20
    y_position = 20
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    title_label = tk.Label(
        root,
        text="📅 你在SCUPI最近的ddl",
        font=('Microsoft YaHei UI', 14, 'bold'),
        bg="#f4ffb0",
        fg="#9ec100"
    )
    title_label.pack(pady=10)
    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    text_widget = tk.Text(
        frame,
        wrap=tk.WORD,
        font=('Microsoft YaHei UI', 10),
        bg='white',
        fg='#333333',
        bd=1,
        relief=tk.SOLID
    )
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
    scrollbar = tk.Scrollbar(
        frame,
        orient=tk.VERTICAL,
        command=text_widget.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    def close_window():
        root.withdraw()
        root.iconify()
    close_button = tk.Button(
        root,
        text="最小化到任务栏",
        command=close_window,
        font=('Microsoft YaHei UI', 10),
        bg="#4E00CC",
        fg='white',
        bd=0,
        padx=12,
        pady=20
    )
    close_button.pack(side=tk.BOTTOM, pady=5)
    text_widget.tag_config('title', font=('Microsoft YaHei UI', 10, 'bold'), foreground='#0056b3')
    text_widget.tag_config('subtitle', foreground='#666666')
    text_widget.tag_config('due_date', foreground='#555555')
    text_widget.tag_config('countdown_normal', foreground='#28a745')
    text_widget.tag_config('countdown_warning', foreground='#FF6600')
    text_widget.tag_config('countdown_urgent', foreground='#dc3545')
    text_widget.tag_config('countdown_expired', foreground='#999999')
    text_widget.tag_config('separator', foreground='#cccccc')
    text_widget.tag_config('empty', foreground='#dc3545', justify=tk.CENTER, font=('Microsoft YaHei UI', 10, 'bold'))
    def update_display():
        if not state.queue.empty():
            assignments = state.queue.get()
            state.assignments = assignments
            text_widget.delete(1.0, tk.END)
            if assignments:
                for i, assignment in enumerate(assignments, 1):
                    due_datetime = assignment['due_datetime']
                    current_time = datetime.now()
                    delta = due_datetime - current_time
                    total_hours = delta.total_seconds() / 3600
                    if total_hours < 0:
                        countdown_tag = 'countdown_expired'
                        icon = "⚠️ "
                    elif total_hours < 5:
                        countdown_tag = 'countdown_urgent'
                        icon = "🔥 "
                    elif total_hours < 24:
                        countdown_tag = 'countdown_warning'
                        icon = "⏳ "
                    else:
                        countdown_tag = 'countdown_normal'
                        icon = "📅 "
                    text_widget.insert(tk.END, f"{icon}{i}. ", ('title',))
                    text_widget.insert(tk.END, f"{assignment['title']}\n", ('title',))
                    text_widget.insert(tk.END, f"课程: {assignment['subject']}\n", ('subtitle',))
                    text_widget.insert(tk.END, "   📅 ", ('subtitle',))
                    text_widget.insert(tk.END, f"截止时间: {assignment['due_date']}\n", ('due_date',))
                    text_widget.insert(tk.END, "   ⏳ ", ('subtitle',))
                    text_widget.insert(tk.END, f"剩余时间: {assignment['countdown']}\n\n", (countdown_tag,))
                    text_widget.insert(tk.END, "─" * 50 + "\n\n", ('separator',))
            else:
                text_widget.insert(tk.END, "🔍 未找到作业信息\n", 'empty')
            text_widget.yview_moveto(0)
        if state.running:
            root.after(1000, update_display)
        else:
            root.destroy()
    update_display()
    return root
def login(state):
    try:
        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                with browser.new_context() as context:
                    page = context.new_page()
                    try:
                        page.goto(url_of_scupibb)
                        username, password = load_credentials()
                        if not username or not password:
                            username, password = usr_ipt()
                        try:
                            ok_button = page.locator('.button-1')
                            if ok_button.count() > 0 and ok_button.is_visible():
                                ok_button.click()
                        except Exception as e:
                            print(f"点击确认按钮失败: {e}")
                        page.locator('#user_id').fill(username)
                        page.locator('#password').fill(password)
                        page.keyboard.press("Enter")
                        try:
                            page.wait_for_selector('span:text("On Demand Help")', timeout=10000)
                        except Exception as e:
                            print(f"登录超时或失败: {e}")
                            return
                        try:
                            with open("pibbEnhanced.js", "r", encoding="utf-8") as f:
                                script_content = f.read()
                            page.add_script_tag(content=script_content)
                        except Exception as e:
                            print(f"注入脚本失败: {e}")
                        page.wait_for_selector('li[style*="margin-bottom: 15px;"] strong', timeout=10000)
                        while state.running:
                            try:
                                page.reload()
                                page.wait_for_selector('span:text("On Demand Help")', timeout=10000)
                                with open("pibbEnhanced.js", "r", encoding="utf-8") as f:
                                    script_content = f.read()
                                page.add_script_tag(content=script_content)
                                page.wait_for_selector('li[style*="margin-bottom: 15px;"] strong', timeout=10000)
                                assignments = analyze_assignments(page)
                                state.queue.put(assignments)
                                for _ in range(60):
                                    if not state.running:
                                        break
                                    time.sleep(1)
                            except Exception as e:
                                print(f"刷新作业信息时出错: {e}")
                                time.sleep(10)
                    finally:
                        pass
    except Exception as e:
        print(f"登录过程发生严重错误: {e}")
def main():
    state = AppState()
    gui_thread = threading.Thread(target=lambda: create_gui(state).mainloop())
    gui_thread.daemon = True
    gui_thread.start()
    login_thread = threading.Thread(target=login, args=(state,))
    login_thread.daemon = True
    login_thread.start()
    try:
        while state.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        state.running = False
        login_thread.join(timeout=5)
        print("程序已退出")
if __name__ == "__main__":
    main()
