from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab
    ext_conn0 = lab.create_external_connector(ini.ext_conn0.__name__, 800,400, is_bridge=True)
    r0 = lab.create_iosv(ini.iosv_0.__name__, 400, 400, slots=1)

    r0.create_links([ext_conn0[0]])
    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()