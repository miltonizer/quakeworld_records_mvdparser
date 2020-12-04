from demo_parser import DemoParser
import sys


def main():
    if len(sys.argv) != 2:
        print('Wrong number of parameters given')
    else:
        try:
            demo_handle = open(sys.argv[1], "rb")
            demo_parser = DemoParser()

            demo_parser.read(demo_handle)
            demo_handle.close()

        except IOError:
            print("File " + sys.argv[1] + " could not be read")
        #except:
        #    print("An unexpected error happened")


main()
