from window import Window

def main():
    window = Window(800, 600)
    window.redraw()
    window.wait_for_close()
    print("Program closed")
    return 0

if __name__ == "__main__":
    main()