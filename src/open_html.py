import webbrowser

open_path = '../data/preprocess/edinet/etc/open_html_files.txt'

def run():
    with open(open_path,'r') as f:
        paths = f.readlines()
    for path in paths:
        print(path)
        webbrowser.open_new_tab(path.replace("\n",""))

if __name__ == '__main__':
    run()