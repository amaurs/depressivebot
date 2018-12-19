from depressivebot import do_action

def main():
    with open("robot.txt") as f:
         do_action(f.read())

if __name__ == '__main__':
    main()