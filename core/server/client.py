def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="give some data to be transfered to the server")
    args = parser.parse_args()
    
    while True:
         print "Sending {0}".format(args.data)
         time.sleep(3)

if __name__ == "__main__":
    main()

