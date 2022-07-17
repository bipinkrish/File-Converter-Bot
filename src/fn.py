import typing
import os


def give_name(data: typing.Tuple):
    name = ""
    for i in data:
        name += ", " + str(i)
    return name[1:]


# videoinfo
def videoinfo(file, telegraph):
    cmd = f'ffprobe -v quiet -show_format -show_streams "{file}" > "{file}.txt"'
    print(cmd)
    os.system(cmd)
    with open(f"{file}.txt", "rb") as infile:
        info = str(infile.read())

    os.remove(f"{file}.txt")

    stream = info[10:].split("[/STREAM]")
    formats = str(stream[1])[10:-12]
    stream = stream[0]

    info = formats + stream[2:]
    info = info.replace("=", "     =        ")
    info = info.replace("\\n", "<br>")
    info = info.replace(":", "   ")
    info = info.replace("./", "")

    file = file.split("downloads")[-1]
    if file[0] == "/":
        file = file[1:]
    print(file)
    response = telegraph.create_page(
        f'{file.replace("./", "")}', html_content=f"<p>{info}</p>"
    )
    return response["url"]


# new filename
def update_file(input_file, new):
    input_file = input_file.split(".")
    input_file[-1] = new
    output = ""
    for ele in input_file:
        output = output + "." + ele
    output = output[1:]
    print(f"New Filename will be")
    print(output)
    return output


# calibre command
def calibre_command(cmd, output):
    cmd = f'ebook-convert "{cmd}" "{output}" --enable-heuristics'
    print("Command to be Executed is")
    print(cmd)
    return cmd
