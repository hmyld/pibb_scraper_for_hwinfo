# pibb_scraper_for_hwinfo
SCUPI 自动作业提醒工具
# 简介
这是一个基于 Python 和 Playwright 的自动化工具，用于监控四川大学匹兹堡学院（SCUPI）抽象课程平台（SCUPI BB）的作业截止时间，并通过 GUI 界面实时显示作业信息及倒计时。支持自动登录、密码保存、作业信息解析和多线程运行。其中，注入脚本部分来自作者@violetctl39，原本是那位作者写的 pibb enhancing 工具，插件写的不错可以多去支持。
# 目录
  功能特性
  环境要求
  安装步骤
  使用说明
  代码结构说明
  注意事项
  贡献与反馈

# 1.功能特性
  自动登录：支持账号密码保存与读取，避免重复输入。
  作业解析：实时抓取课程平台作业信息，解析截止时间并计算倒计时。
  GUI 界面：置顶窗口显示作业列表，按截止时间排序，不同状态（正常 / 紧急 / 过期）用颜色区分。
  多线程运行：GUI 与浏览器自动化分离，保证界面流畅。
  自动刷新：定时刷新页面获取最新作业信息（默认每分钟刷新一次）。
  
# 2.环境要求
  # Python版本：
  Python 版本：3.8+ ，原生版本3.11.11
  # 依赖库：
  playwright  # 浏览器自动化
  tkinter     # GUI界面（Python标准库，通常无需安装）
  浏览器驱动：Playwright 支持的 Chromium 内核浏览器（安装 Playwright 时会自动下载）。
  
# 3.安装步骤
  ## 1.在这里下载好py文件。
  ## 2.去https://github.com/violetctl39/pibbEnhanced下载注入脚本pibbEnhanced.js，并与上述py文件储存在同一目录下。
  ## 3.安装依赖：
   pip install playwright
   python -m playwright install chromium  # 安装Chromium驱动

# 4.使用说明
  运行代码
  根据提示输入 pibb 平台账号密码：
  请输入账号：your_username
  请输入密码：your_password
  是否保存密码? (y/n)：y  # 可选，保存后下次自动读取
  程序将自动打开 Chromium 浏览器并登录，成功后 GUI 窗口会显示作业信息。
  
# 5.后续运行
  直接执行脚本，若已保存密码则自动登录；如需修改密码，删除或修改同目录下的credentials.txt文件后重新运行即可。
  
# 6.代码结构说明
  ## 1.核心模块
    AppState类：管理程序状态（运行标志、作业列表、消息队列）。
    usr_ipt()与load_credentials()：处理用户输入和密码存储。
    analyze_assignments(page)：解析页面作业信息，计算倒计时。
    create_gui(state)：创建 GUI 界面，包含作业列表、滚动条和最小化按钮。
    login(state)：浏览器自动化流程，包括登录、注入脚本、刷新页面。
    main()：主函数，启动多线程（GUI 线程和登录线程）。
  ## 2.关键文件
    main.py：主程序入口。
    credentials.txt：保存账号密码（可选，明文存储，注意安全）。
    pibbEnhanced.js：注入脚本（核心文件，必要）。
    
# 7.注意事项
  密码安全：credentials.txt为明文存储，建议仅在个人设备使用，敏感环境请勿保存密码。
  页面兼容性：作业解析依赖页面 HTML 结构，若平台更新导致标签变化，需修改analyze_assignments函数中的选择器，需要联系作者。
  
# 8.贡献与反馈
  问题反馈：如需报告 bug 或提出建议，请在GitHub Issues提交。
  代码贡献：欢迎提交 PR 优化代码，建议先创建 Issue 讨论方案。
  支持作者：用 QQ 1454988406 联系作者，如果您能赏给作者一瓶百事可乐，作者会很开心，并有继续改进代码的动力。
  开发者：Ose Chen - SCUPI
  邮箱：1454988406@qq.com
  项目地址：GitHub [仓库链接](https://github.com/hmyld/pibb_scraper_for_hwinfo)

## 9.效果预览
![QQ_1748636026758](https://github.com/user-attachments/assets/2fa3aaa5-935b-4ef5-9d23-2b2c1b3254f3)
