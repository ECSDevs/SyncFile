def do_job(mode="stable"):
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    MY_LOGGING_CONFIG = LOGGING_CONFIG.copy()
    MY_LOGGING_CONFIG["handlers"]["default"]["class"] = "logging.FileHandler"
    MY_LOGGING_CONFIG["handlers"]["default"]["filename"] = "mcsmtWebApi.log"
    del MY_LOGGING_CONFIG["handlers"]["default"]["stream"]
    MY_LOGGING_CONFIG["handlers"]["access"]["class"] = "logging.FileHandler"
    MY_LOGGING_CONFIG["handlers"]["access"]["filename"] = "mcsmtWebApiAccess.log"
    del MY_LOGGING_CONFIG["handlers"]["access"]["stream"]
    MY_LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(levelname)s] %(message)s"
    MY_LOGGING_CONFIG["formatters"]["default"]["use_colors"] = False
    MY_LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s [%(levelname)s] %(message)s"
    MY_LOGGING_CONFIG["formatters"]["access"]["use_colors"] = False
    if mode == "stable":
        uvicorn.run("mcsmt.webApi:app", host="0.0.0.0", port=36685, log_config=MY_LOGGING_CONFIG)
    elif mode=="develop":
        uvicorn.run("mcsmt.webApi:app", host="127.0.0.1", port=36685, reload=True, log_config=MY_LOGGING_CONFIG)

if __name__ == "__main__":
    from sys import argv
    argv = argv[1::]
    kwargv  = {}
    for a in argv:
        if ":" in a:
            x = a.split(":")
            kwargv[x[0]]=':'.join(x[1::])
            argv.remove(a)
    do_job(*argv, **kwargv)