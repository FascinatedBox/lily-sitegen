import subprocess, sys

if len(sys.argv) != 2 or \
   sys.argv[1].endswith("lily_pkg_core.c") == False:
    print("Usage: sitegen.py <path to lily_pkg_core.c>")
    sys.exit(0)

subprocess.call(["python", "./gen_basic/gen_basic.py"])
subprocess.call(["lily", "./gen_sandbox/gen_sandbox.lily"])
subprocess.call(["lily", "./gen_core/docgen.lily", sys.argv[1]])
