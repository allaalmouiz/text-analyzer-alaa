def read_text_file(filepath):
    # Starting the terminal
    print("")
    print("Starting to read the file...")
    print(f"Reading file: {filepath}")
    print("==========="*10)
    print("")

    #Handling file reading with error management
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            return content

    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied.")
    except UnicodeDecodeError:
        print("Error: Encoding issue.")
    except OSError as e:
        print(f"Error: OS error: {e}")


    


def main():
    #Reading the file and printing a snippet
    file = read_text_file("sample_text.txt")
    print(file[:200])  # print first 200 characters


if __name__ == "__main__":
    main()
