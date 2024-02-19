import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import socket

# Tạo cửa sổ chính
root = tk.Tk()
root.title("App Window")

# Tạo ô edit field
Url_field = tk.Entry(root, width=100) # widget Entry cho phép người dùng nhập vào từ bàn phím: tham số thứ nhất là cửa sổ cha,
                                   # tham số thứ 2 là các option để cấu hình widget trong đó có width (độ rộng)
Url_field.pack(padx=10, pady=10)      # pack dùng để đưa widget vào cửa số và đặt vị trí của nó dựa trên mối quan hệ với các widget khác
                                   # padx, pady là khoảng cách với khung cửa sổ và với các widget khác


# Tạo field kết quả
# Text là một widget trong thư viện Tkinter của Python, được sử dụng để hiển thị hoặc nhập dữ liệu dưới dạng văn bản có thể chỉnh sửa
display_field = tk.Text(root, width=100)
display_field.pack(padx=10, pady=10)

def scan():
    url = Url_field.get()
    try:
        Space = "***************************************************************************************************\n***************************************************************************************************\n"
        responce = requests.get(url)
        content = responce.text
        soup = BeautifulSoup(content, 'html.parser')

        # Phần I: hiển thị nội dung của Dictionary List
        display_field.insert(tk.END, "INFORMATION DISCLOSURE DICTIONARY LIST" + "\n")
        links = soup.find_all("a")
        # Thuộc tính find_all: tìm tất cả các vị trí của một mẫu (pattern) trong một văn bản Text
        # Tại đây tìm tất cả các
        for link in links:
            href = link.get('href')
            if href.endswith('/'):
                display_field.insert(tk.END, 'Directory: ' + href + "\n")
            if 'user' in href:   
                display_field.insert(tk.END, 'User account page: ' + href + "\n") 
        display_field.insert(tk.END, Space)

        # Phần II: Hiển thị nội dung comment code của nhà phát triển
        display_field.insert(tk.END, "INFORMATION DISCLOSURE COMMENT CODE" + "\n")
            # re.findall được sử dụng để tìm tất cả các chuỗi con trong para phù hợp với biểu thức chính quy r"<!--(.*?)-->".
            # <!-- và --> là cặp ký tự đánh dấu comment trong HTML.
            # .*? được sử dụng để tìm bất kỳ ký tự nào (trừ ký tự xuống dòng) trong cặp dấu <!-- và -->, Ký tự ? sử dụng để đảm bảo rằng biểu 
            # thức chính quy sẽ tìm kiếm chuỗi con ngắn nhất có thể, thay vì chuỗi con dài nhất có thể
        comments = re.findall(r"<!--(.*?)-->", content)
        for comment in comments:
            display_field.insert(tk.END, f"Deverlop comment: {comment}" + "\n")
        display_field.insert(tk.END, Space)

        # Phần III: tìm tất cả các thông báo lỗi trong một đoạn văn bản
        display_field.insert(tk.END, "INFORMATION DISCLOSURE ERROR MESSAGE" + "\n")
        # tìm tất cả các chuỗi con trong para phù hợp với biểu thức chính quy r'(?:Exception|Error)(.*?)(?:\n|$)'.
        # Exception|Error là một phần của biểu thức chính quy, nó tìm kiếm bất kỳ từ "Exception" hoặc "Error" nào.
        # (.*?) được sử dụng để tìm bất kỳ ký tự nào trừ ký tự xuống dòng và lưu trữ nó vào một nhóm không đánh số.
        # (?:\n|$) là một phần của biểu thức chính quy, nó tìm kiếm bất kỳ ký tự xuống dòng nào hoặc kết thúc chuỗi. Dấu ?: ở đây 
        # chỉ ra rằng đây là một nhóm không lưu trữ kết quả.
        errors1 = re.findall(r'(?:Exception|Error)(.*?)(?:\n|$)', content)

        # tìm tất cả các chuỗi con trong para phù hợp với biểu thức chính quy r'<div class="error">(.*?)</div>'.
        # <div class="error"> và </div> là các thẻ HTML đánh dấu thông báo lỗi trong một trang web.
        # (.*?) được sử dụng để tìm bất kỳ ký tự nào và lưu trữ nó vào một nhóm không đánh số.
        errors2 = re.findall(r'<div class="error">(.*?)</div>', content)

        #`(?s)`: là một flag để cho phép dấu chấm (".") khớp với cả ký tự xuống dòng ("\n") trong chuỗi.
        # `(?<=\n)`: là một positive lookbehind, đảm bảo rằng chuỗi phù hợp phải có một ký tự xuống dòng ("\n") ở phía trước.
        # `[^a-z]*`: là một ký tự bất kỳ không phải ký tự chữ cái viết thường, có thể có hoặc không xuất hiện.
        # `(error|exception)`: là một group, khớp với chuỗi "error" hoặc "exception".
        # `[^a-z]*`: là một ký tự bất kỳ không phải ký tự chữ cái viết thường, có thể có hoặc không xuất hiện.
        # `:`: khớp với một dấu hai chấm (":").
        # `.+?`: là một chuỗi bất kỳ, có thể có hoặc không xuất hiện, và sẽ được khớp ngắn nhất có thể (non-greedy), đảm bảo rằng chuỗi phù hợp chỉ bao gồm phần tử từ lần xuất hiện ký tự đầu tiên đến lần xuất hiện ký tự cuối cùng của pattern.
        # `(?=\n\n|\Z)`: là một positive lookahead, đảm bảo rằng chuỗi phù hợp phải kết thúc bằng hai ký tự xuống dòng ("\n\n") hoặc kết thúc chuỗi (ký tự "\Z").
        errors3 = re.findall(r'(?s)(?<=\n)[^a-z]*(error|exception)[^a-z]*:.+?(?=\n\n|\Z)', content)

        if len(errors1) == 0 and len(errors2) == 0 and len(errors3) == 0:
            display_field.insert(tk.END, "Error Message not found" + "\n")
        else:
            display_field.insert(tk.END, f"Error Message: {errors1} + '\n'")
            display_field.insert(tk.END, f"Error Message: {errors2} + '\n'")
            display_field.insert(tk.END, f"Error Message: {errors3} + '\n'")
        
        display_field.insert(tk.END, Space)

        # Phần IV: Hiển thị debugging data
        display_field.insert(tk.END, "INFORMATION DISCLOSURE DEBUGGING DATA" + "\n")
        debugging_data = re.findall(r'<!-- DEBUGGING DATA START -->(.*?)<!-- DEBUGGING DATA END -->', content)

        if len(debugging_data) == 0:
            display_field.insert(tk.END, "Not fount debugging data" + "\n")
        else:
            display_field.insert(tk.END, f"Debugging data {debugging_data}" + "\n")
        display_field.insert(tk.END, Space)

        # Phần V: Hiển thị thông tin các backup file
        display_field.insert(tk.END, "INFORMATION DISCLOSURE DICTIONARY LIST" + "\n")
        backup_files = []

        with open("backupfile.txt", 'r') as file:  # Mở file backupfile.txt và tạo đối tượng tên file để đọc nội dụng file
            for line in file:  # Duyệt từng dòng của file
                backup = line[:-1]  # Cắt đoạn cuối cùng của dòng ở đây là '\n'
                backup_files.append(backup)  # Đưa dòng đó vào list backup_files
    
        # Duyệt từng phần tử của mảng backup_files, nối với url
        for file in backup_files:
            backup_url = url + file
            # Lấy dữ liệu từ đường link
            response = requests.get(backup_url)
            # Nếu kết quả trả về == 200 thì tiến hành tìm kiếm thông tin nhạy cảm
            if response.status_code == 200:
            # Kiểm tra xem file backup có chứa thông tin nhạy cảm hay không
                if 'password' in response.text or 'login' in response.text:
                    display_field.insert(tk.END, 'Sensitive information found in backup file: ' + backup_url + "\n")
                else:
                    display_field.insert(tk.END, 'Backup file exists but does not contain sensitive information: ' + backup_url + "\n")
            else:
                display_field.insert(tk.END, 'Backup file does not exist: ' + backup_url + "\n")
        display_field.insert(tk.END, Space)


        # Phần VI: Hiển thị kết quả kiểm tra các thư mục kiểm soát phiên bản (version control) của một URL
        display_field.insert(tk.END, "INFORMATION DISCLOSURE VERSION CONTROL" + "\n")
        # danh sách các thư mục kiểm soát phiên bản được khởi tạo với các giá trị ".git", ".svn" và "CVS"
        version_control_dirs = ['.git', '.svn', 'CVS']

        # lặp qua các phần tử của mảng nối với url để tiến hành requests
        for dir in version_control_dirs:
            target_url = url + '/' + dir
            response = requests.get(target_url)
            
            # Nếu status_code trả về == 200 thì trả về kết quả và content thu thập được
            if response.status_code == 200:
                display_field.insert(tk.END, f'FOUND {dir} DICTIONARY AT {target_url}' + "\n")
        display_field.insert(tk.END, Space)
        
        # Phần VII: Hiển thị một số thông tin thêm về miền domain
        display_field.insert(tk.END, "INFORMATION DISCLOSURE IP AND FULL DOMAIN" + "\n")
        # hàm urlparse trong module urllib.parse để phân tích URL được truyền vào. Kết quả phân tích được lưu trữ trong biến parsed_url
        parsed_url = urlparse(url)

        # tên miền được trích xuất từ parsed_url bằng cách loại bỏ phần "www." nếu có, và lưu trữ trong biến domain
        domain = parsed_url.netloc.replace('www.', '')
        # Gethostbyname được sử dụng để lấy địa chỉ IP tương ứng với tên miền domain, hàm nhận về 1 tham số là domain
        display_field.insert(tk.END, "gethostbyname: " + socket.gethostbyname(domain) + "\n") 
        # gethostbyname_ex() được sử dụng để lấy thông tin danh sách các địa chỉ IP tương ứng và danh sách các hostname tương ứng của domain
        display_field.insert(tk.END, "gethostbyname_ex: ")
        display_field.insert(tk.END, socket.gethostbyname_ex(domain))
        display_field.insert(tk.END, "\n")
        # getfqdn() được sử dụng để lấy tên miền đầy đủ (fully qualified domain name) tương ứng với tên miền domain
        display_field.insert(tk.END, "getfqdn: "+ socket.getfqdn(domain) + "\n")
        # getaddrinfo() được sử dụng để lấy thông tin giao thức và số cổng ứng với domain
        display_field.insert(tk.END, "getaddrinfor: ")
        display_field.insert(tk.END,socket.getaddrinfo(domain, None, 0, socket.SOCK_STREAM))
        display_field.insert(tk.END, "\n")
        display_field.insert(tk.END, Space)

        # Phần VIII: Hiển thị thông tin về một số danh sách các đường dẫn và thư mục thường được sử dụng để truy cập vào trang quản trị (admin) của một trang web
        display_field.insert(tk.END, "INFORMATION DISCLOSURE PATHS AND DIRECTORIES USED TO ACCESS THE ADMIN PAGE OF WEBSITE" + "\n")
        login_urls = []

        with open("login_url.txt", 'r') as file:  # Mở file login_url.txt và tạo đối tượng tên file để đọc nội dụng file
            for line in file:  # Duyệt từng dòng của file
                login = line[:-1]  # Cắt đoạn cuối cùng của dòng ở đây là '\n'
                login_urls.append(login)  # Đưa dòng đó vào list login_urls

        # lặp qua tất cả các URL đăng nhập có thể và kiểm tra xem chúng có trả về mã trạng thái 200 không
        for url_part in login_urls:
            # xây dựng URL đầy đủ bằng cách kết hợp tên miền và URL có thể dự đoán
            full_url_part = 'http://' + domain + url_part
            # thực hiện get request
            response = requests.get(full_url_part)
            # kiểm tra mã trạng thái
            if response.status_code == 200:
                display_field.insert(tk.END, 'Login page found at:'+ full_url_part + "\n")
        display_field.insert(tk.END, Space)


    # Thuộc tính insert dùng để chèn nội dung vào một widget
    # tham số thứ nhất có dạng line.column: vị trí bắt đầu chèn
    # Tham số thứ hai là nội dung cần chèn vào widget
        #entry2.insert("1.0", soup)
    except requests.exceptions.HTTPError as e:
        print('HTTP error occurred:', e)
    except requests.exceptions.RequestException as e:
        print('Other error occurred:', e)
    # Hiển thị nội dung ở ô edit field kết quả

# Tạo button scan
button = tk.Button(root, text="Scan", command=scan)
button.pack(padx=10, pady=10)

# Khởi chạy app
root.mainloop()