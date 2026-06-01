#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
📅 2026中国+国际日历 - 强制对齐版
"""

import calendar
from datetime import datetime, date
import os

class Calendar2026:
    def __init__(self):
        self.year = 2026
        self.month = datetime.now().month
        self.today = datetime.now().date()
        
        # 颜色
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.CYAN = '\033[96m'
        self.PURPLE = '\033[95m'
        self.WHITE = '\033[97m'
        self.GRAY = '\033[90m'
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
        
        # ===== 2026年节日数据 =====
        # 国务院法定节假日
        self.public_holidays = {
            '2026-01-01': '元旦',
            '2026-02-17': '春节',
            '2026-04-05': '清明',
            '2026-05-01': '劳动节',
            '2026-06-19': '端午节',
            '2026-09-25': '中秋节',
            '2026-10-01': '国庆节',
        }
        
        # 农历传统节日
        self.lunar_festivals = {
            '2026-02-17': '春节',
            '2026-03-03': '元宵节',
            '2026-04-12': '寒食节',
            '2026-06-19': '端午节',
            '2026-08-28': '七夕节',
            '2026-09-15': '中元节',
            '2026-09-25': '中秋节',
            '2026-10-08': '重阳节',
            '2026-12-21': '冬至',
        }
        
        # 24节气
        self.solar_terms = {
            '2026-01-05': '小寒', '2026-01-20': '大寒',
            '2026-02-03': '立春', '2026-02-18': '雨水',
            '2026-03-05': '惊蛰', '2026-03-20': '春分',
            '2026-04-05': '清明', '2026-04-20': '谷雨',
            '2026-05-05': '立夏', '2026-05-21': '小满',
            '2026-06-05': '芒种', '2026-06-21': '夏至',
            '2026-07-07': '小暑', '2026-07-22': '大暑',
            '2026-08-07': '立秋', '2026-08-23': '处暑',
            '2026-09-07': '白露', '2026-09-22': '秋分',
            '2026-10-08': '寒露', '2026-10-23': '霜降',
            '2026-11-07': '立冬', '2026-11-22': '小雪',
            '2026-12-07': '大雪', '2026-12-21': '冬至',
        }
        
        # 国际节日
        self.international_days = {
            '01-01': '元旦',
            '02-14': '情人节',
            '03-08': '妇女节',
            '03-20': '国际幸福日',
            '03-21': '世界森林日',
            '03-22': '世界水日',
            '03-23': '世界气象日',
            '04-01': '愚人节',
            '04-07': '世界卫生日',
            '04-22': '地球日',
            '04-23': '世界读书日',
            '05-01': '劳动节',
            '05-04': '青年节',
            '05-08': '世界红十字日',
            '05-12': '护士节',
            '05-15': '国际家庭日',
            '05-31': '世界无烟日',
            '06-01': '儿童节',
            '06-05': '世界环境日',
            '06-06': '全国爱眼日',
            '06-26': '国际禁毒日',
            '07-01': '建党节',
            '07-11': '世界人口日',
            '08-01': '建军节',
            '09-08': '国际扫盲日',
            '09-10': '教师节',
            '09-16': '国际臭氧层保护日',
            '09-21': '国际和平日',
            '09-27': '世界旅游日',
            '10-01': '国庆节',
            '10-04': '世界动物日',
            '10-09': '世界邮政日',
            '10-10': '辛亥革命纪念日',
            '10-14': '世界标准日',
            '10-16': '世界粮食日',
            '10-24': '联合国日',
            '10-31': '万圣节',
            '11-08': '中国记者节',
            '11-09': '全国消防日',
            '11-11': '光棍节',
            '11-17': '国际大学生节',
            '12-01': '世界艾滋病日',
            '12-03': '国际残疾人日',
            '12-05': '国际志愿者日',
            '12-09': '世界足球日',
            '12-10': '世界人权日',
            '12-20': '澳门回归纪念日',
            '12-24': '平安夜',
            '12-25': '圣诞节',
            '12-26': '毛泽东诞辰',
        }
        
    def get_festival(self, date_obj):
        """获取节日（优先显示最重要的）"""
        date_str = date_obj.strftime('%Y-%m-%d')
        month_day = date_obj.strftime('%m-%d')
        
        # 优先级：法定 > 农历 > 节气 > 国际
        if date_str in self.public_holidays:
            return self.public_holidays[date_str]
        if date_str in self.lunar_festivals:
            return self.lunar_festivals[date_str]
        if date_str in self.solar_terms:
            return self.solar_terms[date_str]
        if month_day in self.international_days:
            return self.international_days[month_day]
        return None
    
    def clear_screen(self):
        os.system('clear')
    
    def show_calendar(self):
        """显示日历（强制对齐版）"""
        self.clear_screen()
        
        # 标题
        print(f"{self.GRAY}════════════════════════════════════════{self.RESET}")
        print(f"{self.BOLD}{self.YELLOW}📅 2026年{self.month}月 中国日历{self.RESET}".center(40))
        print(f"{self.GRAY}════════════════════════════════════════{self.RESET}")
        
        # 星期表头（每个占4字符）
        weekdays = [' 一 ', ' 二 ', ' 三 ', ' 四 ', ' 五 ', ' 六 ', ' 日 ']
        header = ""
        for i, w in enumerate(weekdays):
            if i >= 5:
                header += f"{self.RED}{w}{self.RESET}"
            else:
                header += f"{self.CYAN}{w}{self.RESET}"
        print(header)
        
        # 获取日历
        cal = calendar.monthcalendar(2026, self.month)
        
        # 显示日历（每个日期固定占4字符）
        for week in cal:
            line = ""
            for day in week:
                if day == 0:
                    line += "    "  # 4个空格
                else:
                    current_date = date(2026, self.month, day)
                    festival = self.get_festival(current_date)
                    
                    # 每个日期固定占4字符：数字占2，标记占1，空格占1
                    if current_date == self.today:
                        # 今天（绿色）
                        line += f"{self.GREEN}{day:2d}✨{self.RESET} "
                    elif festival:
                        if festival in ['春节', '元旦', '国庆节', '中秋节']:
                            # 重大节日用红色★
                            line += f"{self.RED}{day:2d}★{self.RESET} "
                        else:
                            # 普通节日用黄色*
                            line += f"{self.YELLOW}{day:2d}*{self.RESET} "
                    elif current_date.weekday() >= 5:
                        # 周末（红色）
                        line += f"{self.RED}{day:2d} {self.RESET} "
                    else:
                        # 平日（白色）
                        line += f"{self.WHITE}{day:2d} {self.RESET} "
            print(line)
        
        print(f"{self.GRAY}────────────────────────────────────────{self.RESET}")
        
        # 今日信息
        today_festival = self.get_festival(self.today)
        weekdays_cn = ['一', '二', '三', '四', '五', '六', '日']
        weekday = weekdays_cn[self.today.weekday()]
        
        print(f"{self.BLUE}📌 今日:{self.RESET} 2026-{self.month:02d}-{self.today.day:02d} 星期{weekday}")
        if today_festival:
            print(f"    {self.YELLOW}{today_festival}{self.RESET}")
        
        # 本月节日列表（每行4个）
        festivals = []
        for day in range(1, 32):
            try:
                d = date(2026, self.month, day)
                if name := self.get_festival(d):
                    festivals.append((day, name))
            except ValueError:
                break
        
        if festivals:
            print(f"{self.YELLOW}📅 本月节日:{self.RESET}")
            for i in range(0, len(festivals), 4):
                line = "  "
                for j in range(4):
                    if i + j < len(festivals):
                        day, name = festivals[i + j]
                        # 节日名称太长时截断
                        if len(name) > 4:
                            name = name[:4]
                        line += f"{day:2}日:{name}  "
                print(line)
        
        # 图例
        print(f"\n{self.GREEN}✨今天{self.RESET}  {self.RED}★重大{self.RESET}  {self.YELLOW}*节日{self.RESET}  {self.RED}周末{self.RESET}  {self.WHITE}平日{self.RESET}")
        
        # 操作提示
        print()
        print(f"{self.GREEN}[n]{self.RESET}下月 {self.YELLOW}[p]{self.RESET}上月 {self.BLUE}[t]{self.RESET}今天 {self.RED}[q]{self.RESET}退出")
        print(f"{self.GRAY}────────────────────────────────────────{self.RESET}")
    
    def run(self):
        """主程序"""
        while True:
            self.show_calendar()
            
            cmd = input(f"{self.GREEN}❯ {self.RESET}").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'n':
                self.month += 1
                if self.month > 12:
                    self.month = 1
            elif cmd == 'p':
                self.month -= 1
                if self.month < 1:
                    self.month = 12
            elif cmd == 't':
                self.month = datetime.now().month
                self.today = datetime.now().date()
        
        self.clear_screen()
        print(f"\n{self.YELLOW}👋 再见！{self.RESET}\n")

if __name__ == "__main__":
    cal = Calendar2026()
    cal.run()
