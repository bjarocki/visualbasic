import server.server as Server
import sys

if __name__ == '__main__':
    try:
        s = Server.Server()
        s.run()
    except:
        sys.exit(1)
