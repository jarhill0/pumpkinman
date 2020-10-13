from relay_driver import RelayDriver


def main():
    driver = RelayDriver()
    driver.clear()
    try:
        while True:
            driver[int(input("Enter relay to enable: "))] = True
            driver[int(input("Enter relay to disable: "))] = False
    except KeyboardInterrupt:
        driver.stop()
    except Exception:
        driver.stop()
        raise


if __name__ == "__main__":
    main()
