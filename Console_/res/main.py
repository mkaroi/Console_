import time
import datetime
import os
import shutil
import logging
import sys
import shelve

def load():
    import time
    import datetime
    import os
    import shutil
    import logging
    import sys

def save_variables(variables, filename):
    with open(filename, 'w') as f:
        for key, value in variables.items():
            f.write(f"{key}={value}\n")

def load_variables(filename):
    variables = {}
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            variables[key] = value
    return variables

def psod(cp):
    pso = """Paragraph screen of death 
------------------------------------------------- 
The system isn't able to handle that error, and you can't fix this either. 
Please contact devs. 
------------------------------------------------- 
ERRTXT: """
    print(pso, cp)

def initialize_logging(log_file):
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

def initialize():
    with open("ver/version.txt", "r") as versionFile:
        version = versionFile.read()
    session = datetime.datetime.now()
    dir_now = os.getcwd()
    log_name = str(dir_now + "/log/" + session.strftime("%Y-%m-%d %H.%M.%S.%f") + ".log")
    initialize_logging(log_name)
    logging.info("Time start")
    return version, session, dir_now, log_name

def import_success_message(start_time):
    import_success_time = time.time()
    import_duration = import_success_time - start_time
    print("Imported successful ({} ms)".format(import_duration * 1000))
    os.system("cls")

def reload():
    load()
    print("Reload successful, return.")

def clear_log():
    folder = 'log'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def get_time():
    return datetime.datetime.now()

def err(error_code):
    logging.info("ERR " + error_code)

def send_test():
    print("Test successful, return.")

def get_version(version):
    print("Current version is:", version)

def exit(session):
    print("Session:", session, "Exiting at:")
    print("Session ended.")
    sys.exit()

def exec_fun(fun_name, variables, version):
    logging.info("FUNC EXEC " + fun_name)
    if len(fun_name) >= 120:
        print("Error at:")
        print("Cannot handle command longer than 120 (", len(fun_name), ")")
        print("Proceed to exit.")
        err("LNG")
        sys.exit()
    else:
        try:
            # Check if the command is a print statement with a variable reference
            if fun_name.startswith("print(") and fun_name.endswith(")"):
                # Extract the variable name from the print statement
                var_name = fun_name[6:-1]
                # Check if the variable exists
                if var_name in variables:
                    # Print the variable value
                    print(variables[var_name])
                else:
                    print("Error at:")
                    print("Variable", var_name, "not defined.")
                    err("NOUNDEF")
            elif fun_name == "get_version()":
                get_version(version)
            else:
                # Execute the command as usual
                exec(fun_name, globals(), variables)
        except SyntaxError as e:
            print("Error at:")
            print("Syntax Error:", e)
            err("SYNERR")
        except NameError:
            print("Error at:")
            print(fun_name + " is not defined (NameError), return.")
            err("NOCMD")
        except ImportError:
            print("Error at:")
            print("No Such Module as " + fun_name + " (ImportError), return.")
            err("NOMOD")

def main():
    cache_file = "__pycache__/variables_cache"
    variables_file = "__pycache__/var.log"
    
    # Load variables from cache or file
    with shelve.open(cache_file) as cache:
        if 'variables' in cache:
            variables = cache['variables']
        else:
            try:
                variables = load_variables(variables_file)
            except FileNotFoundError:
                variables = {}

    version, session, dir_now, log_name = initialize()
    import_success_message(time.time())
    print("Console_", version)
    print(session)
    print(version)

    log_file = open(log_name, "w")
    log_file.write("Console_" + version + str(session) + "\n")
    log_file.close()

    while True:
        console_input = input(dir_now + ">>")
        if console_input.startswith("save"):
            _, var_name, var_value = console_input.split()
            variables[var_name] = var_value
        elif console_input == "exit()":
            # Save variables to file and cache before exiting
            save_variables(variables, variables_file)
            with shelve.open(cache_file) as cache:
                cache['variables'] = variables
            exit(session)
        else:
            # Execute the command and update variables dictionary if needed
            exec_fun(console_input, variables, version)
            # Update variables file and cache
            save_variables(variables, variables_file)
            with shelve.open(cache_file) as cache:
                cache['variables'] = variables

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        psod(e)
        logging.info("PSD EC " + str(e))
        sys.exit()
