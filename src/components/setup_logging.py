import logging

logging.basicConfig(
    level=logging.DEBUG,
    # format="%(levelname)s | %(name)s | %(message)s",
    # format="[%(name)s] %(asctime)s %(funcName)s %(lineno)-3d  %(message)s"
    format="[%(asctime)s] [%(levelname)-8s] %(message)s",
    # datefmt="%Y-%m-%d %H:%M:%S",
    filename=r"E:\sys.tmp\[STASH DEV]\plugins\renamer-2\app.log",
    filemode="w",
)
