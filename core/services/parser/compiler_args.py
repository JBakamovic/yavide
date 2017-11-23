import clang.cindex
import logging
import os

class CompilerArgs():
    class JSONCompilationDatabase():
        def __init__(self, default_compiler_args, filename):
            self.default_compiler_args = default_compiler_args
            self.cached_compiler_args = []
            try:
                self.database = clang.cindex.CompilationDatabase.fromDirectory(os.path.dirname(filename))
            except:
                logging.error(sys.exc_info())

        def get(self, filename):
            def eat_minus_c_compiler_option(json_comp_db_command):
                return json_comp_db_command[0:len(json_comp_db_command)-2] # -c <source_code_filename>

            def eat_minus_o_compiler_option(json_comp_db_command):
                return json_comp_db_command[0:len(json_comp_db_command)-2] # -o <object_file>

            def eat_compiler_invocation(json_comp_db_command):
                return json_comp_db_command[1:len(json_comp_db_command)]   # i.e. /usr/bin/c++

            def cache_compiler_args(args_list):
                # JSON compilation database ('compile_commands.json'):
                #   1. Will include information about translation units only (.cxx)
                #   2. Will NOT include information about header files
                #
                # That is the reason why we have to cache existing compiler
                # arguments (i.e. the ones from translation units existing
                # in JSON database) and apply them equally to any other file
                # which does not exist in JSON database (i.e. header file).
                #
                # This approach will obviously not going to work if there
                # are no translation units in the database at all. I.e. think
                # of header-only libraries.
                self.cached_compiler_args = list(args_list) # most simplest is to create a copy of current ones

            compiler_args = []
            compile_cmds  = self.database.getCompileCommands(filename)
            if compile_cmds:
                for arg in compile_cmds[0].arguments:
                    compiler_args.append(arg)
                compiler_args = self.default_compiler_args + eat_compiler_invocation(eat_minus_o_compiler_option(eat_minus_c_compiler_option(compiler_args)))
                cache_compiler_args(compiler_args)
            else: # doesn't exist in JSON database, use cached compiler args
                compiler_args = list(self.cached_compiler_args)
            return compiler_args

    class CompileFlagsCompilationDatabase():
        def __init__(self, default_compiler_args, filename):
            self.compiler_args = default_compiler_args + [line.rstrip('\n') for line in open(filename)]

        def get(self, filename):
            return self.compiler_args

    class FallbackCompilationDatabase():
        def __init__(self, default_compiler_args):
            self.default_compiler_args = default_compiler_args

        def get(self, filename):
            return self.default_compiler_args

    def __init__(self, compiler_args_filename):
        self.database = None
        self.database_filename = None
        self.default_compiler_args = ['-x', 'c++'] + get_system_includes()
        self.set(compiler_args_filename)
        logging.info('Compiler args filename = {0}. Default compiler args = {1}'.format(compiler_args_filename, self.default_compiler_args))

    def filename(self):
        return self.database_filename

    def set(self, compiler_args_filename):
        self.database_filename = compiler_args_filename
        if self.is_json_database(compiler_args_filename):
            self.database = self.JSONCompilationDatabase(self.default_compiler_args, compiler_args_filename)
        elif self.is_compile_flags_database(compiler_args_filename):
            self.database = self.CompileFlagsCompilationDatabase(self.default_compiler_args, compiler_args_filename)
        else:
            self.database = self.FallbackCompilationDatabase(self.default_compiler_args)
            logging.error("Unsupported way of providing compiler args: '{0}'. Parsing capabilities will be very limited or NOT functional at all!".format(compiler_args_filename))

    def get(self, source_code_filename, source_code_is_modified):
        compiler_args = self.database.get(source_code_filename)
        if source_code_is_modified:
            # Append additional include path to the compiler args which points to the parent directory of current buffer.
            #   * This needs to be done because we will be doing analysis on temporary file which is located outside the project
            #     directory. By doing this, we might invalidate header includes for that particular file and therefore trigger
            #     unnecessary Clang parsing errors.
            #   * An alternative would be to generate tmp files in original location but that would pollute project directory and
            #     potentially would not play well with other tools (indexer, version control, etc.).
            compiler_args.insert(0, ' -I' + os.path.dirname(source_code_filename))
        logging.info('Compiler args = ' + str(compiler_args))
        return compiler_args

    def is_json_database(self, compiler_args_filename):
        return os.path.basename(compiler_args_filename) == 'compile_commands.json'

    def is_compile_flags_database(self, compiler_args_filename):
        return os.path.basename(compiler_args_filename) == 'compile_flags.txt'

def get_system_includes():
    import subprocess
    output = subprocess.Popen(["g++", "-v", "-E", "-x", "c++", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    pattern = ["#include <...> search starts here:", "End of search list."]
    output = str(output)
    return output[output.find(pattern[0]) + len(pattern[0]) : output.find(pattern[1])].replace(' ', '-I').split('\\n')
