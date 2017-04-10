import subprocess

if __name__=='__main__':
    with open('sudokus_start.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    i=1
    for board in content:
        print i
        subprocess.call(["python","driver.py",board])
        i+=1
        print