from gpio_driver import GPIODriver


def main():
    driver = GPIODriver()
    driver.clear()
    try:
        while True:
            driver[int(input('Enter pin to enable: '))] = True
            driver[int(input('Enter pin to disable: '))] = False
    except KeyboardInterrupt:
        driver.stop()


if __name__ == '__main__':
    main()
