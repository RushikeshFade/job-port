def save_resume(file):
    path = "resumes/" + file.filename

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path