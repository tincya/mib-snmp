from diagram import mod_entry
import natlas

# Argvs
argvs = ['-r', 'demo.snmplabs.com', '-o', 'network.svg']

DEFAULT_OPT_CONF    = './natlas_lib/natlas.conf'
def argv_get_conf(argv):
    opt_conf = DEFAULT_OPT_CONF
    for i in range(0, len(argv)):
        if (argv[i] == '-c'):
            if ((i+1) >= len(argv)):
                raise Exception('-c used but no file specified')
            opt_conf = argv[i+1]
            del argv[i+1]
            del argv[i]
            break
    return (argv, opt_conf)

def exec_diagram(argvs):
    try:
        natlas_obj = natlas.natlas()
    except Exception as e:
        print('[ERROR] %s' % e)
        return 0
    try:
        argv, opt_conf = argv_get_conf(argvs)
    except Exception as e:
        print('[ERROR] %s' % e)
        return 0
    try:
        natlas_obj.config_load(opt_conf)
    except Exception as e:
        print(e)
        return 0

    modret = mod_entry(natlas_obj, argv)
    if modret!=99:
        print(modret)

exec_diagram(argvs)