import json

# mode select
mode = input("mode(add/rewrite): ")

# mode
if mode == "add":
    with open("config.json")as f:
        config=json.load(f)
elif mode == "rewrite":
    config=[]
else:
    print("not a valid mode")

# main program
while True:
    # continue or break
    cmd = input("want(add/end):")
    # if end
    if cmd=="end":
        # end the while
        break
    # if continue
    elif cmd=="add":
        # ask message
        conf = [input("resourcePath:"),[],input("outputPath")]
        while True:
            # continue or break
            cmdft=input("file type: continue?(yes/no):")
            # if continue
            if cmdft=="yes":
                # add filetype
                conf[1].append(input("fileType: "))
            # if end
            elif cmdft=="no":
                # end the while
                break
            # if others
            else:
                print("not a valid command.")
        # save to config
        config.append(conf)
    # others
    else:
        print("not a valid command.")

# write to config file
with open("config.json",'w')as f:
    json.dump(config,f)
